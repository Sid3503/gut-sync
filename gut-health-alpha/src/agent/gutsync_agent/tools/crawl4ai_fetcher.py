"""
Crawl4AI enrichment layer for DDG search results.
Enriches [{title, href, body}] with full_content from crawled pages.
Falls back to body snippet on crawl failure.
Extracts rich article/guideline titles from content when metadata is generic.
"""
import asyncio
from typing import Any
from urllib.parse import urlparse

# Apply at import time — safe for LangGraph's running event loop
try:
    import nest_asyncio
    nest_asyncio.apply()
except ImportError:
    pass  # nest_asyncio optional; may work without in some environments

_CRAWL4AI_AVAILABLE = False
try:
    from crawl4ai import (
        AsyncWebCrawler,
        BrowserConfig,
        CrawlerRunConfig,
        CacheMode,
        LXMLWebScrapingStrategy,
        DefaultMarkdownGenerator,
        PruningContentFilter,
    )
    _CRAWL4AI_AVAILABLE = True
except ImportError:
    pass


# Shared browser config for all tools
def _get_browser_config() -> Any:
    if not _CRAWL4AI_AVAILABLE:
        raise RuntimeError("Crawl4AI is not installed")
    return BrowserConfig(
        headless=True,
        java_script_enabled=True,
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
    )


def _make_run_config(cache: bool = True) -> Any:
    if not _CRAWL4AI_AVAILABLE:
        raise RuntimeError("Crawl4AI is not installed")
    return CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED if cache else CacheMode.BYPASS,
        wait_until="domcontentloaded",  # Faster than networkidle; CDC/NIH never reach networkidle
        page_timeout=45000,  # 45s for slow gov sites (CDC, NIH)
        delay_before_return_html=1.5,
        word_count_threshold=40,
        remove_overlay_elements=True,
        excluded_tags=["nav", "footer", "header", "aside", "script", "style", "form"],
        scraping_strategy=LXMLWebScrapingStrategy(),
        markdown_generator=DefaultMarkdownGenerator(
            content_filter=PruningContentFilter(
                threshold=0.48,
                threshold_type="dynamic",
                min_word_threshold=25,
            ),
            options={"ignore_links": False},
        ),
    )


def _safe_fit_markdown(result: Any, max_chars: int = 4000) -> str:
    """Safely extract fit_markdown or raw_markdown from a CrawlResult."""
    try:
        if result.markdown:
            md = result.markdown
            if hasattr(md, "fit_markdown") and md.fit_markdown:
                return md.fit_markdown[:max_chars]
            if hasattr(md, "raw_markdown") and md.raw_markdown:
                return md.raw_markdown[:max_chars]
            if isinstance(md, str):
                return md[:max_chars]
    except Exception:
        pass
    return ""


async def _fetch_single_async(url: str, cache: bool = True) -> dict:
    if not _CRAWL4AI_AVAILABLE:
        return {
            "url": url,
            "title": "",
            "fit_markdown": "",
            "success": False,
            "error": "Crawl4AI not installed",
        }
    run_conf = _make_run_config(cache=cache)
    try:
        async with AsyncWebCrawler(config=_get_browser_config()) as crawler:
            crawl_result = await crawler.arun(url=url, config=run_conf)
    except Exception as e:
        return {
            "url": url,
            "title": "",
            "fit_markdown": "",
            "success": False,
            "error": str(e),
        }
    if not crawl_result.success:
        return {
            "url": url,
            "title": "",
            "fit_markdown": "",
            "success": False,
            "error": getattr(crawl_result, "error_message", "Crawl failed"),
        }
    meta = getattr(crawl_result, "metadata", None) or {}
    return {
        "url": getattr(crawl_result, "url", url),
        "title": meta.get("title", ""),
        "fit_markdown": _safe_fit_markdown(crawl_result),
        "success": True,
        "error": None,
    }


async def _fetch_many_async(urls: list[str], max_concurrent: int = 3) -> list[dict]:
    if not _CRAWL4AI_AVAILABLE or not urls:
        return []
    run_conf = _make_run_config(cache=True)
    results_map: dict[str, dict] = {}
    try:
        async with AsyncWebCrawler(config=_get_browser_config()) as crawler:
            raw_results = await crawler.arun_many(urls=urls, config=run_conf)
    except Exception:
        return []
    for res in raw_results:
        url = getattr(res, "url", "")
        meta = getattr(res, "metadata", None) or {}
        results_map[url] = {
            "url": url,
            "title": meta.get("title", ""),
            "fit_markdown": _safe_fit_markdown(res) if getattr(res, "success", False) else "",
            "success": getattr(res, "success", False),
            "error": getattr(res, "error_message", None) if not getattr(res, "success", True) else None,
        }
    ordered = []
    for url in urls:
        if url in results_map:
            ordered.append(results_map[url])
        else:
            matched = next(
                (v for k, v in results_map.items() if url in k or k in url),
                {"url": url, "title": "", "fit_markdown": "", "success": False, "error": "not found"},
            )
            ordered.append(matched)
    return ordered


def fetch_urls(urls: list[str]) -> list[dict]:
    """Sync wrapper for batch URL fetch. Safe for use inside LangGraph nodes."""
    if not urls:
        return []
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_fetch_many_async(urls))
    except Exception:
        return []


def fetch_url(url: str, cache: bool = True) -> dict:
    """Sync wrapper for single URL fetch."""
    try:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(_fetch_single_async(url, cache=cache))
    except Exception:
        return {"url": url, "title": "", "fit_markdown": "", "success": False, "error": "fetch failed"}


# Generic titles that indicate we should extract from content instead
_GENERIC_TITLES = frozenset({
    "pubmed", "pubmed central", "pmc", "pmc.ncbi.nlm.nih.gov",
    "pubmed central - ncbi", "nih", "ncbi", "national library of medicine",
    "cdc", "centers for disease control", "nhs", "nice", "world gastroenterology",
    "rome foundation", "usda", "nutrition.gov", "eatright", "harvard",
})

# Phrases that indicate generic gov/boilerplate metadata (partial match)
_GENERIC_PHRASES = (
    "a website belongs to an official government",
    "official government organization",
    "in the united states",
    "skip to main content",
    "skip to content",
)


def _is_generic_title(title: str) -> bool:
    """True if title is a generic site name rather than article/guideline title."""
    if not title or len(title) < 5:
        return True
    t = title.strip().lower()
    if len(t) < 20 and t in _GENERIC_TITLES:
        return True
    # Gov boilerplate metadata
    for phrase in _GENERIC_PHRASES:
        if phrase in t:
            return True
    # Domain-only patterns (e.g., "pmc.ncbi.nlm.nih.gov")
    if t.count(" ") < 2 and ("." in t or t.endswith(".org") or t.endswith(".gov")):
        return True
    return False


# Lines to skip when extracting title (nav, boilerplate)
_SKIP_PATTERNS = (
    "pubmed", "ncbi", "nih", "search", "sign in", "log in", "menu",
    "home", "skip to", "official government", "united states",
)


def _looks_like_nav(line: str) -> bool:
    """True if line is likely nav/boilerplate, not article title."""
    if not line or len(line) > 150:
        return True
    lower = line.lower()
    return any(p in lower for p in _SKIP_PATTERNS) or len(line) < 12


def _extract_title_from_content(full_content: str, max_len: int = 120) -> str | None:
    """
    Extract article/guideline title from crawled markdown.
    Prefer first # heading, else first substantial line that looks like a title.
    PMC/NIH articles often have title as first non-nav line.
    """
    if not full_content or not full_content.strip():
        return None
    lines = full_content.strip().split("\n")
    candidates: list[str] = []
    for line in lines[:20]:
        line = line.strip()
        if not line or len(line) < 20:
            continue
        if line.startswith(("[", "*", "-", "•", "|", "©")):
            continue
        if "http" in line or _looks_like_nav(line) or _is_generic_title(line):
            continue
        # # heading
        if line.startswith("#"):
            title = line.lstrip("#").strip()
            if 15 <= len(title) <= max_len:
                return title
        # Plain line - article titles often have 4+ words, mixed case
        if 25 <= len(line) <= max_len and line[0].isupper() and line.count(" ") >= 3:
            candidates.append(line)
    return candidates[0] if candidates else None


def _extract_from_ddg_body(body: str) -> str | None:
    """Extract a title-like phrase from DDG snippet (e.g. before ' - PubMed' or first sentence)."""
    if not body or len(body) < 25:
        return None
    # DDG often returns "Article description... - Source" or "First sentence. Second..."
    for sep in (" - ", " | ", " – ", " — "):
        if sep in body:
            part = body.split(sep)[0].strip()
            if 20 <= len(part) <= 120 and not _is_generic_title(part):
                return part
    # First sentence
    first = body.split(".")[0].strip()
    if 20 <= len(first) <= 120 and not _looks_like_nav(first):
        return first
    return None


def _pick_rich_title(
    meta_title: str,
    ddg_title: str,
    full_content: str,
    ddg_body: str,
    url: str,
) -> str:
    """
    Prefer rich, specific title over generic metadata.
    Order: extracted from content > DDG title > DDG body phrase > meta title > domain.
    """
    extracted = _extract_title_from_content(full_content) if full_content else None
    if extracted and not _is_generic_title(extracted):
        return extracted[:120]
    if ddg_title and not _is_generic_title(ddg_title) and len(ddg_title) > 15:
        return ddg_title[:120]
    body_title = _extract_from_ddg_body(ddg_body) if ddg_body else None
    if body_title:
        return body_title[:120]
    if meta_title and not _is_generic_title(meta_title) and len(meta_title) > 15:
        return meta_title[:120]
    try:
        parsed = urlparse(url)
        netloc = (parsed.netloc or url).replace("www.", "")
        return netloc or "Source"
    except Exception:
        return "Source"


def enrich_ddg_results(ddg_results: list[dict]) -> list[dict]:
    """
    Takes raw DDG results [{title, href, body}].
    Returns enriched [{title, href, body, full_content, crawl_success}].
    full_content = fit_markdown from Crawl4AI (~4000 chars). Falls back to body on crawl failure.
    Title is derived from content when metadata is generic (e.g., "PubMed").
    """
    if not ddg_results:
        return []
    urls = [r.get("href", "") for r in ddg_results if r.get("href")]
    if not urls:
        return [
            {**r, "full_content": r.get("body", ""), "crawl_success": False}
            for r in ddg_results
        ]
    if not _CRAWL4AI_AVAILABLE:
        return [
            {**r, "full_content": r.get("body", ""), "crawl_success": False}
            for r in ddg_results
        ]
    try:
        crawled = fetch_urls(urls)
    except Exception:
        return [
            {**r, "full_content": r.get("body", ""), "crawl_success": False}
            for r in ddg_results
        ]
    crawled_by_url = {c["url"]: c for c in crawled}
    seen_titles: set[str] = set()
    enriched = []
    for ddg in ddg_results:
        href = ddg.get("href", "")
        crawl = crawled_by_url.get(href) or next(
            (v for k, v in crawled_by_url.items() if href in k or k in href),
            {},
        )
        full_content = crawl.get("fit_markdown", "")
        if not full_content:
            full_content = ddg.get("body", "")

        meta_title = crawl.get("title", "")
        ddg_title = ddg.get("title", "")
        ddg_body = ddg.get("body", "")

        title = _pick_rich_title(meta_title, ddg_title, full_content, ddg_body, href)

        # Deduplicate: if same title already used, append domain hint
        if title in seen_titles and href:
            try:
                domain = urlparse(href).netloc.replace("www.", "")
                title = f"{title} | {domain}"
            except Exception:
                pass
        seen_titles.add(title)

        enriched.append({
            "title": title,
            "href": href,
            "body": ddg_body,
            "full_content": full_content,
            "crawl_success": crawl.get("success", False),
        })
    return enriched

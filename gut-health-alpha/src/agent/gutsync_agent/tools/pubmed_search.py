# For this alpha, we use DuckDuckGo restricted to site:nih.gov or site:pubmed.ncbi.nlm.nih.gov
# This avoids complex XML parsing of NCBI E-utilities for now, while ensuring reliable sources.
# Crawl4AI enriches results with full_content from crawled pages.

from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool
from src.agent.gutsync_agent.tools.crawl4ai_fetcher import enrich_ddg_results

DOMAINS = "site:nih.gov OR site:pubmed.ncbi.nlm.nih.gov OR site:pmc.ncbi.nlm.nih.gov"


class PubMedSearchTool:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches ONLY reliable medical domains via search engine.
        Trusted: nih.gov, pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov
        Enriches with full_content via Crawl4AI.
        """
        safe_query = f"{DOMAINS} {query}"
        print(f"  [Tool] PubMed/NIH: Searching '{query}'...")

        ddg_results = self.search_tool.search(safe_query)
        if not ddg_results:
            return []

        print(f"  [Tool] Crawl4AI: Enriching {len(ddg_results)} PubMed URLs...")
        return enrich_ddg_results(ddg_results)

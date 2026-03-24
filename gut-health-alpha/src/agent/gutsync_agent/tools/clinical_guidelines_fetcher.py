# Fetches from official bodies: CDC, NHS (UK), NICE, ACG, WGO, Rome Foundation
from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool
from src.agent.gutsync_agent.tools.crawl4ai_fetcher import enrich_ddg_results, fetch_url

ROME_IV_URL = "https://theromefoundation.org/rome-iv/rome-iv-criteria/"

DOMAINS = (
    "site:cdc.gov OR site:nhs.uk OR site:nice.org.uk OR site:gi.org "
    "OR site:worldgastroenterology.org OR site:theromefoundation.org"
)


class ClinicalGuidelinesFetcher:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches ONLY official clinical guideline bodies.
        Trusted: cdc.gov, nhs.uk, nice.org.uk, gi.org (ACG), WGO, Rome Foundation
        Enriches with full_content via Crawl4AI.
        """
        safe_query = f"({DOMAINS}) guidelines {query} management guidelines"
        print(f"  [Tool] Guidelines: Searching '{query}'...")

        ddg_results = self.search_tool.search(safe_query)
        if not ddg_results:
            return []

        print(f"  [Tool] Crawl4AI: Enriching {len(ddg_results)} guideline URLs...")
        return enrich_ddg_results(ddg_results)

    def fetch_rome_criteria(self) -> str:
        """
        Direct fetch of Rome IV IBS diagnostic criteria.
        Returns clean markdown string for injection into prompts.
        """
        print("  [Tool] Fetching Rome IV criteria directly...")
        result = fetch_url(ROME_IV_URL, cache=True)
        return result.get("fit_markdown", "")

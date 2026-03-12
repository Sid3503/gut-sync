# Fetches from official bodies: CDC, NHS (UK), NICE, ACG
from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool

class ClinicalGuidelinesFetcher:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches ONLY official clinical guideline bodies.
        Trusted: cdc.gov, nhs.uk, nice.org.uk, gi.org (ACG)
        """
        domains = "site:cdc.gov OR site:nhs.uk OR site:nice.org.uk OR site:gi.org"
        safe_query = f"({domains}) guidelines {query}"
        print(f"  [Tool] Guidelines: Searching '{query}'...")
        
        return self.search_tool.search(safe_query)

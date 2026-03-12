# For this alpha, we use DuckDuckGo restricted to site:nih.gov or site:pubmed.ncbi.nlm.nih.gov
# This avoids complex XML parsing of NCBI E-utilities for now, while ensuring reliable sources.

from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool

class PubMedSearchTool:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches ONLY reliable medical domains via search engine.
        Trusted: nih.gov, pubmed.ncbi.nlm.nih.gov
        """
        # Constrain search to trusted domains
        safe_query = f"site:nih.gov OR site:pubmed.ncbi.nlm.nih.gov {query}"
        print(f"  [Tool] PubMed/NIH: Searching '{query}'...")
        
        return self.search_tool.search(safe_query)

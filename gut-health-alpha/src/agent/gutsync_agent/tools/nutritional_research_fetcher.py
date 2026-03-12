# Fetches from: USDA, Nutritionix (via web scraping search for alpha), or robust medical nutrition sites.
from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool

class NutritionalResearchFetcher:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches reliable nutrition data sources.
        Trusted: fdc.nal.usda.gov, nutrition.gov, harvard.edu/nutrition, dietitians.org
        """
        domains = "site:fdc.nal.usda.gov OR site:nutrition.gov OR site:hsph.harvard.edu OR site:eatright.org"
        safe_query = f"({domains}) {query}"
        print(f"  [Tool] Nutrition: Searching '{query}'...")
        
        return self.search_tool.search(safe_query)

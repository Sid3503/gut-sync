# Fetches from: USDA, Harvard, Eatright, Open Food Facts API
import requests
from src.agent.gutsync_agent.tools.duckduckgo_search import DuckDuckGoSearchTool
from src.agent.gutsync_agent.tools.crawl4ai_fetcher import enrich_ddg_results

DOMAINS = (
    "site:fdc.nal.usda.gov OR site:nutrition.gov OR site:nal.usda.gov "
    "OR site:hsph.harvard.edu OR site:eatright.org"
)


class NutritionalResearchFetcher:
    def __init__(self, max_results=3):
        self.search_tool = DuckDuckGoSearchTool(max_results=max_results)

    def search(self, query: str) -> list[dict]:
        """
        Searches reliable nutrition data sources.
        Trusted: fdc.nal.usda.gov, nutrition.gov, nal.usda.gov, Harvard, Eatright
        Enriches with full_content via Crawl4AI.
        """
        safe_query = f"({DOMAINS}) {query}"
        print(f"  [Tool] Nutrition: Searching '{query}'...")

        ddg_results = self.search_tool.search(safe_query)
        if not ddg_results:
            return []

        print(f"  [Tool] Crawl4AI: Enriching {len(ddg_results)} nutrition URLs...")
        return enrich_ddg_results(ddg_results)

    def fetch_open_food_facts(self, food_name: str) -> dict:
        """
        Direct Open Food Facts API — free, no auth needed.
        Returns NOVA group, FODMAP indicators, allergens, nutrient per 100g.
        """
        name = food_name.replace(" ", "+")
        url = (
            f"https://world.openfoodfacts.org/cgi/search.pl"
            f"?search_terms={name}&search_simple=1&json=1&page_size=3"
        )
        try:
            resp = requests.get(url, timeout=8)
            data = resp.json()
            products = data.get("products", [])
            return {
                "success": True,
                "source": "open_food_facts",
                "results": [
                    {
                        "name": p.get("product_name", ""),
                        "nova_group": p.get("nova_group", ""),
                        "nutriments": p.get("nutriments", {}),
                        "allergens": p.get("allergens", ""),
                        "ingredients_text": (p.get("ingredients_text") or "")[:300],
                    }
                    for p in products[:3]
                ],
            }
        except Exception as e:
            return {"success": False, "error": str(e), "source": "open_food_facts"}

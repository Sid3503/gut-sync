from duckduckgo_search import DDGS
import time

class DuckDuckGoSearchTool:
    def __init__(self, max_results=3):
        self.max_results = max_results

    def search(self, query: str) -> list[dict]:
        """
        Safely searches DuckDuckGo.
        Returns a list of dicts: {'title': str, 'href': str, 'body': str}
        """
        print(f"  [Tool] DuckDuckGo: Searching for '{query[:60]}...'")
        results = []
        try:
            with DDGS() as ddgs:
                # Default backend is more robust
                results_gen = ddgs.text(query, max_results=self.max_results)
                for r in results_gen:
                    print(f"    - Found: {r.get('title')}")
                    results.append({
                        "title": r.get("title", ""),
                        "href": r.get("href", ""),
                        "body": r.get("body", "")
                    })
        except Exception as e:
            print(f"  [Tool] DuckDuckGo Error: {e}")
            # Fail gracefully returning empty list, never crash graph
            return []
            
        return results

from src.agent.gutsync_agent.service.llm_client import LLMClient
from src.agent.gutsync_agent.tools.nutritional_research_fetcher import NutritionalResearchFetcher

class NutritionalResearchAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.tool = NutritionalResearchFetcher()

    def run(self, diet_changes: str, symptoms: list) -> tuple[list[str], list[dict]]:
        print(f"  [Agent] Running NutritionalResearchAgent...")
        if not diet_changes:
            return [], []
        # Handle None or empty symptoms
        if not symptoms:
            symptoms = []
        query_context = f"{diet_changes} {' '.join(symptoms)} interaction"
        search_results = self.tool.search(query_context)

        if not search_results:
            # Fallback for demo/reliability
            search_results = [{
                "title": "Probiotics: What You Need To Know - NCCIH",
                "href": "https://www.nccih.nih.gov/health/probiotics-what-you-need-to-know",
                "body": "Probiotics such as Lactobacillus and Bifidobacterium can support gut health after antibiotic use. Fermented foods like yogurt and kefir are natural sources.",
            }]

        # Optional: if user mentioned a specific food, add Open Food Facts data
        if diet_changes and len(diet_changes.split()) <= 4:
            off_data = self.tool.fetch_open_food_facts(diet_changes)
            if off_data.get("success") and off_data.get("results"):
                search_results.append({
                    "title": f"Open Food Facts: {diet_changes}",
                    "href": "https://world.openfoodfacts.org",
                    "body": "",
                    "full_content": str(off_data["results"])[:1000],
                    "crawl_success": True,
                })

        # Build context from full_content (Crawl4AI) or body (DDG snippet)
        context_parts = []
        for r in search_results:
            content = r.get("full_content") or r.get("body", "")
            context_parts.append(f"**{r.get('title', '')}**\nSource: {r.get('href', '')}\n{content}")
        context_str = "\n\n---\n\n".join(context_parts)

        prompt = f"""
        You are a nutritional researcher. Analyze these search results from reliable sources (USDA, Harvard Nutrition).
        Find evidence linking diet triggers to symptoms: {query_context}.
        
        Rules:
        - Focus on food properties (FODMAPs, fiber, acidity).
        - Cite the source.
        - ONE sentence per finding.
        - Max 2 findings.

        Search Results:
        {context_str}
        """
        
        response = self.llm.generate_text(prompt)
        insights = [line.strip("- *") for line in response.split("\n") if line.strip()]
        
        sources = [{"title": r.get("title"), "url": r.get("href")} for r in search_results]
        return insights, sources

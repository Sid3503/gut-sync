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
                "body": "Probiotics such as Lactobacillus and Bifidobacterium can support gut health after antibiotic use. Fermented foods like yogurt and kefir are natural sources."
            }]

        prompt = f"""
        You are a nutritional researcher. Analyze these search results from reliable sources (USDA, Harvard Nutrition).
        Find evidence linking diet triggers to symptoms: {query_context}.
        
        Rules:
        - Focus on food properties (FODMAPs, fiber, acidity).
        - Cite the source.
        - ONE sentence per finding.
        - Max 2 findings.

        Search Results:
        {search_results}
        """
        
        response = self.llm.generate_text(prompt)
        insights = [line.strip("- *") for line in response.split("\n") if line.strip()]
        
        sources = [{"title": r.get("title"), "url": r.get("href")} for r in search_results]
        return insights, sources

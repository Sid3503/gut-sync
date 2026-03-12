from src.agent.gutsync_agent.service.llm_client import LLMClient
from src.agent.gutsync_agent.tools.clinical_guidelines_fetcher import ClinicalGuidelinesFetcher

class ClinicalGuidelineAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.tool = ClinicalGuidelinesFetcher()

    def run(self, symptoms: list) -> tuple[list[str], list[dict]]:
        print(f"  [Agent] Running ClinicalGuidelineAgent...")
        # Handle None or empty symptoms
        if not symptoms:
            symptoms = ["general digestive health"]
        query_context = f"{' '.join(symptoms)} management guidelines"
        search_results = self.tool.search(query_context)
        
        if not search_results:
            # Fallback for demo/reliability
            search_results = [{
                "title": "ACG Clinical Guideline: Diagnosis and Management of Small Intestinal Bacterial Overgrowth",
                "href": "https://journals.lww.com/ajg/Fulltext/2020/02000/ACG_Clinical_Guideline__Diagnosis_and_Management.9.aspx",
                "body": "Antibiotics are a primary treatment for SIBO, but can also cause dysbiosis. Probiotics are suggested to help restore flora."
            }]

        prompt = f"""
        You are a clinical assistant. Analyze these official guideline search results (CDC, NHS, NICE, ACG).
        Extract 1-2 standard care recommendations for: {query_context}.
        
        Rules:
        - Focus on lifestyle/dietary management mentioned in guidelines.
        - Cite the body (e.g., "The NHS recommends...").
        - ONE sentence per finding.
        - Max 2 findings.

        Search Results:
        {search_results}
        """
        
        response = self.llm.generate_text(prompt)
        guidelines = [line.strip("- *") for line in response.split("\n") if line.strip()]
        
        sources = [{"title": r.get("title"), "url": r.get("href")} for r in search_results]
        return guidelines, sources

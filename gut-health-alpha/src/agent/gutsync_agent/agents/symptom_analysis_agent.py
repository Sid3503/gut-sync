import json
from src.agent.gutsync_agent.service.llm_client import LLMClient
from src.agent.gutsync_agent.tools.medication_lookup import MedicationLookup

class SymptomAnalysisAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.med_tool = MedicationLookup()

    def run(self, symptoms: list, timing: str, medications: list, pdf_context: str = None) -> list:
        # Lookup meds
        med_effects = {}
        if medications:
            for med in medications:
                effects = self.med_tool.lookup(med)
                if effects:
                    med_effects[med] = effects

        prompt_path = "src/agent/gutsync_agent/prompts/symptom_analysis.md"
        with open(prompt_path, "r") as f:
            template = f.read()

        context_str = f"\n\nAdditional Clinical Context from Documents:\n{pdf_context}" if pdf_context else ""

        prompt = template.replace("{symptoms}", str(symptoms))\
                         .replace("{timing}", str(timing))\
                         .replace("{medications}", str(medications))\
                         .replace("{medication_effects}", json.dumps(med_effects))\
                         .replace("{pdf_context}", context_str)

        return self.llm.generate_json(prompt)

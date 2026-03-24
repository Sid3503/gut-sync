import os
import json
from src.agent.gutsync_agent.service.llm_client import LLMClient

class RootCauseAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, symptoms: list, timing: str, diet_changes: str, patterns: list, pdf_context: str = None) -> list:
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "root_cause.md")
        with open(prompt_path, "r") as f:
            template = f.read()

        context_str = f"\n\nAdditional Clinical Context from Documents:\n{pdf_context}" if pdf_context else ""

        prompt = template.replace("{symptoms}", str(symptoms))\
                         .replace("{timing}", str(timing))\
                         .replace("{diet_changes}", str(diet_changes))\
                         .replace("{symptom_patterns}", str(patterns))\
                         .replace("{pdf_context}", context_str)
        
        return self.llm.generate_json(prompt)

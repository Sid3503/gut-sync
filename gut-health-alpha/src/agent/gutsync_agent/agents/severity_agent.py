import os
from src.agent.gutsync_agent.service.llm_client import LLMClient

class SeverityAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, symptoms: list, patterns: list) -> str:
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "severity.md")
        with open(prompt_path, "r") as f:
            template = f.read()

        prompt = template.replace("{symptoms}", str(symptoms))\
                         .replace("{symptom_patterns}", str(patterns))
        
        response = self.llm.generate_text(prompt) # Expecting raw string "mild", "moderate", "severe"
        return response.strip().lower()

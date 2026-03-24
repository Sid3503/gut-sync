import os
import json
from src.agent.gutsync_agent.service.llm_client import LLMClient

class ReliefStrategyAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, symptoms: list, root_causes: list, severity: str) -> list:
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "relief.md")
        with open(prompt_path, "r") as f:
            template = f.read()

        prompt = template.replace("{symptoms}", str(symptoms))\
                         .replace("{possible_root_causes}", str(root_causes))\
                         .replace("{severity}", severity)
        
        return self.llm.generate_json(prompt)

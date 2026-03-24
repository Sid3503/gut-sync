import os
import json
from src.agent.gutsync_agent.service.llm_client import LLMClient

class IntakeAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, user_input: str) -> dict:
        prompt_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts", "intake.md")
        with open(prompt_path, "r") as f:
            template = f.read()
        
        prompt = template.replace("{user_input}", user_input)
        response = self.llm.generate_json(prompt)
        return response

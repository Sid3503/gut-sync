import json
from src.agent.gutsync_agent.service.llm_client import LLMClient
from src.agent.gutsync_agent.tools.red_flag_rules import RedFlagRules

class RedFlagAgent:
    def __init__(self):
        self.llm = LLMClient()
        self.rules_tool = RedFlagRules()

    def run(self, user_input: str, symptoms: list) -> list:
        rules = self.rules_tool.get_rules()
        
        prompt_path = "src/agent/gutsync_agent/prompts/red_flags.md"
        with open(prompt_path, "r") as f:
            template = f.read()

        prompt = template.replace("{user_input}", user_input)\
                         .replace("{symptoms}", str(symptoms))\
                         .replace("{red_flag_rules}", json.dumps(rules))
        
        return self.llm.generate_json(prompt)

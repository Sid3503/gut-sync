import json
import os

class RedFlagRules:
    def __init__(self):
        self.db_path = "data/red_flag_rules.json"

    def get_rules(self) -> dict:
        if not os.path.exists(self.db_path):
            return {}
            
        with open(self.db_path, "r") as f:
            rules = json.load(f)
            print(f"  [Tool] RedFlagRules: Loaded {sum(len(v) for v in rules.values())} rules.")
            return rules

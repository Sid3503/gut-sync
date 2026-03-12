import json
import os

class SymptomMapper:
    def __init__(self):
        self.db_path = "data/symptom_mappings.json"

    def map_symptom(self, raw_symptom: str) -> str:
        if not os.path.exists(self.db_path):
            return raw_symptom
            
        with open(self.db_path, "r") as f:
            mapping = json.load(f)
        
        result = mapping.get(raw_symptom.lower(), raw_symptom)
        print(f"  [Tool] SymptomMapper: '{raw_symptom}' -> '{result}'")
        return result

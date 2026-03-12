import json
import os

class MedicationLookup:
    def __init__(self):
        self.db_path = "data/medication_gut_effects.json"
        
    def lookup(self, medication_name: str) -> list:
        if not os.path.exists(self.db_path):
            return []
            
        with open(self.db_path, "r") as f:
            db = json.load(f)
            
        print(f"  [Tool] MedicationLookup: Checking '{medication_name}'...")
        return db.get(medication_name.lower(), [])

import json
import os

FILE_PATH = "profiles.json"

def load_profiles():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("profiles", []) 
    

def save_profiles(profiles: list):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"profiles": profiles},
            f,
            ensure_ascii=False,
            indent=2
        )

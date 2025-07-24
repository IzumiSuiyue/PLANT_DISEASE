import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "disease.json"

def load_disease_dict():
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_disease_dict(data: dict):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_disease_dict():
    return load_disease_dict()

def update_disease(name: str, symptom: str, cause: str, control: list[str]):
    data = load_disease_dict()
    data[name] = {
        "symptom": symptom,
        "cause": cause,
        "control": control
    }
    save_disease_dict(data)

def delete_disease(name: str):
    data = load_disease_dict()
    if name in data:
        del data[name]
        save_disease_dict(data)

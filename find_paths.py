import json

with open("sample_gmaps_blob.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def search_paths(obj, current_path=""):
    if isinstance(obj, str):
        if "Churrascaria" in obj or "Costela" in obj or "Fogo" in obj or "Espeto" in obj:
            print(f"Path: {current_path} -> {obj[:80]}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            search_paths(item, f"{current_path}[{idx}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            search_paths(v, f"{current_path}['{k}']")

search_paths(data)

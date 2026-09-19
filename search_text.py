import json

with open("gmaps_api_resp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Search for any strings that look like restaurant names or addresses in SP
strings_with_context = []

def search_text(obj, path=""):
    if isinstance(obj, str):
        if any(w in obj for w in ["Churrascaria", "Fogo", "Vento Haragano", "Boi", "Costelão", "Espeto", "Picanha"]):
            print(f"Path: {path} => {obj[:100]}")
    elif isinstance(obj, list):
        for i, el in enumerate(obj):
            search_text(el, f"{path}[{i}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            search_text(v, f"{path}['{k}']")

search_text(data)

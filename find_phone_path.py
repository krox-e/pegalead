import json

with open("gmaps_api_resp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

places_list = data[64]
for idx, entry in enumerate(places_list[:5]):
    if not entry or len(entry) < 2 or not entry[1]:
        continue
    item = entry[1]
    name = item[11] if len(item) > 11 else None
    
    # Let's find all string elements in item and print their index paths
    print(f"\n--- Place {idx}: {name} ---")
    def find_indexed_strings(obj, path=""):
        if isinstance(obj, str):
            if any(c.isdigit() for c in obj) and len(obj) < 40 and not obj.startswith("http") and not obj.startswith("ChIJ") and not obj.startswith("0x") and not obj.startswith("2ahU"):
                print(f"  {path} = {obj}")
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                find_indexed_strings(v, f"{path}[{i}]")
    find_indexed_strings(item)

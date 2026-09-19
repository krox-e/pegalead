import json

with open("gmaps_api_resp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

places_list = data[64]
for idx, entry in enumerate(places_list[:5]):
    if not entry or len(entry) < 2 or not entry[1]:
        continue
    item = entry[1]
    name = item[11] if len(item) > 11 else None
    
    # Let's inspect all fields of item to find place ID, google maps link, phone field index
    print(f"\nPlace {idx}: {name}")
    for i, val in enumerate(item):
        if val is not None:
            val_str = str(val)
            if len(val_str) < 150:
                print(f"  item[{i}] = {val_str}")

import json

with open("sample_gmaps_blob.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data[11]
print(f"data[11] length: {len(items)}")

for idx, item in enumerate(items):
    if not item or not isinstance(item, list):
        continue
    # Let's inspect item[14]
    if len(item) > 14 and item[14]:
        info = item[14]
        title = info[11] if len(info) > 11 else None
        rating = info[4][7] if len(info) > 4 and isinstance(info[4], list) and len(info[4]) > 7 else (info[4][0] if len(info) > 4 and isinstance(info[4], list) else None)
        website = info[7][0] if len(info) > 7 and isinstance(info[7], list) and len(info[7]) > 0 else None
        phone = None
        # let's search for phone numbers in info
        info_str = json.dumps(info, ensure_ascii=False)
        print(f"\nItem {idx}:")
        print(f"  Title: {title}")
        print(f"  Website: {website}")
        # Search all strings in info
        strings = []
        def extract_strings(x):
            if isinstance(x, str):
                strings.append(x)
            elif isinstance(x, list):
                for y in x:
                    extract_strings(y)
            elif isinstance(x, dict):
                for v in x.values():
                    extract_strings(v)
        extract_strings(info)
        print(f"  Sample strings: {strings[:8]}")

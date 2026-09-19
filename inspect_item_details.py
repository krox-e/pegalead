import json

with open("sample_gmaps_blob.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for idx, item in enumerate(data[11]):
    print(f"item {idx}: type={type(item)}, len={len(item) if isinstance(item, list) else 'N/A'}")
    if isinstance(item, list):
        # find where restaurant names appear
        for sub_idx, sub in enumerate(item):
            if isinstance(sub, str) and ("Churrascaria" in sub or "Churrasco" in sub or "Boi" in sub or "Costela" in sub):
                print(f"  found at [{idx}][{sub_idx}]: {sub}")
            elif isinstance(sub, list):
                s = json.dumps(sub, ensure_ascii=False)
                if "Churrascaria" in s or "Churrasco" in s or "Costela" in s:
                    print(f"  found in list at [{idx}][{sub_idx}], len={len(sub)}, preview: {s[:100]}")

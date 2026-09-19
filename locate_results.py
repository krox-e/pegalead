import json

with open("sample_gmaps_blob.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for i, x in enumerate(data):
    if isinstance(x, list):
        print(f"data[{i}]: len={len(x)}")
        if len(x) > 0 and isinstance(x[0], list):
            print(f"   data[{i}][0]: len={len(x[0])}")
            if len(x) > 1 and isinstance(x[1], list):
                print(f"   data[{i}][1]: len={len(x[1])}")

import json

with open("sample_gmaps_blob.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# parsed[0][1] or parsed[0] or parsed[0][1]...
# Let's find entries that represent places
print("Searching for places in blob...")

places = []
def find_places(obj, depth=0):
    if depth > 10:
        return
    if isinstance(obj, list):
        # A place entity often has name, rating, address, coordinates, place_id
        # Let's inspect items
        if len(obj) > 14 and isinstance(obj[14], list) and len(obj) > 1 and isinstance(obj[11], str):
            # Might be a place
            pass
        for item in obj:
            find_places(item, depth + 1)
    elif isinstance(obj, dict):
        for v in obj.values():
            find_places(v, depth + 1)

# In Google Maps search results, parsed[0][1] contains the list of results:
results_container = data[0][1]
print(f"Results container length: {len(results_container) if results_container else 'None'}")

if results_container:
    for idx, res in enumerate(results_container):
        if not res or not isinstance(res, list) or len(res) < 15:
            continue
        # res[14] usually holds place details
        details = res[14]
        if not details or not isinstance(details, list):
            continue
        
        # Details indices:
        # details[11]: title/name
        # details[4]: rating
        # details[4][7]: review count
        # details[7]: website (if any)
        # details[178] or details[183] or details[14]: phone, address
        print(f"\n--- Item {idx} ---")
        # Let's print fields that are strings or short lists
        for d_idx, field in enumerate(details):
            if field is not None and d_idx in [11, 4, 7, 13, 14, 18, 2, 39, 178, 183]:
                print(f"  details[{d_idx}] = {str(field)[:120]}")

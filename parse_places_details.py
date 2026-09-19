import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open("gmaps_api_resp.json", "r", encoding="utf-8") as f:
    data = json.load(f)

places_list = data[64]
print(f"Total entries in data[64]: {len(places_list)}")

for idx, entry in enumerate(places_list):
    if not entry or len(entry) < 2 or not entry[1]:
        continue
    item = entry[1]
    name = item[11] if len(item) > 11 else None
    addr = item[18] if len(item) > 18 else None
    
    # Check website:
    website = None
    if len(item) > 7 and item[7]:
        website = item[7][0] if isinstance(item[7], list) else item[7]
        
    # Check rating and reviews:
    rating = None
    reviews = None
    if len(item) > 4 and item[4] and isinstance(item[4], list):
        rating = item[4][7] if len(item[4]) > 7 else (item[4][0] if len(item[4]) > 0 else None)
        reviews = item[4][8] if len(item[4]) > 8 else None
        
    # Check phone:
    phones = []
    def find_phone(obj):
        if isinstance(obj, str):
            if any(p in obj for p in ["+55", "(11)", "(21)", "(31)", "(41)", "(51)", "(61)", "(71)", "(81)", "(85)", "(62)", "(19)", "(13)"]):
                phones.append(obj)
        elif isinstance(obj, list):
            for x in obj:
                find_phone(x)
        elif isinstance(obj, dict):
            for v in obj.values():
                find_phone(v)
    find_phone(item)
    phone = phones[0] if phones else None
    
    # Check coordinates:
    lat, lon = None, None
    if len(item) > 9 and isinstance(item[9], list) and len(item[9]) >= 3:
        lat = item[9][2]
        lon = item[9][3] if len(item[9]) > 3 else None
        
    print(f"\n--- [{idx}] {name} ---")
    print(f"  Endereço: {addr}")
    print(f"  Website: {website}")
    print(f"  Avaliação: {rating} ({reviews} avaliações)")
    print(f"  Telefone: {phone}")
    print(f"  Coords: {lat}, {lon}")

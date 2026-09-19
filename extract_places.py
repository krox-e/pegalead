import httpx
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = "https://www.google.com/maps/search/churrascaria+sao+paulo"
r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)
match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
r2 = httpx.get(sub_url, headers=headers, follow_redirects=True, timeout=15.0)

text = r2.text
if text.startswith(")]}'"):
    text = text[4:].strip()

data = json.loads(text)

# Let's save data to a file
with open("gmaps_api_resp.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Saved gmaps_api_resp.json. Total top-level elements:", len(data))

# Find places
def find_places(obj, path=""):
    if isinstance(obj, list):
        # In Google Maps, a place entry in search results is usually a list where item[14] is another list containing name, rating, address, etc.
        # Or item[11] is a string or item[1] is a list
        if len(obj) > 14 and isinstance(obj[14], list) and len(obj[14]) > 11 and isinstance(obj[14][11], str):
            info = obj[14]
            name = info[11]
            address = info[2] if len(info) > 2 else None
            rating = info[4][7] if len(info) > 4 and isinstance(info[4], list) and len(info[4]) > 7 else None
            num_reviews = info[4][8] if len(info) > 4 and isinstance(info[4], list) and len(info[4]) > 8 else None
            website = info[7][0] if len(info) > 7 and isinstance(info[7], list) and len(info[7]) > 0 else None
            phone = info[178][0] if len(info) > 178 and isinstance(info[178], list) and len(info[178]) > 0 else None
            print(f"Found place at {path}: {name} | Rating: {rating} ({num_reviews}) | Web: {website} | Phone: {phone} | Addr: {address}")
        for idx, item in enumerate(obj):
            find_places(item, f"{path}[{idx}]")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            find_places(v, f"{path}['{k}']")

find_places(data)

import httpx
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = "https://www.google.com/maps/search/churrascaria+em+sao+paulo"
r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)

match = re.search(r'window\.APP_INITIALIZATION_STATE\s*=\s*(.+?);window\.', r.text)
if match:
    raw_json = json.loads(match.group(1))
    # data[3][1] is a string starting with )]}'
    blob_str = raw_json[3][1]
    if blob_str.startswith(")]}'"):
        blob_str = blob_str[4:].strip()
    
    parsed = json.loads(blob_str)
    # The list of places is usually in parsed[0][1] or parsed[0][1] list
    print("Parsed blob type:", type(parsed))
    print("Parsed blob len:", len(parsed))
    
    # Save a clean sample to inspect
    with open("sample_gmaps_blob.json", "w", encoding="utf-8") as f:
        json.dump(parsed, f, ensure_ascii=False, indent=2)
    print("Saved sample_gmaps_blob.json")

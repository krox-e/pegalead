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
    data_str = match.group(1)
    data = json.loads(data_str)
    print("Type of data:", type(data))
    print("Len of data:", len(data))
    for i, item in enumerate(data):
        if item is not None:
            s = str(item)
            print(f"Index {i}: type {type(item)}, len/preview: {s[:100]}")
            if "Churrascaria" in s or "churrascaria" in s:
                print(f"--> Found 'churrascaria' in index {i}!")
                
    # Also check other scripts in r.text
    scripts = re.findall(r'window\.APP_OPTIONS\s*=\s*(.+?);', r.text)
    print("APP_OPTIONS:", len(scripts))

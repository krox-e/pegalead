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
if match:
    sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
    print("Found map search API URL:", sub_url[:120])
    
    r2 = httpx.get(sub_url, headers=headers, follow_redirects=True, timeout=15.0)
    print("API Status:", r2.status_code)
    print("API Content Length:", len(r2.text))
    
    text = r2.text
    if text.startswith(")]}'"):
        text = text[4:].strip()
    
    try:
        data = json.loads(text)
        print("Successfully loaded JSON!")
        # Let's inspect data[0][1]
        results = data[0][1]
        print(f"Number of results in data[0][1]: {len(results)}")
        for i, item in enumerate(results):
            if item and len(item) > 14 and item[14]:
                info = item[14]
                name = info[11] if len(info) > 11 else "N/A"
                # Check for rating, website, phone, address
                # Let's inspect fields in info
                print(f"Result {i}: {name}")
    except Exception as e:
        print("JSON parse error:", e)
        with open("raw_api_resp.txt", "w", encoding="utf-8") as f:
            f.write(r2.text)

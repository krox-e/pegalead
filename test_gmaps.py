import httpx
import json
import re
from urllib.parse import quote

# Test fetching from Google Maps search HTML / API
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = "https://www.google.com/maps/search/churrascaria+em+sao+paulo"
try:
    r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)
    print("Status:", r.status_code)
    print("Content length:", len(r.text))
    # Look for business data in initial data window.APP_INITIALIZATION_STATE
    matches = re.findall(r'window\.APP_INITIALIZATION_STATE\s*=\s*(.+?);window\.', r.text)
    if matches:
        print("Found APP_INITIALIZATION_STATE!")
    else:
        # Check for other data blobs
        print("Looking for blobs...")
        if "_pageData" in r.text or "AF_initDataCallback" in r.text:
            print("Found page data / AF_initDataCallback")
except Exception as e:
    print("Error:", e)

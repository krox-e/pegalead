import httpx
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

url = "https://www.google.com/maps/search/churrascaria+sao+paulo"
r = httpx.get(url, headers=headers, follow_redirects=True, timeout=15.0)

matches = [m.start() for m in re.finditer(r'churrascaria', r.text, re.IGNORECASE)]
print(f"Found {len(matches)} occurrences of 'churrascaria' in r.text")

for pos in matches[:5]:
    start = max(0, pos - 100)
    end = min(len(r.text), pos + 200)
    print("--- Snippet ---")
    print(r.text[start:end])

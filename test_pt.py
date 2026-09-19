import httpx
import re
import json
from urllib.parse import quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8'
}
client = httpx.Client(timeout=15.0)

queries = [
    "clinica dentaria lisboa",
    "clinica dentaria porto",
    "dentista braga",
    "clinica odontologica coimbra",
    "estetica lisboa",
    "energia solar portugal"
]

def is_portugal_phone(cand):
    if not cand or not isinstance(cand, str):
        return False, None, None, False
    if any(w in cand.lower() for w in ["rua", "r.", "av.", "avenida", "alameda", "estrada", "praça", "largo", "bairro", "cep", "http", "nº"]):
        return False, None, None, False
    
    digits = re.sub(r'\D', '', cand)
    if digits.startswith("351") and len(digits) == 12:
        digits = digits[3:]
    elif digits.startswith("00351") and len(digits) == 14:
        digits = digits[5:]
        
    if len(digits) != 9:
        return False, None, None, False
    
    is_mobile = digits.startswith("9")
    formatted = f"+351 {digits[0:3]} {digits[3:6]} {digits[6:9]}" if is_mobile else f"+351 {digits[0:2]} {digits[2:5]} {digits[5:9]}"
    wa_link = f"https://wa.me/351{digits}"
    return True, formatted, wa_link, is_mobile

for q in queries:
    url = f"https://www.google.com/maps/search/{quote(q)}"
    r = client.get(url, headers=headers, follow_redirects=True)
    match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
    if not match:
        print(f"No match for {q}")
        continue
    sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
    r2 = client.get(sub_url, headers=headers, follow_redirects=True)
    text = r2.text
    if text.startswith(")]}'"):
        text = text[4:].strip()
    data = json.loads(text)
    items = data[64] if len(data) > 64 and data[64] else []
    print(f"\n=== Query: {q} (Found {len(items)} places) ===")
    
    for it in items:
        if not it or len(it) < 2 or not it[1]:
            continue
        entry = it[1]
        name = entry[11].strip() if len(entry) > 11 and entry[11] else "Sem nome"
        has_site = False
        if len(entry) > 7 and entry[7]:
            if isinstance(entry[7], list) and len(entry[7]) > 0 and entry[7][0]:
                has_site = True
            elif isinstance(entry[7], str) and entry[7].strip():
                has_site = True
                
        # extract phone candidates
        raw_candidates = []
        if len(entry) > 178 and entry[178] and isinstance(entry[178], list) and len(entry[178]) > 0:
            p_obj = entry[178][0]
            if isinstance(p_obj, list) and len(p_obj) > 0 and isinstance(p_obj[0], str):
                raw_candidates.append(p_obj[0])
            elif isinstance(p_obj, str):
                raw_candidates.append(p_obj)
                
        def search_strings(obj):
            if isinstance(obj, str):
                if any(c.isdigit() for c in obj) and len(obj) < 40:
                    raw_candidates.append(obj)
            elif isinstance(obj, list):
                for x in obj:
                    search_strings(x)
            elif isinstance(obj, dict):
                for v in obj.values():
                    search_strings(v)
        search_strings(entry)
        
        found_phone = None
        for cand in raw_candidates:
            ok, fmt, link, is_mob = is_portugal_phone(cand)
            if ok:
                found_phone = (fmt, link, is_mob)
                break
                
        address = entry[39] if len(entry) > 39 and entry[39] else (entry[18] if len(entry) > 18 else "")
        print(f"Place: {name} | HasSite: {has_site} | Phone: {found_phone} | Address: {address}")

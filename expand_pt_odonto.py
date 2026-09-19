import httpx
import re
import json
import time
from urllib.parse import quote

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-PT,pt;q=0.9,en;q=0.8'
}
client = httpx.Client(timeout=15.0)

def is_portugal_phone(cand):
    if not cand or not isinstance(cand, str):
        return False, None, None, False
    if any(w in cand.lower() for w in ["rua", "r.", "av.", "avenida", "alameda", "estrada", "praça", "largo", "bairro", "cep", "http", "nº", "loja", "piso"]):
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

def extract_pt_phone(item):
    raw_candidates = []
    if len(item) > 178 and item[178] and isinstance(item[178], list) and len(item[178]) > 0:
        p_obj = item[178][0]
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
    search_strings(item)
    
    # Priority mobile (9)
    for cand in raw_candidates:
        ok, fmt, link, is_mob = is_portugal_phone(cand)
        if ok and is_mob:
            return fmt, link, True
            
    return None, None, False

def extract_city(address_str, item):
    m = re.search(r'\d{4}-\d{3}\s+([A-Za-zÀ-ÿ\s]+)', address_str)
    if m:
        city = m.group(1).split(',')[0].strip()
        return f"{city}, Portugal"
    for c in ["Lisboa", "Porto", "Braga", "Coimbra", "Setúbal", "Faro", "Aveiro", "Leiria", "Guimarães", "Cascais", "Sintra", "Vila Nova de Gaia", "Funchal", "Almada", "Matosinhos", "Viseu", "Évora", "Portimão", "Barreiro", "Amadora", "Maia", "Odivelas"]:
        if c.lower() in address_str.lower():
            return f"{c}, Portugal"
    return "Portugal"

queries = [
    "consultorio dentario lisboa", "medico dentista lisboa", "ortodontista lisboa",
    "consultorio dentario porto", "dentista porto boavista", "ortodontista porto",
    "medico dentista braga", "implantes dentarios braga",
    "consultorio dentario coimbra", "medico dentista coimbra",
    "dentista setubal centro", "clinica dentaria barreiro",
    "dentista faro", "dentista portimao", "dentista albufeira",
    "dentista aveiro", "dentista leiria", "dentista viseu",
    "dentista cascais", "dentista sintra", "dentista amadora", "dentista odivelas",
    "dentista vila nova de gaia", "dentista matosinhos", "dentista maia",
    "dentista evora", "dentista santarem", "dentista viana do castelo"
]

existing_leads = []
try:
    with open("clinicas_dentarias_portugal_leads.json", "r", encoding="utf-8") as f:
        existing_leads = json.load(f)
except Exception:
    existing_leads = []

seen_phones = {re.sub(r'\D', '', l["whatsapp"]) for l in existing_leads}
seen_names = {l["name"].lower() for l in existing_leads}

default_msg = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."

for q in queries:
    if len(existing_leads) >= 40:
        break
    url = f"https://www.google.com/maps/search/{quote(q)}"
    try:
        r = client.get(url, headers=headers, follow_redirects=True, timeout=12.0)
        if r.status_code != 200: continue
        match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
        if not match: continue
        sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
        r2 = client.get(sub_url, headers=headers, follow_redirects=True, timeout=12.0)
        if r2.status_code != 200: continue
        text = r2.text
        if text.startswith(")]}'"): text = text[4:].strip()
        data = json.loads(text)
        if len(data) <= 64 or not data[64]: continue
        
        for entry in data[64]:
            if len(existing_leads) >= 40: break
            if not entry or len(entry) < 2 or not entry[1]: continue
            item = entry[1]
            if len(item) < 12 or not item[11]: continue
            name = item[11].strip()
            if name.lower() in seen_names: continue
            
            cats = item[13] if len(item) > 13 and isinstance(item[13], list) else []
            
            # check site
            site = None
            if len(item) > 7 and item[7]:
                if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
                    site = str(item[7][0]).strip()
                elif isinstance(item[7], str) and item[7].strip():
                    site = item[7].strip()
            if site and not ("business.site" in site or "facebook" in site or "instagram" in site):
                continue
                
            phone_fmt, wa_link, is_mob = extract_pt_phone(item)
            if not phone_fmt or not is_mob: continue
            
            clean_digits = re.sub(r'\D', '', phone_fmt)
            if clean_digits in seen_phones: continue
            
            seen_phones.add(clean_digits)
            seen_names.add(name.lower())
            
            address = item[39] if len(item) > 39 and item[39] else (item[18] if len(item) > 18 else "")
            rating = "5.0"
            reviews = 10
            if len(item) > 4 and item[4] and isinstance(item[4], list):
                if len(item[4]) > 7 and item[4][7] is not None:
                    rating = f"{item[4][7]:.1f}"
                elif len(item[4]) > 0 and item[4][0] is not None:
                    rating = f"{item[4][0]:.1f}"
                if len(item[4]) > 8 and item[4][8] is not None:
                    reviews = item[4][8]
            place_id = item[78] if len(item) > 78 and isinstance(item[78], str) else None
            gmaps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + address)}"
            city_state = extract_city(address, item)
            bairro = item[14] if len(item) > 14 and isinstance(item[14], str) else city_state.split(',')[0]
            
            existing_leads.append({
                "country": "PT",
                "name": name,
                "categories": ", ".join(cats) if cats else q,
                "address": address,
                "bairro": bairro,
                "city_state": city_state,
                "whatsapp": phone_fmt,
                "wa_link": wa_link,
                "rating": rating,
                "reviews": reviews,
                "gmaps_url": gmaps_url,
                "place_id": place_id,
                "instagram": "Não identificado / Sem site",
                "reviews_int": reviews,
                "mensagem_personalizada": default_msg,
                "wa_link_com_mensagem": f"{wa_link}?text={quote(default_msg)}"
            })
    except Exception:
        pass

with open("clinicas_dentarias_portugal_leads.json", "w", encoding="utf-8") as f:
    json.dump(existing_leads, f, ensure_ascii=False, indent=2)

print(f"Total de clinicas dentarias Portugal salvas: {len(existing_leads)}")

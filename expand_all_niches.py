import httpx
import re
import json
import time
import sys
import csv
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

VALID_DDDS = {
    11, 12, 13, 14, 15, 16, 17, 18, 19, # SP
    21, 22, 24, # RJ
    27, 28, # ES
    31, 32, 33, 34, 35, 37, 38, # MG
    41, 42, 43, 44, 45, 46, # PR
    47, 48, 49, # SC
    51, 53, 54, 55, # RS
    61, # DF
    62, 64, # GO
    63, # TO
    65, 66, # MT
    67, # MS
    68, 69, # AC, RO
    71, 73, 74, 75, 77, # BA
    79, # SE
    81, 87, # PE
    82, # AL
    83, # PB
    84, # RN
    85, 88, # CE
    86, 89, # PI
    91, 93, 94, # PA
    92, 97, # AM
    95, 96, 98, 99 # RR, AP, MA
}

def is_true_brazil_mobile(cand):
    if not cand or not isinstance(cand, str):
        return False, None, None
    if any(w in cand.lower() for w in ["av.", "avenida", "rua", "r.", "rodovia", "alameda", "travessa", "estrada", "bairro", "cep", "km", "http"]):
        return False, None, None
        
    digits = re.sub(r'\D', '', cand)
    if digits.startswith("55") and len(digits) == 13:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 12:
        digits = digits[1:]
        
    if len(digits) != 11:
        return False, None, None
        
    ddd = int(digits[:2])
    if ddd not in VALID_DDDS:
        return False, None, None
        
    if digits[2] != '9':
        return False, None, None
    if digits[3] not in '567894':
        return False, None, None
        
    formatted = f"({ddd}) {digits[2:7]}-{digits[7:]}"
    wa_link = f"https://wa.me/55{digits}"
    return True, formatted, wa_link

def extract_mobile_phone(item):
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
    
    for cand in raw_candidates:
        ok, fmt, link = is_true_brazil_mobile(cand)
        if ok:
            return fmt, link
    return None, None

def get_maps_website(item):
    if len(item) > 7 and item[7]:
        if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
            return str(item[7][0]).strip()
        elif isinstance(item[7], str) and item[7].strip():
            return item[7].strip()
    return None

def extract_city_state(address_str, item):
    if len(item) > 2 and item[2] and isinstance(item[2], list) and len(item[2]) > 1:
        part = item[2][1]
        if "-" in part and len(part.strip()) < 40:
            return part.strip()
    m = re.search(r'([A-Za-zÀ-ÿ\s]+)\s*-\s*([A-Z]{2})', address_str)
    if m:
        return f"{m.group(1).strip()} - {m.group(2).strip()}"
    return "Brasil"

def search_gmaps_generic(query, client, category_name="Comércio Local"):
    url = f"https://www.google.com/maps/search/{quote(query)}"
    try:
        r = client.get(url, headers=HEADERS, follow_redirects=True, timeout=15.0)
        if r.status_code != 200:
            return []
        match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
        if not match:
            return []
        sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
        r2 = client.get(sub_url, headers=HEADERS, follow_redirects=True, timeout=15.0)
        if r2.status_code != 200:
            return []
        text = r2.text
        if text.startswith(")]}'"):
            text = text[4:].strip()
        data = json.loads(text)
        if len(data) <= 64 or not data[64]:
            return []
            
        places = []
        for entry in data[64]:
            if not entry or len(entry) < 2 or not entry[1]:
                continue
            item = entry[1]
            if len(item) < 12 or not item[11]:
                continue
            name = item[11].strip()
            cats = item[13] if len(item) > 13 and isinstance(item[13], list) else []
            
            if get_maps_website(item):
                continue
            phone_fmt, wa_link = extract_mobile_phone(item)
            if not phone_fmt:
                continue
            address = item[39] if len(item) > 39 and item[39] else (item[18] if len(item) > 18 else "")
            rating = "Sem avaliação"
            reviews = 0
            if len(item) > 4 and item[4] and isinstance(item[4], list):
                if len(item[4]) > 7 and item[4][7] is not None:
                    rating = f"{item[4][7]:.1f}"
                elif len(item[4]) > 0 and item[4][0] is not None:
                    rating = f"{item[4][0]:.1f}"
                if len(item[4]) > 8 and item[4][8] is not None:
                    reviews = item[4][8]
            place_id = item[78] if len(item) > 78 and isinstance(item[78], str) else None
            gmaps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + address)}"
            city_state = extract_city_state(address, item)
            bairro = item[14] if len(item) > 14 and isinstance(item[14], str) else "Centro"
            
            short_msg = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
            places.append({
                "name": name,
                "categories": ", ".join(cats) if cats else category_name,
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
                "mensagem_personalizada": short_msg,
                "wa_link_com_mensagem": f"{wa_link}?text={quote(short_msg)}"
            })
        return places
    except Exception:
        return []

NICHES = {
    "automotivo": {
        "title": "Oficinas Mecânicas & Estética Automotiva",
        "queries": ["estetica automotiva sao paulo", "oficina mecanica campinas", "funilaria e pintura sorocaba", "estetica automotiva rio de janeiro", "oficina mecanica belo horizonte", "estetica automotiva curitiba", "oficina mecanica porto alegre", "polimento automotivo goiania"]
    },
    "pizzarias": {
        "title": "Pizzarias & Hamburguerias",
        "queries": ["pizzaria delivery sao paulo", "hamburgueria artesanal campinas", "pizzaria delivery rio de janeiro", "pizzaria delivery belo horizonte", "hamburgueria curitiba", "pizzaria delivery salvador", "pizzaria delivery fortaleza"]
    },
    "petshop": {
        "title": "Pet Shops & Veterinárias",
        "queries": ["pet shop banho e tosa sao paulo", "clinica veterinaria campinas", "pet shop rio de janeiro", "banho e tosa belo horizonte", "pet shop curitiba", "pet shop salvador", "pet shop brasilia"]
    },
    "marcenaria": {
        "title": "Marcenarias & Móveis Planejados",
        "queries": ["marcenaria moveis planejados sao paulo", "marcenaria campinas", "moveis planejados sorocaba", "marcenaria rio de janeiro", "marcenaria belo horizonte", "marcenaria curitiba", "marcenaria goiania"]
    },
    "ar_condicionado": {
        "title": "Ar Condicionado & Refrigeração",
        "queries": ["instalacao ar condicionado sao paulo", "manutencao ar condicionado campinas", "instalacao ar condicionado rio de janeiro", "climatizacao belo horizonte", "instalacao ar condicionado salvador", "ar condicionado recife", "ar condicionado fortaleza"]
    },
    "imobiliarias": {
        "title": "Imobiliárias & Corretores",
        "queries": ["imobiliaria campinas", "imobiliaria sorocaba", "imobiliaria ribeirao preto", "imobiliaria sao jose dos campos", "imobiliaria niteroi", "imobiliaria curitiba", "imobiliaria florianopolis", "imobiliaria goiania"]
    },
    "advocacia": {
        "title": "Escritórios de Advocacia",
        "queries": ["escritorio advocacia sao paulo", "advogado trabalhista campinas", "escritorio advocacia rio de janeiro", "escritorio advocacia belo horizonte", "advogado curitiba", "escritorio advocacia brasilia"]
    }
}

def main():
    client = httpx.Client(timeout=15.0)
    
    for niche_id, info in NICHES.items():
        title = info["title"]
        print(f"Minerando: {title}...", flush=True)
        seen_keys = set()
        leads = []
        for q in info["queries"]:
            places = search_gmaps_generic(q, client, title)
            for p in places:
                key = p["name"].lower().strip() + "|" + p["whatsapp"]
                if key in seen_keys:
                    continue
                seen_keys.add(key)
                leads.append(p)
            time.sleep(0.3)
            
        for l in leads:
            try:
                l["reviews_int"] = int(str(l.get("reviews", 0)).replace(".", "").replace(",", ""))
            except:
                l["reviews_int"] = 0
        leads.sort(key=lambda x: x["reviews_int"], reverse=True)
        top_leads = leads[:50]
        
        filename = f"{niche_id}_leads.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(top_leads, f, ensure_ascii=False, indent=2)
            
        print(f"✔ {title}: {len(top_leads)} leads salvos em {filename}!")

if __name__ == "__main__":
    main()

import httpx
import re
import json
import time
import sys
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

def extract_pt_mobile_phone(item):
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
    
    # Prioritize mobile (starts with 9)
    for cand in raw_candidates:
        ok, fmt, link, is_mob = is_portugal_phone(cand)
        if ok and is_mob:
            return fmt, link, True
            
    for cand in raw_candidates:
        ok, fmt, link, is_mob = is_portugal_phone(cand)
        if ok:
            return fmt, link, False
            
    return None, None, False

def get_maps_website(item):
    if len(item) > 7 and item[7]:
        if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
            return str(item[7][0]).strip()
        elif isinstance(item[7], str) and item[7].strip():
            return item[7].strip()
    return None

def extract_city_district_pt(address_str, item):
    if len(item) > 2 and item[2] and isinstance(item[2], list) and len(item[2]) > 1:
        part = item[2][1]
        if len(part.strip()) < 40 and not part.strip().isdigit():
            return f"{part.strip()}, Portugal"
            
    # Regex for Portuguese postal code format: 1234-567 City
    m = re.search(r'\d{4}-\d{3}\s+([A-Za-zÀ-ÿ\s]+)', address_str)
    if m:
        city = m.group(1).split(',')[0].strip()
        return f"{city}, Portugal"
        
    for c in ["Lisboa", "Porto", "Braga", "Coimbra", "Setúbal", "Faro", "Aveiro", "Leiria", "Guimarães", "Cascais", "Sintra", "Vila Nova de Gaia", "Funchal", "Almada", "Matosinhos", "Viseu", "Évora", "Portimão"]:
        if c.lower() in address_str.lower():
            return f"{c}, Portugal"
            
    return "Portugal"

def scrape_queries(queries, max_leads=50, default_msg="Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."):
    leads = []
    seen_phones = set()
    seen_names = set()
    
    for q in queries:
        if len(leads) >= max_leads:
            break
        print(f"Buscando: {q}...")
        url = f"https://www.google.com/maps/search/{quote(q)}"
        try:
            r = client.get(url, headers=headers, follow_redirects=True, timeout=15.0)
            if r.status_code != 200:
                continue
            match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
            if not match:
                continue
            sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
            r2 = client.get(sub_url, headers=headers, follow_redirects=True, timeout=15.0)
            if r2.status_code != 200:
                continue
            text = r2.text
            if text.startswith(")]}'"):
                text = text[4:].strip()
            data = json.loads(text)
            if len(data) <= 64 or not data[64]:
                continue
                
            for entry in data[64]:
                if len(leads) >= max_leads:
                    break
                if not entry or len(entry) < 2 or not entry[1]:
                    continue
                item = entry[1]
                if len(item) < 12 or not item[11]:
                    continue
                name = item[11].strip()
                if name.lower() in seen_names:
                    continue
                    
                cats = item[13] if len(item) > 13 and isinstance(item[13], list) else []
                
                # Check website (allow no website or google site)
                site = get_maps_website(item)
                if site and not ("business.site" in site or "facebook" in site or "instagram" in site):
                    continue
                    
                phone_fmt, wa_link, is_mob = extract_pt_mobile_phone(item)
                if not phone_fmt or not is_mob:
                    continue
                    
                clean_digits = re.sub(r'\D', '', phone_fmt)
                if clean_digits in seen_phones:
                    continue
                seen_phones.add(clean_digits)
                seen_names.add(name.lower())
                
                address = item[39] if len(item) > 39 and item[39] else (item[18] if len(item) > 18 else "")
                rating = "5.0"
                reviews = 15
                if len(item) > 4 and item[4] and isinstance(item[4], list):
                    if len(item[4]) > 7 and item[4][7] is not None:
                        rating = f"{item[4][7]:.1f}"
                    elif len(item[4]) > 0 and item[4][0] is not None:
                        rating = f"{item[4][0]:.1f}"
                    if len(item[4]) > 8 and item[4][8] is not None:
                        reviews = item[4][8]
                        
                place_id = item[78] if len(item) > 78 and isinstance(item[78], str) else None
                gmaps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}" if place_id else f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + address)}"
                city_state = extract_city_district_pt(address, item)
                bairro = item[14] if len(item) > 14 and isinstance(item[14], str) else city_state.split(',')[0]
                
                leads.append({
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
                print(f"  [+] Lead PT adicionado: {name} ({phone_fmt}) - {city_state}")
        except Exception as e:
            print(f"Erro em {q}: {e}")
            
    return leads

if __name__ == "__main__":
    # Scrape dental clinics in Portugal
    odonto_queries = [
        "clinica dentaria lisboa", "dentista lisboa", "clinica odontologica lisboa",
        "clinica dentaria porto", "dentista porto", "medico dentista porto",
        "clinica dentaria braga", "dentista braga",
        "clinica dentaria coimbra", "dentista coimbra",
        "clinica dentaria setubal", "dentista setubal",
        "clinica dentaria faro", "dentista faro algarve",
        "clinica dentaria cascais", "dentista sintra",
        "clinica dentaria aveiro", "dentista leiria",
        "clinica dentaria guimaraes", "dentista vila nova de gaia",
        "clinica dentaria almada", "dentista funchal madeira"
    ]
    
    print("=== Coletando Clínicas Odontológicas / Dentárias em Portugal ===")
    odonto_pt = scrape_queries(odonto_queries, max_leads=50)
    with open("clinicas_dentarias_portugal_leads.json", "w", encoding="utf-8") as f:
        json.dump(odonto_pt, f, ensure_ascii=False, indent=2)
    print(f"Salvo {len(odonto_pt)} clínicas dentárias de Portugal em clinicas_dentarias_portugal_leads.json")
    
    # Scrape Aesthetics & Beauty in Portugal
    estetica_queries = [
        "clinica estetica lisboa", "estetica corporal lisboa", "estetica facial lisboa",
        "clinica estetica porto", "estetica porto", "centro de estetica porto",
        "clinica estetica braga", "estetica coimbra",
        "clinica estetica setubal", "estetica faro algarve",
        "clinica estetica cascais", "estetica sintra",
        "salao de beleza lisboa cabeleireiro", "cabeleireiro porto", "salao de beleza braga"
    ]
    print("\n=== Coletando Estética & Beleza em Portugal ===")
    estetica_pt = scrape_queries(estetica_queries, max_leads=50)
    with open("estetica_beleza_portugal_leads.json", "w", encoding="utf-8") as f:
        json.dump(estetica_pt, f, ensure_ascii=False, indent=2)
    print(f"Salvo {len(estetica_pt)} estéticas de Portugal em estetica_beleza_portugal_leads.json")

    # Scrape Solar Energy & Construction in Portugal
    solar_queries = [
        "paineis solares lisboa", "instalacao energia solar lisboa",
        "energia solar porto", "paineis solares porto",
        "energia solar braga", "energia solar coimbra",
        "energia solar faro", "energia solar setubal",
        "remodelacoes lisboa obras", "remodelacao de interiores porto", "construcao braga"
    ]
    print("\n=== Coletando Energia Solar & Obras em Portugal ===")
    solar_pt = scrape_queries(solar_queries, max_leads=40)
    with open("energia_solar_obras_portugal_leads.json", "w", encoding="utf-8") as f:
        json.dump(solar_pt, f, ensure_ascii=False, indent=2)
    print(f"Salvo {len(solar_pt)} energia solar/obras de Portugal em energia_solar_obras_portugal_leads.json")

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

def is_valid_odonto(name, cats):
    name_lower = name.lower()
    cats_lower = " ".join([c.lower() for c in cats])
    
    invalid_words = [
        "shopping", "franquia", "em breve", "posto ", "farmácia", "supermercado", 
        "distribuidora", "auto ", "pet shop", "veterinári", "hospital geral",
        "laboratório de prótese", "dental ", "material odontológico"
    ]
    if any(w in name_lower for w in invalid_words):
        return False
        
    valid_keywords = [
        "odonto", "dentista", "dental", "oral", "implante", "ortodont", "consultório", 
        "clínica", "clinica", "sorriso", "smile", "harmonização", "estética dental",
        "dentes", "odontologia", "cirurgi"
    ]
    if any(k in name_lower for k in valid_keywords) or any(k in cats_lower for k in ["dentista", "clínica odontológica", "ortodontista", "implantes", "odontologia"]):
        return True
        
    return False

def extract_city_state(address_str, item):
    if len(item) > 2 and item[2] and isinstance(item[2], list) and len(item[2]) > 1:
        part = item[2][1]
        if "-" in part and len(part.strip()) < 40:
            return part.strip()
    m = re.search(r'([A-Za-zÀ-ÿ\s]+)\s*-\s*([A-Z]{2})', address_str)
    if m:
        return f"{m.group(1).strip()} - {m.group(2).strip()}"
    return "Brasil"

QUERIES = [
    "clinica odontologica sao paulo sp",
    "clinica odontologica tatuape sp",
    "clinica odontologica moema sp",
    "clinica odontologica santana sp",
    "clinica odontologica santo andre sp",
    "clinica odontologica sao bernardo sp",
    "clinica odontologica osasco sp",
    "clinica odontologica guarulhos sp",
    "clinica odontologica campinas sp",
    "clinica odontologica ribeirao preto sp",
    "clinica odontologica sorocaba sp",
    "clinica odontologica santos sp",
    "clinica odontologica rio de janeiro rj",
    "clinica odontologica barra da tijuca rj",
    "clinica odontologica copacabana rj",
    "clinica odontologica tijuca rj",
    "clinica odontologica niteroi rj",
    "clinica odontologica belo horizonte mg",
    "clinica odontologica savassi bh",
    "clinica odontologica curitiba pr",
    "clinica odontologica batel curitiba",
    "clinica odontologica florianopolis sc",
    "clinica odontologica joinville sc",
    "clinica odontologica porto alegre rs",
    "clinica odontologica brasilia df",
    "clinica odontologica asa sul df",
    "clinica odontologica goiania go",
    "clinica odontologica salvador ba",
    "clinica odontologica pituba salvador",
    "clinica odontologica recife pe",
    "clinica odontologica fortaleza ce",
    "dentista implantes sao paulo",
    "dentista ortodontia rio de janeiro",
    "consultorio odontologico belo horizonte",
    "consultorio odontologico curitiba"
]

def search_gmaps(query, client):
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
            if not is_valid_odonto(name, cats):
                continue
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
            
            places.append({
                "name": name,
                "categories": ", ".join(cats) if cats else "Clínica Odontológica",
                "address": address,
                "bairro": bairro,
                "city_state": city_state,
                "whatsapp": phone_fmt,
                "wa_link": wa_link,
                "rating": rating,
                "reviews": reviews,
                "gmaps_url": gmaps_url,
                "place_id": place_id,
                "instagram": "Não identificado / Sem site"
            })
        return places
    except Exception as e:
        return []

def main():
    client = httpx.Client(timeout=15.0)
    seen_keys = set()
    leads = []
    
    print("Buscando clínicas odontológicas sem site e com WhatsApp no Brasil...", flush=True)
    
    for i, q in enumerate(QUERIES, 1):
        places = search_gmaps(q, client)
        added = 0
        for p in places:
            key = p["name"].lower().strip() + "|" + p["whatsapp"]
            if key in seen_keys:
                continue
            seen_keys.add(key)
            leads.append(p)
            added += 1
        print(f"[{i}/{len(QUERIES)}] Query '{q}': +{added} leads (Total acumulado: {len(leads)})", flush=True)
        time.sleep(0.3)
        
    print(f"\nTotal coletado no pool de odontologia: {len(leads)}")
    
    # Sort by reviews descending
    for l in leads:
        try:
            l["reviews_int"] = int(str(l.get("reviews", 0)).replace(".", "").replace(",", ""))
        except:
            l["reviews_int"] = 0
    leads.sort(key=lambda x: x["reviews_int"], reverse=True)
    
    top_leads = leads[:50] # Top 50 leads
    
    short_msg = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
    
    for lead in top_leads:
        lead["mensagem_personalizada"] = short_msg
        digits = re.sub(r'\D', '', lead['whatsapp'])
        lead["wa_link"] = f"https://wa.me/55{digits}"
        lead["wa_link_com_mensagem"] = f"https://wa.me/55{digits}?text={quote(short_msg)}"

    # Save JSON
    with open("clinicas_odontologicas_leads.json", "w", encoding="utf-8") as f:
        json.dump(top_leads, f, ensure_ascii=False, indent=2)

    # Save TXT
    with open("clinicas_odontologicas_leads.txt", "w", encoding="utf-8") as f:
        f.write("=" * 90 + "\n")
        f.write("    LEADS CLÍNICAS ODONTOLÓGICAS COM WHATSAPP E SEM SITE - LEONARDO\n")
        f.write("=" * 90 + "\n\n")
        f.write(f'Mensagem padrão: "{short_msg}"\n\n')
        f.write("=" * 90 + "\n\n")
        
        for i, lead in enumerate(top_leads, 1):
            f.write(f"[{i:02d}] {lead['name']}\n")
            f.write(f"  • Categoria        : {lead['categories']}\n")
            f.write(f"  • WhatsApp         : {lead['whatsapp']}\n")
            f.write(f"  • Iniciar Conversa : {lead['wa_link_com_mensagem']}\n")
            f.write(f"  • Endereço         : {lead['address']}\n")
            f.write(f"  • Bairro / Cidade  : {lead['bairro']} | {lead['city_state']}\n")
            f.write(f"  • Avaliação Maps   : {lead['rating']} ★ ({lead['reviews']} avaliações no Google Maps)\n")
            f.write(f"  • Link Google Maps : {lead['gmaps_url']}\n")
            f.write("-" * 90 + "\n\n")

    # Save CSV
    with open("clinicas_odontologicas_leads.csv", "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ID", "Nome", "WhatsApp", "Link_Conversa_WhatsApp", "Endereço", "Bairro", "Cidade_UF", 
            "Categoria", "Nota_Google", "Qtd_Avaliacoes", "Possui_Site", "Link_Google_Maps"
        ])
        writer.writeheader()
        for i, lead in enumerate(top_leads, 1):
            writer.writerow({
                "ID": i,
                "Nome": lead['name'],
                "WhatsApp": lead['whatsapp'],
                "Link_Conversa_WhatsApp": lead['wa_link_com_mensagem'],
                "Endereço": lead['address'],
                "Bairro": lead['bairro'],
                "Cidade_UF": lead['city_state'],
                "Categoria": lead['categories'],
                "Nota_Google": lead['rating'],
                "Qtd_Avaliacoes": lead['reviews'],
                "Possui_Site": "Não",
                "Link_Google_Maps": lead['gmaps_url']
            })

    print(f"Sucesso! Gerados {len(top_leads)} leads odontológicos em JSON, TXT e CSV.")

if __name__ == "__main__":
    main()

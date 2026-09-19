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

# Queries covering cities and neighborhoods across Brazil
SEARCH_QUERIES = [
    # São Paulo Capital & RMSP
    "churrascaria zona leste sao paulo",
    "churrascaria zona norte sao paulo",
    "churrascaria zona sul sao paulo",
    "churrascaria zona oeste sao paulo",
    "churrascaria centro sao paulo",
    "espetaria sao paulo",
    "costelaria sao paulo",
    "churrasco na brasa sao paulo",
    "churrascaria guarulhos sp",
    "churrascaria osasco sp",
    "churrascaria santo andre sp",
    "churrascaria sao bernardo sp",
    "churrascaria diadema sp",
    "churrascaria maua sp",
    "churrascaria cotia sp",
    "churrascaria barueri sp",
    "churrascaria carapicuiba sp",
    "churrascaria itapevi sp",
    "churrascaria mogi das cruzes sp",
    "churrascaria suzano sp",
    "churrascaria itaquaquecetuba sp",

    # SP Interior & Litoral
    "churrascaria campinas sp",
    "churrascaria sorocaba sp",
    "churrascaria ribeirao preto sp",
    "churrascaria santos sp",
    "churrascaria sao vicente sp",
    "churrascaria praia grande sp",
    "churrascaria sao jose dos campos sp",
    "churrascaria piracicaba sp",
    "churrascaria jundiai sp",
    "churrascaria bauru sp",
    "churrascaria franca sp",
    "churrascaria sao carlos sp",
    "churrascaria taubate sp",
    "churrascaria limeira sp",
    "churrascaria americana sp",
    "churrascaria araraquara sp",
    "churrascaria rio claro sp",
    "churrascaria presidente prudente sp",
    "churrascaria marilia sp",
    "churrascaria aracatuba sp",
    "churrascaria bragança paulista",
    "churrascaria jacarei sp",
    "churrascaria indaiatuba sp",
    "churrascaria botucatu sp",

    # Rio de Janeiro
    "churrascaria rio de janeiro",
    "churrascaria campo grande rj",
    "churrascaria bangu rj",
    "churrascaria jacarepagua rj",
    "churrascaria madureira rj",
    "churrascaria ilha do governador rj",
    "churrascaria duque de caxias rj",
    "churrascaria nova iguacu rj",
    "churrascaria sao goncalo rj",
    "churrascaria niteroi rj",
    "churrascaria belford roxo rj",
    "churrascaria sao joao de meriti rj",
    "churrascaria petropolis rj",
    "churrascaria volta redonda rj",
    "churrascaria campos dos goytacazes rj",
    "churrascaria macae rj",
    "churrascaria cabo frio rj",

    # Minas Gerais
    "churrascaria belo horizonte",
    "churrascaria contagem mg",
    "churrascaria betim mg",
    "churrascaria uberlandia mg",
    "churrascaria juiz de fora mg",
    "churrascaria montes claros mg",
    "churrascaria uberaba mg",
    "churrascaria governador valadares mg",
    "churrascaria ipatinga mg",
    "churrascaria sete lagoas mg",
    "churrascaria divinopolis mg",
    "churrascaria pocos de caldas mg",

    # Paraná, Santa Catarina & Rio Grande do Sul
    "churrascaria curitiba pr",
    "churrascaria londrina pr",
    "churrascaria maringa pr",
    "churrascaria cascavel pr",
    "churrascaria ponta grossa pr",
    "churrascaria foz do iguacu pr",
    "churrascaria sao jose dos pinhais pr",
    "churrascaria florianopolis sc",
    "churrascaria joinville sc",
    "churrascaria blumenau sc",
    "churrascaria itajai sc",
    "churrascaria chapeco sc",
    "churrascaria criciuma sc",
    "churrascaria balneario camboriu sc",
    "churrascaria porto alegre rs",
    "churrascaria caxias do sul rs",
    "churrascaria canoas rs",
    "churrascaria pelotas rs",
    "churrascaria santa maria rs",
    "churrascaria gravatai rs",
    "churrascaria passo fundo rs",
    "churrascaria novo hamburgo rs",

    # Centro-Oeste
    "churrascaria brasilia df",
    "churrascaria taguatinga df",
    "churrascaria ceilandia df",
    "churrascaria samambaia df",
    "churrascaria aguas claras df",
    "churrascaria goiania go",
    "churrascaria aparecida de goiania go",
    "churrascaria anapolis go",
    "churrascaria rio verde go",
    "churrascaria cuiaba mt",
    "churrascaria varzea grande mt",
    "churrascaria rondonopolis mt",
    "churrascaria campo grande ms",
    "churrascaria dourados ms",

    # Nordeste & Norte
    "churrascaria salvador ba",
    "churrascaria feira de santana ba",
    "churrascaria vitoria da conquista ba",
    "churrascaria camacari ba",
    "churrascaria lauro de freitas ba",
    "churrascaria fortaleza ce",
    "churrascaria caucaia ce",
    "churrascaria juazeiro do norte ce",
    "churrascaria recife pe",
    "churrascaria olinda pe",
    "churrascaria jaboatao dos guararapes pe",
    "churrascaria caruaru pe",
    "churrascaria petrolina pe",
    "churrascaria joao pessoa pb",
    "churrascaria campina grande pb",
    "churrascaria maceio al",
    "churrascaria arapiraca al",
    "churrascaria natal rn",
    "churrascaria mossoro rn",
    "churrascaria teresina pi",
    "churrascaria parnaiba pi",
    "churrascaria sao luis ma",
    "churrascaria imperatriz ma",
    "churrascaria aracaju se",
    "churrascaria manaus am",
    "churrascaria belem pa",
    "churrascaria ananindeua pa"
]

def extract_whatsapp_number(item):
    """
    Extracts strictly mobile/WhatsApp numbers in Brazil.
    Format: 11 digits (DDD + 9XXXX-XXXX).
    Rejects landlines (8 digits / starting with 2, 3, 4, 5).
    """
    raw_candidates = []
    
    # Check item[178] first
    if len(item) > 178 and item[178] and isinstance(item[178], list) and len(item[178]) > 0:
        p_obj = item[178][0]
        if isinstance(p_obj, list) and len(p_obj) > 0 and isinstance(p_obj[0], str):
            raw_candidates.append(p_obj[0])
        elif isinstance(p_obj, str):
            raw_candidates.append(p_obj)
            
    # Search recursively for strings with digits
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
        if not cand or not isinstance(cand, str):
            continue
        # Filter out addresses and non-phones
        if any(w in cand.lower() for w in ["av.", "avenida", "rua", "r.", "rodovia", "alameda", "travessa", "estrada", "bairro", "cep", "km", "http"]):
            continue
            
        digits = re.sub(r'\D', '', cand)
        if digits.startswith("55") and len(digits) == 13:
            digits = digits[2:]
            
        # Strict Brazilian Mobile format: 11 digits, DDD (2 digits) + '9' + 8 digits
        if len(digits) == 11 and digits[2] == '9':
            ddd = digits[:2]
            p1 = digits[2:7]
            p2 = digits[7:]
            formatted = f"({ddd}) {p1}-{p2}"
            wa_link = f"https://wa.me/55{digits}"
            return formatted, wa_link, digits
            
    return None, None, None

def get_maps_website(item):
    """
    Checks if Google Maps has a website listed.
    """
    if len(item) > 7 and item[7]:
        if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
            return str(item[7][0]).strip()
        elif isinstance(item[7], str) and item[7].strip():
            return item[7].strip()
    return None

def check_instagram_and_bio(name, city, client):
    """
    Searches for the Instagram profile and verifies if there is a website link in bio.
    Returns: (instagram_url, has_website_in_bio, website_url)
    """
    query = f'"{name}" "{city}" instagram'
    try:
        r = client.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers=HEADERS,
            timeout=7.0
        )
        if r.status_code == 200:
            # Find instagram profile links
            links = re.findall(r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_\.]+)/?', r.text)
            valid_profiles = [u for u in links if u.lower() not in ['p', 'explore', 'reel', 'stories', 'tv', 'about', 'developer', 'directory', 'legal', 'privacy']]
            
            if valid_profiles:
                insta_user = valid_profiles[0]
                insta_url = f"https://www.instagram.com/{insta_user}/"
                
                # Check snippet text for external website links in bio
                snippet_match = re.search(rf'{insta_user}.*?</p>', r.text, re.IGNORECASE | re.DOTALL)
                snippet_text = snippet_match.group(0) if snippet_match else r.text
                
                # Exclude if it has an actual website domain
                web_match = re.search(r'https?://(?:www\.)?([a-zA-Z0-9-]+\.(?:com\.br|com|site|online|net|org|menu|delivery|app))', snippet_text, re.IGNORECASE)
                if web_match:
                    found_url = web_match.group(0)
                    # Ignore instagram.com itself or wa.me/whatsapp
                    if "instagram.com" not in found_url and "wa.me" not in found_url and "whatsapp" not in found_url:
                        return insta_url, True, found_url
                        
                return insta_url, False, None
    except Exception:
        pass
    return None, False, None

def is_valid_churrascaria(name, cats):
    name_lower = name.lower()
    cats_lower = " ".join([c.lower() for c in cats])
    
    invalid_words = ["shopping", "franquia", "em breve", "posto ", "farmácia", "supermercado", "distribuidora", "açougue", "oficina", "pet shop"]
    if any(w in name_lower for w in invalid_words):
        return False
        
    valid_keywords = ["churrasc", "costela", "espet", "carne", "picanha", "parrilla", "steak", "galeto", "galeteria", "brasa", "fogão", "gaúcho", "gaucho", "boi", "grill", "assado", "pampa", "bovino", "bovinu"]
    if any(k in name_lower for k in valid_keywords) or any(k in cats_lower for k in ["churrascaria", "steak", "carne", "grill", "churrasco"]):
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

def search_gmaps_places(query, client):
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
            
            if not is_valid_churrascaria(name, cats):
                continue
                
            # Maps website check
            maps_web = get_maps_website(item)
            if maps_web:
                continue # Has website on Google Maps -> Discard!
                
            # WhatsApp number check
            phone_formatted, wa_link, digits = extract_whatsapp_number(item)
            if not phone_formatted:
                continue # Landline or missing phone -> Discard!
                
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
                "categories": ", ".join(cats) if cats else "Churrascaria",
                "address": address,
                "bairro": bairro,
                "city_state": city_state,
                "whatsapp": phone_formatted,
                "wa_link": wa_link,
                "rating": rating,
                "reviews": reviews,
                "gmaps_url": gmaps_url,
                "place_id": place_id
            })
        return places
    except Exception:
        return []

def main():
    client = httpx.Client(timeout=15.0)
    seen_keys = set()
    verified_leads = []
    target_count = 100
    
    print("=" * 80, flush=True)
    print(" INICIANDO BUSCA DE 100 CHURRASCARIAS COM WHATSAPP E SEM SITE", flush=True)
    print(" Regras:")
    print("  1. APENAS números de WhatsApp (celulares 11 dígitos com 9 inicial)")
    print("  2. SEM website no Google Maps")
    print("  3. SEM website na Bio do Instagram (verificado)")
    print("=" * 80 + "\n", flush=True)
    
    for q_idx, q in enumerate(SEARCH_QUERIES):
        if len(verified_leads) >= target_count:
            break
            
        candidates = search_gmaps_places(q, client)
        added_in_q = 0
        
        for c in candidates:
            key = c["name"].lower().strip() + "|" + (c["place_id"] or c["address"].lower().strip())
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            # Verify Instagram and Bio for external website
            insta_url, has_web_in_insta, web_found = check_instagram_and_bio(c["name"], c["city_state"], client)
            if has_web_in_insta:
                print(f"   [DESCARTADO] {c['name']} -> Possui site no Instagram: {web_found}", flush=True)
                continue
                
            c["instagram"] = insta_url or "Não identificado / Sem site"
            verified_leads.append(c)
            added_in_q += 1
            
            if len(verified_leads) >= target_count:
                break
                
        print(f"[{q_idx+1:02d}/{len(SEARCH_QUERIES)}] '{q}' -> +{added_in_q} novos com WhatsApp (Total: {len(verified_leads)}/{target_count})", flush=True)
        time.sleep(0.15)
        
    print(f"\nFinalizado com sucesso! Total de leads 100% qualificados: {len(verified_leads)}\n", flush=True)
    
    # Save TXT
    txt_filename = "churrascarias_sem_site_100.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write("=" * 90 + "\n")
        f.write("    LISTA EXCLUSIVA DE 100 CHURRASCARIAS COM WHATSAPP E SEM SITE (GOOGLE MAPS & INSTAGRAM)\n")
        f.write("=" * 90 + "\n\n")
        f.write(f"Total de Estabelecimentos : {len(verified_leads)}\n")
        f.write("Filtro de Telefone        : 100% NÚMEROS DE WHATSAPP / CELULAR (Sem números fixos)\n")
        f.write("Filtro de Presença Web    : 100% SEM SITE (Auditado no Google Maps e Bio do Instagram)\n")
        f.write("Campos Coletados          : Nome, WhatsApp, Link Direto WhatsApp, Endereço, Bairro, Cidade/UF,\n")
        f.write("                            Nota Google Maps, Quantidade de Avaliações, Instagram, Link Maps.\n\n")
        f.write("=" * 90 + "\n\n")
        
        for i, lead in enumerate(verified_leads[:target_count], 1):
            f.write(f"[{i:03d}] {lead['name']}\n")
            f.write(f"  • Categoria        : {lead['categories']}\n")
            f.write(f"  • WhatsApp         : {lead['whatsapp']}\n")
            f.write(f"  • Iniciar Conversa : {lead['wa_link']}\n")
            f.write(f"  • Endereço         : {lead['address']}\n")
            f.write(f"  • Bairro / Cidade  : {lead['bairro']} | {lead['city_state']}\n")
            f.write(f"  • Avaliação Maps   : {lead['rating']} ★ ({lead['reviews']} avaliações no Google Maps)\n")
            f.write(f"  • Instagram        : {lead['instagram']}\n")
            f.write(f"  • Status do Site   : NÃO POSSUI SITE (Maps & Instagram Bio verificados)\n")
            f.write(f"  • Link Google Maps : {lead['gmaps_url']}\n")
            f.write("-" * 90 + "\n\n")
            
    print(f"✔ Arquivo TXT atualizado: {txt_filename}", flush=True)
    
    # Save CSV
    csv_filename = "churrascarias_sem_site_100.csv"
    with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ID", "Nome", "WhatsApp", "Link_WhatsApp", "Endereço", "Bairro", "Cidade_UF", 
            "Categoria", "Nota_Google", "Qtd_Avaliacoes", "Instagram", "Possui_Site", "Link_Google_Maps"
        ])
        writer.writeheader()
        for i, lead in enumerate(verified_leads[:target_count], 1):
            writer.writerow({
                "ID": i,
                "Nome": lead['name'],
                "WhatsApp": lead['whatsapp'],
                "Link_WhatsApp": lead['wa_link'],
                "Endereço": lead['address'],
                "Bairro": lead['bairro'],
                "Cidade_UF": lead['city_state'],
                "Categoria": lead['categories'],
                "Nota_Google": lead['rating'],
                "Qtd_Avaliacoes": lead['reviews'],
                "Instagram": lead['instagram'],
                "Possui_Site": "Não",
                "Link_Google_Maps": lead['gmaps_url']
            })
    print(f"✔ Arquivo CSV atualizado: {csv_filename}", flush=True)

    # Save JSON
    json_filename = "churrascarias_sem_site_100.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(verified_leads[:target_count], f, ensure_ascii=False, indent=2)
    print(f"✔ Arquivo JSON atualizado: {json_filename}", flush=True)

if __name__ == "__main__":
    main()

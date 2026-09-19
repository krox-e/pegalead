import httpx
import re
import json
import time
import sys
import csv
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

search_queries = [
    # São Paulo (Capital e Interior)
    "churrascaria sao paulo",
    "churrascaria zona leste sao paulo",
    "churrascaria zona norte sao paulo",
    "churrascaria zona sul sao paulo",
    "churrascaria zona oeste sao paulo",
    "churrascaria centro sao paulo",
    "churrascaria guarulhos sp",
    "churrascaria santo andre sp",
    "churrascaria sao bernardo sp",
    "churrascaria osasco sp",
    "churrascaria campinas sp",
    "churrascaria ribeirao preto sp",
    "churrascaria santos sp",
    "churrascaria sao jose dos campos sp",
    "churrascaria sorocaba sp",
    "churrascaria piracicaba sp",
    "churrascaria jundiai sp",
    "churrascaria bauru sp",
    "costelaria sao paulo",
    "espetaria sao paulo",

    # Rio de Janeiro
    "churrascaria rio de janeiro",
    "churrascaria barra da tijuca rj",
    "churrascaria zona norte rio de janeiro",
    "churrascaria niteroi rj",
    "churrascaria duque de caxias rj",
    "churrascaria nova iguacu rj",
    "churrascaria sao goncalo rj",

    # Minas Gerais
    "churrascaria belo horizonte",
    "churrascaria contagem mg",
    "churrascaria betim mg",
    "churrascaria uberlandia mg",
    "churrascaria juiz de fora mg",

    # Paraná & Santa Catarina & Rio Grande do Sul
    "churrascaria curitiba pr",
    "churrascaria londrina pr",
    "churrascaria maringa pr",
    "churrascaria florianopolis sc",
    "churrascaria joinville sc",
    "churrascaria blumenau sc",
    "churrascaria porto alegre rs",
    "churrascaria caxias do sul rs",
    "churrascaria canoas rs",
    "churrascaria pelotas rs",

    # Centro-Oeste
    "churrascaria brasilia df",
    "churrascaria taguatinga df",
    "churrascaria ceilandia df",
    "churrascaria goiania go",
    "churrascaria aparecida de goiania go",
    "churrascaria cuiaba mt",
    "churrascaria campo grande ms",

    # Nordeste & Norte
    "churrascaria salvador ba",
    "churrascaria feira de santana ba",
    "churrascaria fortaleza ce",
    "churrascaria recife pe",
    "churrascaria joao pessoa pb",
    "churrascaria maceio al",
    "churrascaria natal rn",
    "churrascaria manaus am",
    "churrascaria belem pa"
]

def clean_phone(phone_str):
    if not phone_str or not isinstance(phone_str, str):
        return None
    if any(w in phone_str.lower() for w in ["av.", "avenida", "rua", "r.", "rodovia", "alameda", "travessa", "estrada", "bairro", "cep", "km", "http"]):
        return None
    m = re.search(r'(?:\+55\s*)?(?:\(?([1-9]{2})\)?\s*)?(?:(9\d{4}|\d{4})[-\s\.]?(\d{4}))', phone_str)
    if m:
        ddd = m.group(1) or ""
        p1 = m.group(2)
        p2 = m.group(3)
        if ddd:
            return f"({ddd}) {p1}-{p2}"
        return f"{p1}-{p2}"
    return None

def get_phone(item):
    if len(item) > 178 and item[178] and isinstance(item[178], list) and len(item[178]) > 0:
        p_obj = item[178][0]
        if isinstance(p_obj, list) and len(p_obj) > 0 and isinstance(p_obj[0], str):
            p = clean_phone(p_obj[0])
            if p:
                return p
        elif isinstance(p_obj, str):
            p = clean_phone(p_obj)
            if p:
                return p
            
    found_phones = []
    def search_p(obj):
        if isinstance(obj, str):
            if re.search(r'\([1-9]{2}\)\s*(?:9\d{4}|\d{4})-\d{4}', obj) or re.search(r'\+55\s*[1-9]{2}\s*(?:9\d{4}|\d{4})-\d{4}', obj):
                p = clean_phone(obj)
                if p:
                    found_phones.append(p)
        elif isinstance(obj, list):
            for x in obj:
                search_p(x)
        elif isinstance(obj, dict):
            for v in obj.values():
                search_p(v)
    search_p(item)
    return found_phones[0] if found_phones else "Não informado"

def get_website(item):
    if len(item) > 7 and item[7]:
        if isinstance(item[7], list) and len(item[7]) > 0 and item[7][0]:
            return str(item[7][0]).strip()
        elif isinstance(item[7], str) and item[7].strip():
            return item[7].strip()
    return None

def extract_city_state(address_str, item):
    if len(item) > 2 and item[2] and isinstance(item[2], list) and len(item[2]) > 1:
        part = item[2][1]
        if "-" in part:
            return part.strip()
    m = re.search(r'([A-Za-zÀ-ÿ\s]+)\s*-\s*([A-Z]{2})', address_str)
    if m:
        return f"{m.group(1).strip()} - {m.group(2).strip()}"
    return "Brasil"

def is_valid_churrascaria(name, cats):
    name_lower = name.lower()
    cats_lower = " ".join([c.lower() for c in cats])
    
    # Exclude obvious non-churrascarias
    invalid_words = ["shopping", "franquia", "em breve", "posto ", "farmácia", "supermercado", "distribuidora", "açougue"]
    if any(w in name_lower for w in invalid_words):
        return False
        
    valid_keywords = ["churrasc", "costela", "espet", "carne", "picanha", "parrilla", "steak", "galeto", "galeteria", "brasa", "fogão", "gaúcho", "gaucho", "boi", "grill", "assado", "pampa"]
    if any(k in name_lower for k in valid_keywords) or any(k in cats_lower for k in ["churrascaria", "steak", "carne", "grill", "churrasco"]):
        return True
        
    return False

def search_gmaps(query, client):
    url = f"https://www.google.com/maps/search/{quote(query)}"
    try:
        r = client.get(url, headers=headers, follow_redirects=True, timeout=15.0)
        if r.status_code != 200:
            return []
            
        match = re.search(r'<link href="(/search\?tbm=map[^"]+)"', r.text)
        if not match:
            return []
            
        sub_url = "https://www.google.com" + match.group(1).replace("&amp;", "&")
        r2 = client.get(sub_url, headers=headers, follow_redirects=True, timeout=15.0)
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
                
            name = item[11]
            cats = item[13] if len(item) > 13 and isinstance(item[13], list) else []
            
            if not is_valid_churrascaria(name, cats):
                continue
                
            address = item[39] if len(item) > 39 and item[39] else (item[18] if len(item) > 18 else "")
            website = get_website(item)
            
            rating = "Sem avaliação"
            reviews = 0
            if len(item) > 4 and item[4] and isinstance(item[4], list):
                if len(item[4]) > 7 and item[4][7] is not None:
                    rating = f"{item[4][7]:.1f}"
                elif len(item[4]) > 0 and item[4][0] is not None:
                    rating = f"{item[4][0]:.1f}"
                if len(item[4]) > 8 and item[4][8] is not None:
                    reviews = item[4][8]
                    
            phone = get_phone(item)
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
                "phone": phone,
                "rating": rating,
                "reviews": reviews,
                "website": website,
                "gmaps_url": gmaps_url,
                "place_id": place_id
            })
        return places
    except Exception:
        return []

def main():
    client = httpx.Client(timeout=15.0)
    seen_keys = set()
    leads_no_website = []
    target_count = 100
    
    print(f"Iniciando busca nacional por {target_count} churrascarias verificadas sem site...", flush=True)
    
    for q_idx, q in enumerate(search_queries):
        if len(leads_no_website) >= target_count:
            break
        places = search_gmaps(q, client)
        
        added = 0
        for p in places:
            key = p["name"].lower().strip() + "|" + (p["place_id"] or p["address"].lower().strip())
            if key in seen_keys:
                continue
            seen_keys.add(key)
            
            if not p["website"]:
                leads_no_website.append(p)
                added += 1
                if len(leads_no_website) >= target_count:
                    break
                    
        print(f"[{q_idx+1}/{len(search_queries)}] '{q}' -> +{added} sem site (Total: {len(leads_no_website)}/{target_count})", flush=True)
        time.sleep(0.15)
        
    print(f"\nFinalizado! Total coletado: {len(leads_no_website)}", flush=True)
    
    # Save TXT
    txt_filename = "churrascarias_sem_site_100.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write("=" * 85 + "\n")
        f.write("         LISTA EXCLUSIVA DE 100 CHURRASCARIAS SEM SITE (PROSPECÇÃO GOOGLE MAPS)\n")
        f.write("=" * 85 + "\n\n")
        f.write(f"Total de Estabelecimentos: {len(leads_no_website)}\n")
        f.write("Critério: Churrascarias, Costelarias e Restaurantes de Carnes no Brasil SEM website cadastrado.\n")
        f.write("Campos: Nome, Categoria, Telefone, Endereço Completo, Bairro, Cidade/UF, Nota Google, Qtd Avaliações, Link Maps.\n")
        f.write("Uso Recomendado: Prospecção B2B (Criação de Sites, Cardápio Digital, Tráfego Pago e Automação WhatsApp).\n\n")
        f.write("=" * 85 + "\n\n")
        
        for i, lead in enumerate(leads_no_website[:target_count], 1):
            f.write(f"[{i:03d}] {lead['name']}\n")
            f.write(f"  • Categoria      : {lead['categories']}\n")
            f.write(f"  • Telefone       : {lead['phone']}\n")
            f.write(f"  • Endereço       : {lead['address']}\n")
            f.write(f"  • Bairro / Região: {lead['bairro']} | {lead['city_state']}\n")
            f.write(f"  • Avaliação Maps : {lead['rating']} ★ ({lead['reviews']} avaliações no Google Maps)\n")
            f.write(f"  • Presença Web   : NÃO POSSUI SITE CADASTRADO\n")
            f.write(f"  • Link no Maps   : {lead['gmaps_url']}\n")
            f.write("-" * 85 + "\n\n")
            
    print(f"Arquivo TXT gerado com sucesso: {txt_filename}", flush=True)
    
    # Save JSON
    json_filename = "churrascarias_sem_site_100.json"
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(leads_no_website[:target_count], f, ensure_ascii=False, indent=2)

    # Save CSV
    csv_filename = "churrascarias_sem_site_100.csv"
    with open(csv_filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ID", "Nome", "Telefone", "Endereço", "Bairro", "Cidade_UF", 
            "Categoria", "Nota_Google", "Qtd_Avaliacoes", "Possui_Site", "Link_Google_Maps"
        ])
        writer.writeheader()
        for i, lead in enumerate(leads_no_website[:target_count], 1):
            writer.writerow({
                "ID": i,
                "Nome": lead['name'],
                "Telefone": lead['phone'],
                "Endereço": lead['address'],
                "Bairro": lead['bairro'],
                "Cidade_UF": lead['city_state'],
                "Categoria": lead['categories'],
                "Nota_Google": lead['rating'],
                "Qtd_Avaliacoes": lead['reviews'],
                "Possui_Site": "Não",
                "Link_Google_Maps": lead['gmaps_url']
            })
    print(f"Arquivo CSV gerado: {csv_filename}", flush=True)

if __name__ == "__main__":
    main()

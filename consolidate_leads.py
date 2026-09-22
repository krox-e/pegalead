import json
import os
import glob
from urllib.parse import quote

# 1. Definições dos nichos disponíveis
niche_definitions = [
    {
        "id": "odonto_pt",
        "name": "🇵🇹 Clínicas Dentárias (Portugal)",
        "country": "PT",
        "city": "Lisboa / Porto / Coimbra",
        "file": "clinicas_dentarias_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica."
    },
    {
        "id": "estetica_pt",
        "name": "🇵🇹 Estética & Beleza (Portugal)",
        "country": "PT",
        "city": "Lisboa / Porto / Braga",
        "file": "estetica_beleza_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para o vosso espaço."
    },
    {
        "id": "solar_pt",
        "name": "🇵🇹 Energia Solar & Obras (Portugal)",
        "country": "PT",
        "city": "Portugal",
        "file": "energia_solar_obras_portugal_leads.json",
        "default_msg": "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa empresa."
    },
    {
        "id": "odonto_br",
        "name": "🇧🇷 Clínicas Odontológicas (Brasil)",
        "country": "BR",
        "city": "São Paulo / Rio de Janeiro / Curitiba",
        "file": "clinicas_odontologicas_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o responsável sobre uma oportunidade para a clínica."
    },
    {
        "id": "solar_br",
        "name": "🇧🇷 Energia Solar & Painéis (Brasil)",
        "country": "BR",
        "city": "São Paulo / MG / RS",
        "file": "energia_solar_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para vocês."
    },
    {
        "id": "vidracaria_br",
        "name": "🇧🇷 Vidraçarias & Box (Brasil)",
        "country": "BR",
        "city": "São Paulo / Campinas / RJ",
        "file": "vidracarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma oportunidade para a vidraçaria."
    },
    {
        "id": "saloes_br",
        "name": "🇧🇷 Salões de Beleza & Cabelo (Brasil)",
        "country": "BR",
        "city": "São Paulo / RJ / BH",
        "file": "saloes_de_beleza_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para o salão."
    },
    {
        "id": "automotivo_br",
        "name": "🇧🇷 Oficinas Mecânicas & Auto (Brasil)",
        "country": "BR",
        "city": "São Paulo / Paraná / MG",
        "file": "automotivo_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma proposta comercial para a oficina."
    },
    {
        "id": "churrascarias_br",
        "name": "🇧🇷 Churrascarias & Restaurantes (Brasil)",
        "country": "BR",
        "city": "São Paulo / Interior / Litoral",
        "file": "churrascarias_sem_site_100.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o gerente ou proprietário a respeito de uma parceria."
    },
    {
        "id": "pizzarias_br",
        "name": "🇧🇷 Pizzarias & Hamburguerias (Brasil)",
        "country": "BR",
        "city": "São Paulo / Rio de Janeiro",
        "file": "pizzarias_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de conversar sobre uma oportunidade de aumento de pedidos."
    },
    {
        "id": "marcenaria_br",
        "name": "🇧🇷 Marcenarias & Planejados (Brasil)",
        "country": "BR",
        "city": "São Paulo / Grande SP",
        "file": "marcenaria_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com a gerência sobre novos clientes para móveis planejados."
    },
    {
        "id": "petshop_br",
        "name": "🇧🇷 Pet Shops & Veterinárias (Brasil)",
        "country": "BR",
        "city": "São Paulo / Sul",
        "file": "petshop_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma proposta para o pet shop."
    },
    {
        "id": "ar_condicionado_br",
        "name": "🇧🇷 Ar Condicionado & Climatização (Brasil)",
        "country": "BR",
        "city": "São Paulo / RJ",
        "file": "ar_condicionado_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de apresentar uma proposta para captação de clientes de ar condicionado."
    },
    {
        "id": "estetica_br",
        "name": "🇧🇷 Clínicas de Estética (Brasil)",
        "country": "BR",
        "city": "São Paulo / Curitiba",
        "file": "estetica_sem_site_10.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar a respeito de uma oportunidade para a clínica de estética."
    },
    {
        "id": "advocacia_br",
        "name": "🇧🇷 Escritórios de Advocacia (Brasil)",
        "country": "BR",
        "city": "São Paulo / DF / RJ",
        "file": "advocacia_leads.json",
        "default_msg": "Olá, tudo bem? Meu nome é Leonardo, gostaria de falar com o responsável pelo escritório sobre prospecção."
    }
]

niches_data = {}
total_loaded = 0

for nd in niche_definitions:
    filepath = nd["file"]
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                raw_leads = json.load(f)
                
            processed_leads = []
            for item in raw_leads:
                name = item.get("name", "").strip()
                phone = item.get("whatsapp", item.get("phone", "")).strip()
                if not name or not phone:
                    continue
                
                clean_phone = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                is_pt = nd["country"] == "PT" or item.get("country") == "PT"
                
                if clean_phone.startswith("+"):
                    wa_number = clean_phone[1:]
                elif is_pt and not clean_phone.startswith("351"):
                    wa_number = "351" + clean_phone
                elif not is_pt and not clean_phone.startswith("55"):
                    wa_number = "55" + clean_phone
                else:
                    wa_number = clean_phone
                
                custom_msg = item.get("mensagem_personalizada") or nd["default_msg"]
                wa_url = f"https://wa.me/{wa_number}?text={quote(custom_msg)}"
                
                lead_obj = {
                    "id": item.get("place_id", f"lead_{len(processed_leads)+1}"),
                    "name": name,
                    "categories": item.get("categories", "Empresa Local"),
                    "address": item.get("address", ""),
                    "bairro": item.get("bairro", ""),
                    "city_state": item.get("city_state", nd["city"]),
                    "whatsapp": phone,
                    "wa_link": f"https://wa.me/{wa_number}",
                    "wa_link_com_mensagem": wa_url,
                    "rating": str(item.get("rating", "4.9")),
                    "reviews": item.get("reviews", item.get("reviews_int", 20)),
                    "gmaps_url": item.get("gmaps_url") or f"https://www.google.com/maps/search/?api=1&query={quote(name + ' ' + (item.get('address') or nd['city']))}",
                    "place_id": item.get("place_id", ""),
                    "country": "PT" if is_pt else "BR",
                    "flag": "🇵🇹" if is_pt else "🇧🇷",
                    "mensagem_personalizada": custom_msg
                }
                processed_leads.append(lead_obj)
            
            niches_data[nd["id"]] = {
                "id": nd["id"],
                "name": nd["name"],
                "country": nd["country"],
                "city": nd["city"],
                "count": len(processed_leads),
                "default_msg": nd["default_msg"],
                "leads": processed_leads
            }
            total_loaded += len(processed_leads)
            print(f"Carregado: {nd['name']} -> {len(processed_leads)} leads")
        except Exception as e:
            print(f"Erro em {filepath}: {e}")

print(f"Total de leads preparados: {total_loaded}")

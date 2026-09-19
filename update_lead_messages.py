import json
from urllib.parse import quote

# 1. Update Portugal Dental Clinics
msg_pt_odonto = "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa clínica."
with open("clinicas_dentarias_portugal_leads.json", "r", encoding="utf-8") as f:
    pt_odonto = json.load(f)

for l in pt_odonto:
    l["country"] = "PT"
    l["country_label"] = "Portugal"
    l["flag"] = "🇵🇹"
    l["lang"] = "pt-PT"
    l["mensagem_personalizada"] = msg_pt_odonto
    l["wa_link_com_mensagem"] = f"{l['wa_link']}?text={quote(msg_pt_odonto)}"

with open("clinicas_dentarias_portugal_leads.json", "w", encoding="utf-8") as f:
    json.dump(pt_odonto, f, ensure_ascii=False, indent=2)

# 2. Update Portugal Aesthetics
msg_pt_estetica = "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para o vosso espaço de estética."
with open("estetica_beleza_portugal_leads.json", "r", encoding="utf-8") as f:
    pt_estetica = json.load(f)

for l in pt_estetica:
    l["country"] = "PT"
    l["country_label"] = "Portugal"
    l["flag"] = "🇵🇹"
    l["lang"] = "pt-PT"
    l["mensagem_personalizada"] = msg_pt_estetica
    l["wa_link_com_mensagem"] = f"{l['wa_link']}?text={quote(msg_pt_estetica)}"

with open("estetica_beleza_portugal_leads.json", "w", encoding="utf-8") as f:
    json.dump(pt_estetica, f, ensure_ascii=False, indent=2)

# 3. Update Portugal Solar
msg_pt_solar = "Olá, viva! O meu nome é Leonardo e gostaria de falar consigo a respeito de uma proposta para a vossa empresa."
with open("energia_solar_obras_portugal_leads.json", "r", encoding="utf-8") as f:
    pt_solar = json.load(f)

for l in pt_solar:
    l["country"] = "PT"
    l["country_label"] = "Portugal"
    l["flag"] = "🇵🇹"
    l["lang"] = "pt-PT"
    l["mensagem_personalizada"] = msg_pt_solar
    l["wa_link_com_mensagem"] = f"{l['wa_link']}?text={quote(msg_pt_solar)}"

with open("energia_solar_obras_portugal_leads.json", "w", encoding="utf-8") as f:
    json.dump(pt_solar, f, ensure_ascii=False, indent=2)

# 4. Load Brazil Leads
msg_br = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
with open("clinicas_odontologicas_leads.json", "r", encoding="utf-8") as f:
    br_odonto = json.load(f)

for l in br_odonto:
    l["country"] = "BR"
    l["country_label"] = "Brasil"
    l["flag"] = "🇧🇷"
    l["lang"] = "pt-BR"
    l["mensagem_personalizada"] = msg_br
    l["wa_link_com_mensagem"] = f"{l['wa_link']}?text={quote(msg_br)}"

with open("clinicas_odontologicas_leads.json", "w", encoding="utf-8") as f:
    json.dump(br_odonto, f, ensure_ascii=False, indent=2)

all_odonto = br_odonto + pt_odonto
with open("clinicas_odontologicas_global.json", "w", encoding="utf-8") as f:
    json.dump(all_odonto, f, ensure_ascii=False, indent=2)

print(f"Bases de dados atualizadas com mensagens autênticas PT-PT e PT-BR!")

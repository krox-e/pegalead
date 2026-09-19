import json
import csv
import re
from urllib.parse import quote

# Load existing salon leads
with open("saloes_de_beleza_leads.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

# The new short message requested by Leonardo:
# "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."
short_msg = "Olá, tudo bem? Meu nome é Leonardo, quero falar a respeito de uma proposta."

for lead in leads:
    digits = re.sub(r'\D', '', lead['whatsapp'])
    lead["mensagem_personalizada"] = short_msg
    lead["wa_link"] = f"https://wa.me/55{digits}"
    lead["wa_link_com_mensagem"] = f"https://wa.me/55{digits}?text={quote(short_msg)}"

# Save JSON
with open("saloes_de_beleza_leads.json", "w", encoding="utf-8") as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)

# Save TXT
with open("saloes_de_beleza_leads.txt", "w", encoding="utf-8") as f:
    f.write("=" * 90 + "\n")
    f.write("    LEADS SALÕES DE BELEZA - MENSAGEM CURTA & DIRETA • LEONARDO\n")
    f.write("=" * 90 + "\n\n")
    f.write(f'Mensagem padrão: "{short_msg}"\n\n')
    f.write("=" * 90 + "\n\n")
    
    for i, lead in enumerate(leads, 1):
        f.write(f"[{i:02d}] {lead['name']}\n")
        f.write(f"  • WhatsApp         : {lead['whatsapp']}\n")
        f.write(f"  • Iniciar WhatsApp : {lead['wa_link_com_mensagem']}\n")
        f.write(f"  • Localização      : {lead['bairro']} | {lead['city_state']}\n")
        f.write(f"  • Avaliação Maps   : {lead['rating']} ★ ({lead['reviews']} avaliações)\n")
        f.write(f"  • Link Google Maps : {lead['gmaps_url']}\n")
        f.write("-" * 90 + "\n\n")

# Save CSV
with open("saloes_de_beleza_leads.csv", "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "ID", "Nome", "WhatsApp", "Link_Conversa_WhatsApp", "Endereço", "Bairro", "Cidade_UF", 
        "Categoria", "Nota_Google", "Qtd_Avaliacoes", "Possui_Site", "Link_Google_Maps"
    ])
    writer.writeheader()
    for i, lead in enumerate(leads, 1):
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

print("JSON, TXT e CSV atualizados com mensagem curta!")

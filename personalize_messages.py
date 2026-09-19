import json
import re
import csv
from urllib.parse import quote

with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

# Sort leads by popularity (review count) to pick the absolute best 25-30 leads
for l in leads:
    try:
        l["reviews_int"] = int(str(l.get("reviews", 0)).replace(".", "").replace(",", ""))
    except:
        l["reviews_int"] = 0

sorted_leads = sorted(leads, key=lambda x: x["reviews_int"], reverse=True)

# Personalize message for Leonardo
def create_personalized_message(lead):
    name = lead['name']
    rating = lead['rating']
    reviews = lead['reviews']
    
    msg = (
        f"Olá, tudo bem? Meu nome é Leonardo, trabalho criando páginas e cardápios digitais para churrascarias.\n\n"
        f"Estava no Google Maps e vi que a {name} tem uma excelente avaliação ({rating} ★ com {reviews} avaliações!), "
        f"mas notei que vocês ainda não possuem um site próprio nem cardápio interativo na bio do Instagram.\n\n"
        f"Hoje a maioria dos clientes pesquisa no Google antes de escolher onde almoçar ou jantar. "
        f"Sem um site, muitos acabam indo em concorrentes.\n\n"
        f"Montei um modelo visual de cardápio digital e página de reservas para vocês. "
        f"Posso te mandar uma prévia rápida de 30 segundos por aqui?"
    )
    return msg

# Add direct pre-filled WhatsApp link to all leads
for lead in leads:
    msg = create_personalized_message(lead)
    digits = re.sub(r'\D', '', lead['whatsapp'])
    if digits.startswith("55"):
        clean_num = digits
    else:
        clean_num = f"55{digits}"
    lead["mensagem_personalizada"] = msg
    lead["wa_link_com_mensagem"] = f"https://wa.me/{clean_num}?text={quote(msg)}"

# Save top 30 leads for Leonardo in TXT
top_30 = sorted_leads[:30]
with open("disparo_30_leads_leonardo.txt", "w", encoding="utf-8") as f:
    f.write("=" * 90 + "\n")
    f.write("     LISTA RECOMENDADA DE 30 LEADS PARA DISPARO SEGURO - LEONARDO\n")
    f.write("=" * 90 + "\n\n")
    f.write("Critério: Top 30 churrascarias mais populares e bem avaliadas sem site no Brasil.\n")
    f.write("Objetivo: Envio seguro de 25 a 30 mensagens sem risco de bloqueio no WhatsApp.\n\n")
    f.write("=" * 90 + "\n\n")
    
    for i, lead in enumerate(top_30, 1):
        f.write(f"[{i:02d}] {lead['name']}\n")
        f.write(f"  • WhatsApp          : {lead['whatsapp']}\n")
        f.write(f"  • Local             : {lead['bairro']} | {lead['city_state']}\n")
        f.write(f"  • Avaliação         : {lead['rating']} ★ ({lead['reviews']} avaliações no Maps)\n")
        f.write(f"  • Link com Mensagem : {lead['wa_link_com_mensagem']}\n")
        f.write("-" * 90 + "\n\n")

# Save updated full JSON
with open("churrascarias_sem_site_100.json", "w", encoding="utf-8") as f:
    json.dump(leads, f, ensure_ascii=False, indent=2)

print("Gerados arquivos com mensagens personalizadas para Leonardo!")

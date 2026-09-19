import httpx
import re
import json
import time
import sys
from urllib.parse import quote

sys.stdout.reconfigure(encoding='utf-8')

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

def is_true_brazil_mobile(phone_str):
    if not phone_str:
        return False, None, None
    digits = re.sub(r'\D', '', phone_str)
    
    # Strip country code 55 if present
    if digits.startswith("55") and len(digits) == 13:
        digits = digits[2:]
    elif digits.startswith("0") and len(digits) == 12:
        digits = digits[1:]
        
    if len(digits) != 11:
        return False, None, None
        
    ddd = int(digits[:2])
    if ddd not in VALID_DDDS:
        return False, None, None
        
    # First digit of mobile is 9, and second digit in Brazil is typically 6, 7, 8, 9 (or 4, 5 in some areas)
    if digits[2] != '9':
        return False, None, None
    if digits[3] not in '567894': # True mobile ranges
        return False, None, None
        
    formatted = f"({ddd}) {digits[2:7]}-{digits[7:]}"
    wa_link = f"https://wa.me/55{digits}"
    return True, formatted, wa_link

# Load leads
with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

true_mobile_leads = []
for l in leads:
    ok, fmt, link = is_true_brazil_mobile(l.get("whatsapp"))
    if ok:
        l["whatsapp"] = fmt
        l["wa_link"] = link
        # Re-encode message for Leonardo
        name = l['name']
        rating = l['rating']
        reviews = l['reviews']
        msg = (
            f"Olá, tudo bem? Meu nome é Leonardo, trabalho criando páginas e cardápios digitais para churrascarias.\n\n"
            f"Estava no Google Maps e vi que a {name} tem uma excelente avaliação ({rating} ★ com {reviews} avaliações!), "
            f"mas notei que vocês ainda não possuem um site próprio nem cardápio interativo na bio do Instagram.\n\n"
            f"Hoje a maioria dos clientes pesquisa no Google antes de escolher onde almoçar ou jantar. "
            f"Sem um site, muitos acabam indo em concorrentes.\n\n"
            f"Montei um modelo visual de cardápio digital e página de reservas para vocês. "
            f"Posso te mandar uma prévia rápida de 30 segundos por aqui?"
        )
        l["mensagem_personalizada"] = msg
        clean_num = re.sub(r'\D', '', link)
        l["wa_link_com_mensagem"] = f"{link}?text={quote(msg)}"
        true_mobile_leads.append(l)

print(f"Total True Mobile WhatsApp leads available: {len(true_mobile_leads)}")

import json
import httpx
import re
from get_10_estetica import search_gmaps, ESTETICA_QUERIES

client = httpx.Client(timeout=15.0)
all_leads = []
seen = set()

# Broaden queries across Brazil capital cities and top neighborhoods
QUERIES = [
    "clinica de estetica sao paulo sp",
    "clinica de estetica moema sao paulo",
    "clinica de estetica jardins sao paulo",
    "clinica de estetica tatuape sp",
    "clinica de estetica santana sp",
    "clinica de estetica campinas sp",
    "clinica de estetica santo andre sp",
    "clinica de estetica sao bernardo do campo",
    "clinica de estetica osasco sp",
    "clinica de estetica guarulhos sp",
    "clinica de estetica rio de janeiro rj",
    "clinica de estetica barra da tijuca rj",
    "clinica de estetica copacabana rj",
    "clinica de estetica niteroi rj",
    "clinica de estetica belo horizonte mg",
    "clinica de estetica curitiba pr",
    "clinica de estetica florianopolis sc",
    "clinica de estetica porto alegre rs",
    "clinica de estetica brasilia df",
    "clinica de estetica goiania go",
    "clinica de estetica salvador ba",
    "clinica de estetica recife pe",
    "clinica de estetica fortaleza ce",
    "salao de beleza e estetica campinas",
    "salao de beleza e estetica rio de janeiro",
    "salao de beleza e estetica curitiba"
]

for q in QUERIES:
    res = search_gmaps(q, client)
    for p in res:
        k = p['name'].strip().lower() + "|" + p['whatsapp']
        if k not in seen:
            seen.add(k)
            all_leads.append(p)

for l in all_leads:
    try:
        l['reviews_int'] = int(str(l.get('reviews', 0)).replace('.', '').replace(',', ''))
    except:
        l['reviews_int'] = 0

all_leads.sort(key=lambda x: x['reviews_int'], reverse=True)

print(f"Total coletado: {len(all_leads)}")
for i, l in enumerate(all_leads[:15], 1):
    print(f"[{i:02d}] {l['name']} | {l['whatsapp']} | {l['city_state']} | {l['rating']} ★ ({l['reviews']} avaliações)")

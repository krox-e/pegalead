import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("churrascarias_sem_site_100.json", "r", encoding="utf-8") as f:
    leads = json.load(f)

print(f"Total leads in JSON: {len(leads)}")

# Check WhatsApp format: (XX) 9XXXX-XXXX
whatsapp_pattern = re.compile(r'^\(\d{2}\)\s*9\d{4}-\d{4}$')
valid_whatsapp = [x for x in leads if whatsapp_pattern.match(x.get("whatsapp", ""))]
print(f"Strict WhatsApp numbers (11 digits, starts with 9): {len(valid_whatsapp)} / {len(leads)}")

# Check website field
with_website = [x for x in leads if x.get("website")]
print(f"Leads with website on Maps: {len(with_website)}")

# Check direct WhatsApp links:
valid_links = [x for x in leads if x.get("wa_link", "").startswith("https://wa.me/55")]
print(f"Valid wa.me direct chat links: {len(valid_links)} / {len(leads)}")

# Check ratings
ratings = [float(x["rating"]) for x in leads if x.get("rating") and x["rating"] != "Sem avaliação"]
if ratings:
    print(f"Average Google Rating: {sum(ratings)/len(ratings):.2f} / 5.0 (from {len(ratings)} rated businesses)")

# Distribution by city
cities = {}
for x in leads:
    c = x.get("city_state", "Desconhecido")
    cities[c] = cities.get(c, 0) + 1

print("\nDistribution by City/Region:")
for c, count in sorted(cities.items(), key=lambda k: k[1], reverse=True):
    print(f"  • {c}: {count}")

print("\nSample 3 leads:")
for l in leads[:3]:
    print(json.dumps(l, ensure_ascii=False, indent=2))

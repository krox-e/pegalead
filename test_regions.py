import httpx
import json

endpoints = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

# Brazil bbox approx: south, west, north, east: -33.75, -73.98, 5.27, -34.79
# Major Brazilian regions bbox:
regions = [
    ("Grande Sao Paulo", -24.0, -47.0, -23.3, -46.2),
    ("Rio de Janeiro", -23.1, -43.8, -22.7, -43.0),
    ("Minas Gerais / BH", -20.1, -44.2, -19.7, -43.8),
    ("Curitiba / PR", -25.6, -49.4, -25.3, -49.1),
    ("Porto Alegre / RS", -30.2, -51.3, -29.9, -51.0),
    ("Brasilia / DF", -16.0, -48.2, -15.5, -47.7),
    ("Goiania / GO", -16.8, -49.4, -16.5, -49.1),
    ("Salvador / BA", -13.1, -38.6, -12.8, -38.3),
    ("Fortaleza / CE", -3.9, -38.7, -3.6, -38.4),
    ("Recife / PE", -8.2, -35.1, -7.9, -34.8),
    ("Campinas / SP", -23.0, -47.2, -22.7, -46.9),
    ("Ribeirao Preto / SP", -21.3, -47.9, -21.1, -47.7),
    ("Santos / SP", -24.0, -46.4, -23.9, -46.2),
    ("Florianopolis / SC", -27.8, -48.7, -27.4, -48.4),
    ("Caxias do Sul / RS", -29.3, -51.3, -29.0, -51.0),
]

all_results = []
client = httpx.Client(timeout=20.0)

for name, s, w, n, e in regions:
    q = f"""
    [out:json][timeout:15];
    (
      node["amenity"="restaurant"]["cuisine"~"barbecue|churrasco|steak",i]({s},{w},{n},{e});
      node["amenity"="restaurant"]["name"~"Churrascaria|Churrasco|Costelaria|Espetinho|Gaucho|Gaúcho|Boi|Picanha|Fogo",i]({s},{w},{n},{e});
      way["amenity"="restaurant"]["cuisine"~"barbecue|churrasco|steak",i]({s},{w},{n},{e});
      way["amenity"="restaurant"]["name"~"Churrascaria|Churrasco|Costelaria|Espetinho|Gaucho|Gaúcho|Boi|Picanha|Fogo",i]({s},{w},{n},{e});
    );
    out center tags;
    """
    for ep in endpoints:
        try:
            r = client.post(ep, data={"data": q})
            if r.status_code == 200:
                data = r.json()
                elems = data.get("elements", [])
                print(f"{name}: found {len(elems)} elements via {ep}")
                all_results.extend(elems)
                break
        except Exception as err:
            pass

print(f"Total raw elements: {len(all_results)}")

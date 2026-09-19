import httpx
import json

# Query Overpass API for churrascarias in Brazil
query = """
[out:json][timeout:30];
area["ISO3166-1"="BR"]->.brazil;
(
  node["amenity"="restaurant"]["cuisine"~"barbecue|churrasco|steak",i](area.brazil);
  node["amenity"="restaurant"]["name"~"Churrascaria|Churrasco|Costelaria|Espetinho|Gaucho|Gaúcho",i](area.brazil);
  way["amenity"="restaurant"]["cuisine"~"barbecue|churrasco|steak",i](area.brazil);
  way["amenity"="restaurant"]["name"~"Churrascaria|Churrasco|Costelaria|Espetinho|Gaucho|Gaúcho",i](area.brazil);
);
out center tags;
"""

try:
    response = httpx.post("https://overpass-api.de/api/interpreter", data={"data": query}, timeout=30.0)
    data = response.json()
    elements = data.get("elements", [])
    print(f"Total elements found in Overpass: {len(elements)}")
    
    without_website = []
    for el in elements:
        tags = el.get("tags", {})
        website = tags.get("website") or tags.get("contact:website") or tags.get("url")
        if not website:
            name = tags.get("name")
            phone = tags.get("phone") or tags.get("contact:phone") or tags.get("contact:whatsapp") or tags.get("contact:mobile")
            city = tags.get("addr:city") or tags.get("addr:municipality")
            street = tags.get("addr:street")
            housenumber = tags.get("addr:housenumber")
            suburb = tags.get("addr:suburb") or tags.get("addr:district")
            state = tags.get("addr:state")
            lat = el.get("lat") or (el.get("center", {}).get("lat") if "center" in el else None)
            lon = el.get("lon") or (el.get("center", {}).get("lon") if "center" in el else None)
            
            if name:
                without_website.append({
                    "name": name,
                    "phone": phone,
                    "street": street,
                    "housenumber": housenumber,
                    "suburb": suburb,
                    "city": city,
                    "state": state,
                    "lat": lat,
                    "lon": lon
                })
                
    print(f"Total without website: {len(without_website)}")
    with_phone = [x for x in without_website if x['phone']]
    print(f"Without website and with phone: {len(with_phone)}")
    print("Sample:", json.dumps(with_phone[:5], indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")

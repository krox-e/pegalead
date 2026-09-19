import httpx
import re
import json
from urllib.parse import quote, unquote

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

def check_instagram_and_website(name, city, client):
    """
    Searches for the Instagram of the business and checks if there's an external website in bio.
    Returns: (instagram_url, has_website, website_url)
    """
    query = f'"{name}" "{city}" site:instagram.com'
    # Try DuckDuckGo HTML search
    ddg_url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    try:
        r = client.post(
            "https://html.duckduckgo.com/html/",
            data={"q": query},
            headers=headers,
            timeout=8.0
        )
        if r.status_code == 200:
            # Find instagram profile links: instagram.com/username
            links = re.findall(r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_\.]+)/?', r.text)
            # Filter out generic instagram paths like 'p', 'explore', 'reel', 'stories', 'tv'
            valid_profiles = [u for u in links if u.lower() not in ['p', 'explore', 'reel', 'stories', 'tv', 'about', 'developer', 'directory', 'legal', 'privacy']]
            
            if valid_profiles:
                insta_user = valid_profiles[0]
                insta_url = f"https://www.instagram.com/{insta_user}/"
                
                # Check snippet for external website clues
                # In DuckDuckGo snippets, website links often appear in bio text
                snippet_match = re.search(rf'{insta_user}.*?</p>', r.text, re.IGNORECASE | re.DOTALL)
                snippet_text = snippet_match.group(0) if snippet_match else ""
                
                # Look for website patterns in snippet or check bio
                website_patterns = [
                    r'https?://(?:www\.)?([a-zA-Z0-9-]+\.(?:com\.br|com|site|online|net|org|menu|delivery))',
                    r'linktr\.ee/[a-zA-Z0-9_]+',
                    r'bit\.ly/[a-zA-Z0-9_]+',
                    r'beacons\.ai/[a-zA-Z0-9_]+'
                ]
                
                for wp in website_patterns:
                    m = re.search(wp, snippet_text, re.IGNORECASE)
                    if m:
                        return insta_url, True, m.group(0)
                        
                return insta_url, False, None
    except Exception as e:
        # print("Error checking insta:", e)
        pass
        
    return None, False, None

# Test with a few sample businesses
test_cases = [
    ("Bicudo Churrascaria", "São Paulo"),
    ("El Toro Steakhouse", "São Paulo"),
    ("Churrascaria Boi Na Brasa", "São Paulo"),
    ("Churrascaria Ponteio Morumbi", "São Paulo"), # Ponteio has a website!
]

client = httpx.Client(timeout=10.0)
for name, city in test_cases:
    insta, has_web, web_url = check_instagram_and_website(name, city, client)
    print(f"[{name}] -> Insta: {insta} | Tem site no Insta? {has_web} ({web_url})")

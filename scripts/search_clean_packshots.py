import urllib.request
import urllib.parse
import json

HEADERS = {'User-Agent': 'OnizoukShopCatalog/1.0 (https://onizoukashop.com; contact@onizoukashop.com)'}

def search_wikimedia_files(query, limit=10):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&srlimit={limit}&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    results = []
    for s in data.get('query', {}).get('search', []):
        t = s.get('title', '')
        if any(t.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            results.append(t)
    return results

queries = [
    "gas cooker white background",
    "gas range stainless steel",
    "water dispenser",
    "water cooler bottle",
    "OLED TV isolated",
    "smart TV white background",
    "television png isolated",
    "steam iron white background",
    "air fryer white background"
]

for q in queries:
    print(f"=== {q} ===")
    res = search_wikimedia_files(q, 4)
    for r in res:
        print("  ", r)

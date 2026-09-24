import urllib.request
import urllib.parse
import json

headers = {'User-Agent': 'OnizoukShopBrandCrawler/1.0 (contact@onizoukashop.com)'}

def search_files(term):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(term)}&srnamespace=6&srlimit=5&format=json"
    req = urllib.request.Request(url, headers=headers)
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    items = []
    for s in data.get('query', {}).get('search', []):
        t = s.get('title', '')
        if any(t.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            items.append(t)
    return items

queries = [
    "Samsung refrigerator",
    "LG refrigerator",
    "Sharp refrigerator",
    "Haier refrigerator",
    "Hisense refrigerator",
    "refrigerator white background",
    "LG air conditioner",
    "split air conditioner",
    "Midea air conditioner",
    "Gree air conditioner",
    "Sony Bravia",
    "LG OLED TV",
    "Samsung QLED",
    "TCL smart TV",
    "flat screen television",
    "gas stove",
    "gas cooker",
    "kitchen stove oven",
    "Beko stove",
    "electric oven",
    "microwave oven",
    "blender kitchen",
    "Moulinex",
    "Philips iron",
    "steam iron",
    "electric fan",
    "stand fan",
    "coffee maker"
]

for q in queries:
    results = search_files(q)
    print(f"{q}: {results[:2]}")

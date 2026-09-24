import urllib.request
import urllib.parse
import json
import os

headers = {'User-Agent': 'OnizoukShopApp/1.0 (contact@onizoukashop.com)'}

def search_wikimedia_image(query):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&srlimit=5&format=json"
    req = urllib.request.Request(url, headers=headers)
    data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
    
    for item in data.get('query', {}).get('search', []):
        title = item.get('title', '')
        # Only image extensions
        if any(title.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png']):
            info_url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(title)}&prop=imageinfo&iiprop=url|thumburl&iiurlwidth=800&format=json"
            req2 = urllib.request.Request(info_url, headers=headers)
            info_data = json.loads(urllib.request.urlopen(req2, timeout=10).read().decode('utf-8'))
            pages = info_data.get('query', {}).get('pages', {})
            for p in pages.values():
                imgs = p.get('imageinfo', [])
                if imgs:
                    img_url = imgs[0].get('thumburl') or imgs[0].get('url')
                    return title, img_url
    return None, None

brand_queries = {
    # Refrigerators
    "samsung_fridge": "SAMSUNG REFRIGERATOR RF60J9030WZ",
    "samsung_fridge_2": "Samsung Refrigerator RF24FSEDBSR",
    "lg_fridge": "LG refrigerator",
    "hisense_fridge": "Hisense IFA 2018 Berlin refrigerator",
    "sharp_fridge": "Sharp refrigerator",
    "haier_fridge": "Haier refrigerator",
    "freezer_chest": "chest freezer",
    
    # Air Conditioners
    "lg_split_1": "Split LG Dual Inverter 1",
    "lg_split_2": "Split LG Dual Inverter 2",
    "midea_split": "Condizionatore Midea Unita interna",
    "gree_split": "Gree Ease Wind air conditioner",
    "tcl_split": "split air conditioner wall",
    "samsung_split": "air conditioner wall unit",
    "stand_fan": "electric pedestal fan",
    
    # Televisions
    "lg_oled_tv": "LG smart TV",
    "sony_bravia_tv": "Sony Bravia CES",
    "samsung_qled_tv": "Samsung Smart TV",
    "tcl_tv": "TCL smart TV",
    "hisense_tv": "Hisense TV",
    "soundbar": "soundbar speaker",
    
    # Cookers & Ovens
    "gas_cooker_stove": "gas stove burner",
    "beko_cooker": "freestanding gas cooker",
    "kitchen_oven": "electric oven kitchen",
    "built_in_hob": "induction cooktop hob",
    
    # Small Appliances
    "panasonic_microwave": "Panasonic MICROWAVE OVEN",
    "sharp_microwave": "Sharp microwave oven",
    "moulinex_blender": "electric blender kitchen",
    "food_processor": "food processor blender",
    "philips_iron": "electric steam iron",
    "tefal_kettle": "electric kettle cordless",
    "coffee_maker": "drip coffee maker"
}

results = {}
for key, q in brand_queries.items():
    title, url = search_wikimedia_image(q)
    results[key] = {"title": title, "url": url}
    print(f"[{key}] -> {title}")
    if url:
        print(f"    URL: {url[:100]}...")

with open("scripts/found_brand_images.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print("Saved to scripts/found_brand_images.json")

import os
import sys
import time
import shutil
import urllib.request
import urllib.parse
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product, ProductImage, Category, Brand

ARTIFACT_DIR = r"C:\Users\a\.gemini\antigravity-ide\brain\ae1a582c-2bf0-4e09-8b46-bac4cae90a35"
MEDIA_DIR = r"c:\Censure\OnizoukShop\media\products"
os.makedirs(MEDIA_DIR, exist_ok=True)

# 1. Copy studio flagships
samsung_studio = os.path.join(ARTIFACT_DIR, "fridge_studio_samsung_1790116051075.jpg")
midea_studio = os.path.join(ARTIFACT_DIR, "ac_studio_midea_1790116068754.jpg")

if os.path.exists(samsung_studio):
    shutil.copyfile(samsung_studio, os.path.join(MEDIA_DIR, "samsung_flagship_fridge.jpg"))
    print("Copied Samsung studio flagship.")
if os.path.exists(midea_studio):
    shutil.copyfile(midea_studio, os.path.join(MEDIA_DIR, "midea_flagship_ac.jpg"))
    print("Copied Midea studio flagship.")

# 2. Get thumb URLs from Wikimedia API using proper User-Agent
HEADERS = {
    'User-Agent': 'OnizoukShopCatalog/1.0 (https://onizoukashop.com; contact@onizoukashop.com) Python/3.13 urllib'
}

def get_wikimedia_thumb(file_title, width=800):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote('File:' + file_title)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=10).read().decode('utf-8'))
        pages = data.get('query', {}).get('pages', {})
        for p in pages.values():
            imgs = p.get('imageinfo', [])
            if imgs:
                return imgs[0].get('thumburl') or imgs[0].get('url')
    except Exception as e:
        print(f"Error fetching thumb for {file_title}: {e}")
    return None

FILES_TO_DOWNLOAD = [
    # Refrigerators
    ("fridge_samsung_rf24.jpg", "Samsung Refrigerator RF24FSEDBSR.jpg", ["Samsung", "Sharp"]),
    ("fridge_hisense_ifa.jpg", "Hisense, IFA 2018, Berlin (P1070193).jpg", ["Hisense"]),
    ("fridge_mabe_double.jpg", "2 NEVERA.jpg", ["Beko", "Westpool", "Ocean"]),
    
    # Air Conditioners
    ("ac_lg_dual_1.jpg", "Split LG Dual Inverter 1.jpg", ["LG Electronics"]),
    ("ac_lg_dual_2.jpg", "Split LG Dual Inverter 2.jpg", ["LG Electronics"]),
    ("ac_midea_indoor.jpg", "Condizionatore Midea - Unità interna.jpg", ["Midea"]),
    ("ac_gree_ease.jpg", "Gree Ease Wind air conditioner.jpg", ["Gree"]),
    ("ac_hyundai_split.jpg", "HYUNDAI - Air conditioner mini split (model BMS-12HD).jpg", ["TCL"]),
    
    # TV & Sound
    ("tv_lg_smart.png", "LG smart TV.png", ["LG Electronics"]),
    ("tv_sony_bravia.jpg", "Sony Bravia KDL-Z4500.jpg", ["Sony"]),
    ("tv_techwood_flat.jpg", "Techwood flat screen television from 2010.jpg", ["Samsung", "TCL", "Hisense"]),
    
    # Cookers & Stoves
    ("stove_mabe_gas.jpg", "2015-11-05 jueves 174624 - Cocina Mabe.jpg", ["Beko", "Ocean"]),
    ("stove_bic_camera.jpg", "Built-in Gas Stove at Bic Camera Namba.jpg", ["Beko", "Ocean"]),
    
    # Small Appliances
    ("microwave_panasonic.jpg", "Panasonic MICROWAVE OVEN NN-GM333W.jpg", ["Moulinex", "Sharp"]),
    ("iron_rowenta.jpg", "A Rowenta iron.jpg", ["Philips", "Tefal", "Binatone"]),
]

for dest_fname, wiki_title, target_brands in FILES_TO_DOWNLOAD:
    dest_path = os.path.join(MEDIA_DIR, dest_fname)
    if not os.path.exists(dest_path) or os.path.getsize(dest_path) < 1000:
        time.sleep(1.2)  # respectful delay to prevent 429
        thumb_url = get_wikimedia_thumb(wiki_title, 800)
        if thumb_url:
            try:
                print(f"Downloading {dest_fname} (800px thumb)...")
                req = urllib.request.Request(thumb_url, headers=HEADERS)
                with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, 'wb') as f:
                    f.write(resp.read())
                print(f"-> Saved {dest_fname} ({os.path.getsize(dest_path)} bytes)")
            except Exception as e:
                print(f"Failed {dest_fname}: {e}")
        else:
            print(f"Could not get thumb URL for {wiki_title}")
    else:
        print(f"Already exists: {dest_fname} ({os.path.getsize(dest_path)} bytes)")

print("\n--- Image download complete! ---")

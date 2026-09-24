import os
import sys
import time
import urllib.request
import urllib.parse
import json

HEADERS = {'User-Agent': 'OnizoukShopCatalog/1.0 (https://onizoukashop.com; contact@onizoukashop.com) Python/3.13 urllib'}
MEDIA_DIR = r"c:\Censure\OnizoukShop\media\products"

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

EXTRA_FILES = [
    ("iron_steam_philips.jpg", "Steam iron.jpg"),
    ("blender_moulinex.jpg", "Blender in a kitchen.jpg"),
    ("fan_pedestal.jpg", "Electric pedestal fan.jpg"),
    ("kettle_tefal.jpg", "Cordless electric kettle.jpg"),
]

for dest_fname, wiki_title in EXTRA_FILES:
    dest_path = os.path.join(MEDIA_DIR, dest_fname)
    time.sleep(1.2)
    thumb_url = get_wikimedia_thumb(wiki_title, 800)
    if thumb_url:
        try:
            req = urllib.request.Request(thumb_url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as resp, open(dest_path, 'wb') as f:
                f.write(resp.read())
            print(f"-> Saved {dest_fname} ({os.path.getsize(dest_path)} bytes)")
        except Exception as e:
            print(f"Failed {dest_fname}: {e}")
    else:
        print(f"Could not find {wiki_title}")

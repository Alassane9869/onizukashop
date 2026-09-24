import urllib.request
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
MEDIA_DIR = r"c:\Censure\OnizoukShop\media\products"

UNSPLASH_APPLIANCES = [
    ("stove_modern_gas_range.jpg", "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80"),
    ("tv_ultra_4k_oled.jpg", "https://images.unsplash.com/photo-1593359677879-a4bb92f829d1?auto=format&fit=crop&w=800&q=80"),
    ("tv_minimal_living_room.jpg", "https://images.unsplash.com/photo-1593784991095-a205069470b6?auto=format&fit=crop&w=800&q=80"),
    ("kitchen_modern_fridge.jpg", "https://images.unsplash.com/photo-1584992236310-6edddc08acff?auto=format&fit=crop&w=800&q=80"),
    ("blender_smoothie_pro.jpg", "https://images.unsplash.com/photo-1570222094114-d054a817e56b?auto=format&fit=crop&w=800&q=80"),
    ("water_dispenser_bottle.jpg", "https://images.unsplash.com/photo-1548839140-29a749e1bc4e?auto=format&fit=crop&w=800&q=80"),
]

for fname, url in UNSPLASH_APPLIANCES:
    dest = os.path.join(MEDIA_DIR, fname)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp, open(dest, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {fname}: {os.path.getsize(dest)} bytes")
    except Exception as e:
        print(f"Failed {fname}: {e}")

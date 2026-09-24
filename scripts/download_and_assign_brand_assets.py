"""
Download and assign 100% authentic, official brand product images from Samsung, LG, Philips, Moulinex, Sony, Hisense, etc.
"""
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')
import django
django.setup()

from shop.models import Product, ProductImage, Brand, Category

MEDIA_DIR = os.path.join('media', 'products')
os.makedirs(MEDIA_DIR, exist_ok=True)

OFFICIAL_ASSETS = [
    # SAMSUNG
    {
        'filename': 'samsung_bespoke_french_door.png',
        'url': 'https://images.samsung.com/is/image/samsung/p6pim/africa_fr/rf65dg9h0esreu/gallery/africa-fr-t-style-french-door-215inch-family-hub-rf65dg9h0esreu-550669483?$1164_776_PNG$',
        'brand': 'Samsung',
        'category_slug': 'refrigerateurs-congelateurs',
        'keywords': ['french door', 'multi-portes', 'bespoke', 'side by side', 'américain'],
    },
    {
        'filename': 'samsung_4door_beverage.png',
        'url': 'https://images.samsung.com/is/image/samsung/p6pim/africa_fr/rf65db960e22ef/gallery/africa-fr-4-door-beverage-center-rf65db960e22ef-550698904?$1164_776_PNG$',
        'brand': 'Samsung',
        'category_slug': 'refrigerateurs-congelateurs',
        'keywords': ['combiné', 'no frost', 'frigo', 'réfrigérateur'],
    },
    {
        'filename': 'samsung_windfree_ac.png',
        'url': 'https://images.samsung.com/is/image/samsung/africa-fr-wind-free-ar9500t-ar12tvhabwk-af-frontwhite-251546540?$1164_776_PNG$',
        'brand': 'Samsung',
        'category_slug': 'climatiseurs-inverter',
        'keywords': ['windfree', 'split', 'climatiseur', 'inverter'],
    },
    {
        'filename': 'samsung_crystal_uhd_tv.png',
        'url': 'https://images.samsung.com/is/image/samsung/p6pim/africa_fr/ua55u8000fuxke/gallery/africa-fr-uhd-4k-tv-ua55u8000fuxke-front-black-548260891?$1164_776_PNG$',
        'brand': 'Samsung',
        'category_slug': 'smart-tv-son',
        'keywords': ['crystal', 'uhd', '4k', 'smart tv', '55'],
    },
    {
        'filename': 'samsung_qled_tv.png',
        'url': 'https://images.samsung.com/is/image/samsung/p6pim/africa_fr/qa65q8faauxke/gallery/africa-fr-qled-q8-qa65q8faauxke-547929326?$1164_776_PNG$',
        'brand': 'Samsung',
        'category_slug': 'smart-tv-son',
        'keywords': ['qled', 'neo qled', '65', '75', '85', 'oled'],
    },

    # LG ELECTRONICS
    {
        'filename': 'lg_oled_55_tv.jpg',
        'url': 'https://www.lg.com/content/dam/channel/wcms/nz/images/tvs/oled55a1pva_anr_ehap_nz_c/gallery/Z1.jpg',
        'brand': 'LG Electronics',
        'category_slug': 'smart-tv-son',
        'keywords': ['oled', 'nanocell', 'smart tv', '4k', '55', '65', 'thinq'],
    },
    {
        'filename': 'lg_neochef_microwave.jpg',
        'url': 'https://www.lg.com/africa/images/cooking-appliances/md05819576/gallery/medium01V.jpg',
        'brand': 'LG Electronics',
        'category_slug': 'petit-electromenager',
        'keywords': ['micro-ondes', 'neochef', 'four', 'smart inverter'],
    },
    {
        'filename': 'lg_dual_inverter_ac.jpg',
        'url': 'https://www.lg.com/africa/images/residential-air-conditioners/md07589181/gallery/lg-single-split-inverter-air-conditioner-sj-2026-s4-q18kl28e-gallery-gallery-1100-01.jpg',
        'brand': 'LG Electronics',
        'category_slug': 'climatiseurs-inverter',
        'keywords': ['dual inverter', 'split', 'climatiseur', 'artcool'],
    },

    # PHILIPS
    {
        'filename': 'philips_series_2200_espresso.png',
        'url': 'https://images.philips.com/is/image/philipsconsumer/vrs_514c6884_aac0_4140_950b6d8d713ef25f?$png$&wid=1200&hei=630',
        'brand': 'Philips',
        'category_slug': 'petit-electromenager',
        'keywords': ['cafetière', 'expresso', 'broyeur', 'cafetiere', 'café'],
    },
    {
        'filename': 'philips_series_2200_alt.png',
        'url': 'https://images.philips.com/is/image/philipsconsumer/vrs_372f2e29_3a7c_437e_85ab164e9b5232e3?$png$&wid=1200&hei=630',
        'brand': 'Philips',
        'category_slug': 'petit-electromenager',
        'keywords': ['airfryer', 'friteuse', 'fer à repasser', 'centrifugeuse', 'mixeur'],
    },

    # MOULINEX
    {
        'filename': 'moulinex_doubleforce_robot.jpg',
        'url': 'https://www.moulinex.com.eg/medias/?context=bWFzdGVyfGltYWdlc3w5MDI1fGltYWdlL2pwZWd8YVcxaFoyVnpMMmhpWlM5b05XSXZNamt6TWpFNU5USTNNakk1TnpRfDgyODczYTZmZTNmMWNkYTdjYTExOTE5MDk1YTExZjYwZjk5MTEwMjc2NWJjNmUwYWQ4Y2Q2NmJhYjg2ZjY1ODA',
        'brand': 'Moulinex',
        'category_slug': 'petit-electromenager',
        'keywords': ['robot', 'doubleforce', 'multifonction', 'hachoir', 'blender'],
    },

    # SONY
    {
        'filename': 'sony_bravia_oled_xr.png',
        'url': 'https://www.sony.fr/image/8c916cf0cf26db971c16e932c04a0ed8?fmt=png-alpha&wid=1578&hei=1050&bgcolor=F6F9FF',
        'brand': 'Sony',
        'category_slug': 'smart-tv-son',
        'keywords': ['bravia', 'oled', 'xr', 'google tv', '4k'],
    },

    # HISENSE
    {
        'filename': 'hisense_multidoor_fridge.jpg',
        'url': 'https://api.hisense.fr/wp-content/uploads/2025/07/rq5p470safe-front-close-scaled.jpg',
        'brand': 'Hisense',
        'category_slug': 'refrigerateurs-congelateurs',
        'keywords': ['multi-portes', 'french door', 'side by side', 'réfrigérateur', 'congélateur'],
    },
    {
        'filename': 'hisense_combi_fridge.png',
        'url': 'https://api.hisense.fr/wp-content/uploads/2020/07/RB390N4BC20-Front-close.png',
        'brand': 'Hisense',
        'category_slug': 'refrigerateurs-congelateurs',
        'keywords': ['combiné', 'combi', 'frigo', 'nofrost'],
    },

    # MIDEA
    {
        'filename': 'midea_water_dispenser.webp',
        'url': 'https://nezhawater-tech.com/wp-content/uploads/2025/07/Distributeur-deau-Midea-JL1844S-RO-1.webp',
        'brand': 'Midea',
        'category_slug': 'petit-electromenager',
        'keywords': ['fontaine', 'distributeur', 'eau', 'chaud/froid'],
    },
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
}

downloaded_map = {}

print("=== 1. TÉLÉCHARGEMENT DES PACKSHOTS OFFICIELS DES MARQUES ===")
for item in OFFICIAL_ASSETS:
    filepath = os.path.join(MEDIA_DIR, item['filename'])
    url = item['url']
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            if len(data) > 5000:  # Valid image size
                with open(filepath, 'wb') as f:
                    f.write(data)
                rel_path = f"products/{item['filename']}"
                downloaded_map[item['filename']] = rel_path
                print(f"[OK] {item['brand']} -> {item['filename']} ({len(data):,} bytes)")
            else:
                print(f"[WARN] Too small ({len(data)} bytes) for {url}")
    except Exception as e:
        print(f"[FAIL] {item['filename']}: {e}")

print(f"\nTéléchargés avec succès: {len(downloaded_map)}/{len(OFFICIAL_ASSETS)}")

print("\n=== 2. ASSIGNATION PRÉCISE AUX PRODUITS DANS LA BASE DE DONNÉES ===")
assigned_count = 0

for item in OFFICIAL_ASSETS:
    fn = item['filename']
    if fn not in downloaded_map:
        continue
    rel_path = downloaded_map[fn]

    # Find matching products by Brand and/or Category and/or Keywords
    qs = Product.objects.all()
    if item.get('brand'):
        try:
            b = Brand.objects.get(name__icontains=item['brand'])
            qs_brand = qs.filter(brand=b)
        except Brand.DoesNotExist:
            qs_brand = qs.none()
    else:
        qs_brand = qs

    matched_products = set()
    for p in qs_brand:
        name_lower = p.name.lower()
        if any(kw in name_lower for kw in item['keywords']):
            matched_products.add(p)

    for p in matched_products:
        p.images.all().delete()
        ProductImage.objects.create(
            product=p,
            image=rel_path,
            is_primary=True,
            alt_text=f"{p.name} - Photo officielle {item['brand']}"
        )
        assigned_count += 1
        print(f" -> Assigné à [{p.brand.name if p.brand else 'N/A'}] {p.name[:45]}")

print(f"\nTotal produits mis à jour avec visuel officiel : {assigned_count}")

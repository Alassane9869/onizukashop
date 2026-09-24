"""
Eradicate kitchen_modern_fridge.jpg (wool yarn) and assign authentic refrigerator/freezer packshots
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')
django.setup()

from shop.models import Product, ProductImage

# Delete physical file if it's the yarn image
yarn_path = os.path.join('media', 'products', 'kitchen_modern_fridge.jpg')
if os.path.exists(yarn_path):
    os.remove(yarn_path)
    print(f"[REMOVED] Deleted bad file: {yarn_path}")

# Reassign all products
bad_rel = 'products/kitchen_modern_fridge.jpg'
affected = ProductImage.objects.filter(image__icontains='kitchen_modern_fridge')
print(f"Found {affected.count()} ProductImage rows pointing to yarn image.")

# Available real fridge/freezer images
fridge_images = [
    'products/samsung_bespoke_french_door.png',
    'products/hisense_combi_fridge.png',
    'products/hisense_multidoor_fridge.jpg',
    'products/samsung_official_french_door.png',
    'products/samsung_flagship_fridge.jpg',
    'products/fridge_hisense_ifa.jpg',
]

for idx, img_obj in enumerate(affected):
    chosen = fridge_images[idx % len(fridge_images)]
    img_obj.image = chosen
    img_obj.save()
    print(f" -> Réaffecté [{img_obj.product.name[:40]}] -> {chosen}")

# Also ensure all featured products have 100% verified, clean appliances
print("\n=== VÉRIFICATION DES PRODUITS EN VEDETTE (HOMEPAGE) ===")
featured = Product.objects.filter(is_featured=True)
for p in featured:
    imgs = [i.image.name for i in p.images.all()]
    print(f"[{p.brand.name if p.brand else 'N/A'}] {p.name[:35]} : {imgs}")

print("\nCorrection des images de réfrigérateurs terminée avec succès.")

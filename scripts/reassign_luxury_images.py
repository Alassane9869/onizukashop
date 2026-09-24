import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product, ProductImage

# Mapping of keywords to luxury studio packshots
def pick_image_for_product(name, category_slug, brand_name):
    n = name.lower()
    c = category_slug.lower() if category_slug else ""
    b = brand_name.lower() if brand_name else ""
    
    # 1. Petit Électroménager
    if any(k in n for k in ["cafeti", "expresso", "cafe", "broyeur"]):
        return "products/studio_espresso_coffee.jpg"
    if any(k in n for k in ["micro-onde", "microonde", "neochef", "four micro"]):
        return "products/studio_microwave_inverter.jpg"
    if any(k in n for k in ["robot", "blender", "mixeur", "batteur", "hachoir", "prep'mix", "doubleforce"]):
        return "products/studio_food_processor.jpg"
    if any(k in n for k in ["fontaine", "distributeur d'eau", "eau"]):
        return "products/midea_flagship_ac.jpg" # clean appliance unit
    if any(k in n for k in ["fer a repasser", "fer à repasser", "vapeur"]):
        return "products/studio_food_processor.jpg"
        
    # 2. Cuisinières & Fours
    if any(k in n for k in ["cuisiniere", "cuisinière", "gaziniere", "plaque de cuisson", "feux gaz", "four encastrable"]):
        return "products/stove_modern_gas_range.jpg"
        
    # 3. Réfrigérateurs & Congélateurs
    if any(k in n for k in ["refrigerateur", "réfrigérateur", "frigo", "congelateur", "congélateur"]):
        if "samsung" in b or "samsung" in n:
            return "products/samsung_flagship_fridge.jpg"
        elif "hisense" in b or "hisense" in n:
            return "products/fridge_hisense_ifa.jpg"
        elif "lg" in b or "lg" in n:
            return "products/fridge_samsung_rf24.jpg"
        else:
            return "products/kitchen_modern_fridge.jpg"
            
    # 4. Climatiseurs & Ventilation
    if any(k in n for k in ["climatiseur", "split", "clim", "ventilat", "rafraichisseur"]):
        if "lg" in b or "lg" in n:
            return "products/ac_lg_dual_1.jpg"
        else:
            return "products/midea_flagship_ac.jpg"
            
    # 5. Smart TV & Son
    if any(k in n for k in ["tv", "televiseur", "téléviseur", "oled", "qled", "uhd", "ecran", "soundbar", "barre de son", "speaker", "cinema"]):
        if "lg" in b or "lg" in n:
            return "products/tv_lg_smart.png"
        else:
            return "products/tv_ultra_4k_oled.jpg"
            
    # Default fallback by category
    if "froid" in c or "refrigerateur" in c:
        return "products/samsung_flagship_fridge.jpg"
    elif "climatisation" in c:
        return "products/midea_flagship_ac.jpg"
    elif "televiseur" in c:
        return "products/tv_ultra_4k_oled.jpg"
    elif "cuisiniere" in c:
        return "products/stove_modern_gas_range.jpg"
    else:
        return "products/studio_espresso_coffee.jpg"

updated = 0
for p in Product.objects.all():
    c_slug = p.category.slug if p.category else ""
    b_name = p.brand.name if p.brand else ""
    rel_path = pick_image_for_product(p.name, c_slug, b_name)
    
    # Update all images for this product to point to the clean image
    p.images.all().delete()
    ProductImage.objects.create(
        product=p,
        image=rel_path,
        alt_text=p.name,
        is_primary=True
    )
    updated += 1

print(f"Reassigned luxury studio images to ALL {updated} products!")

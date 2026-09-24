import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product, ProductImage, Category, Brand

IMAGE_MAP = {
    # Category slug or product keywords -> image file
    "fridge_samsung": "products/samsung_flagship_fridge.jpg",
    "fridge_samsung_rf24": "products/fridge_samsung_rf24.jpg",
    "fridge_hisense": "products/fridge_hisense_ifa.jpg",
    "fridge_general": "products/fridge_mabe_double.jpg",
    
    "ac_midea": "products/midea_flagship_ac.jpg",
    "ac_midea_indoor": "products/ac_midea_indoor.jpg",
    "ac_lg": "products/ac_lg_dual_1.jpg",
    "ac_lg_2": "products/ac_lg_dual_2.jpg",
    "ac_gree": "products/ac_gree_ease.jpg",
    "ac_general": "products/ac_hyundai_split.jpg",
    
    "tv_lg": "products/tv_lg_smart.png",
    "tv_sony": "products/tv_sony_bravia.jpg",
    "tv_general": "products/tv_techwood_flat.jpg",
    
    "stove_gas": "products/stove_mabe_gas.jpg",
    "stove_built_in": "products/stove_bic_camera.jpg",
    
    "small_micro": "products/microwave_panasonic.jpg",
}

print(f"Total products in DB: {Product.objects.count()}")

updated_count = 0
for p in Product.objects.all():
    c_slug = p.category.slug if p.category else ""
    b_name = (p.brand.name if p.brand else "").lower()
    p_name = p.name.lower()
    
    img_rel = None
    
    # 1. Refrigerators
    if "refrigerateur" in c_slug or "congelateur" in c_slug or "refrigerateur" in p_name or "congelateur" in p_name:
        if "samsung" in b_name or "samsung" in p_name:
            if "french" in p_name or "side" in p_name or "inverter" in p_name:
                img_rel = IMAGE_MAP["fridge_samsung"]
            else:
                img_rel = IMAGE_MAP["fridge_samsung_rf24"]
        elif "hisense" in b_name or "hisense" in p_name:
            img_rel = IMAGE_MAP["fridge_hisense"]
        else:
            img_rel = IMAGE_MAP["fridge_general"]
            
    # 2. Climatisation
    elif "climatisation" in c_slug or "climatiseur" in p_name or "ventilat" in p_name:
        if "midea" in b_name or "midea" in p_name:
            img_rel = IMAGE_MAP["ac_midea"]
        elif "lg" in b_name or "lg" in p_name:
            img_rel = IMAGE_MAP["ac_lg"]
        elif "gree" in b_name or "gree" in p_name:
            img_rel = IMAGE_MAP["ac_gree"]
        else:
            img_rel = IMAGE_MAP["ac_general"]
            
    # 3. TV & Son
    elif "televiseur" in c_slug or "tv" in p_name or "son" in c_slug or "ecran" in p_name:
        if "lg" in b_name or "lg" in p_name:
            img_rel = IMAGE_MAP["tv_lg"]
        elif "sony" in b_name or "sony" in p_name:
            img_rel = IMAGE_MAP["tv_sony"]
        else:
            img_rel = IMAGE_MAP["tv_general"]
            
    # 4. Cuisinières & Fours
    elif "cuisiniere" in c_slug or "cuisiniere" in p_name or "plaque" in p_name:
        if "encastrable" in p_name or "plaque" in p_name:
            img_rel = IMAGE_MAP["stove_built_in"]
        else:
            img_rel = IMAGE_MAP["stove_gas"]
            
    # 5. Petit Électroménager
    else:
        if "micro-ondes" in p_name or "four" in p_name:
            img_rel = IMAGE_MAP["small_micro"]
        elif "cuisson" in p_name:
            img_rel = IMAGE_MAP["stove_built_in"]
        else:
            img_rel = IMAGE_MAP["small_micro"]
            
    if img_rel:
        # Update or create primary ProductImage
        primary_img = p.images.filter(is_primary=True).first()
        if not primary_img:
            primary_img = p.images.first()
            
        if primary_img:
            primary_img.image = img_rel
            primary_img.is_primary = True
            primary_img.save()
        else:
            ProductImage.objects.create(
                product=p,
                image=img_rel,
                alt_text=p.name,
                is_primary=True
            )
        updated_count += 1

print(f"Successfully updated images for {updated_count} products!")

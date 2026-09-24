import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product

# Reset is_featured
Product.objects.all().update(is_featured=False)

# Target top prestige products for each category
flagship_names = [
    # 1. Samsung French Door Fridge
    "Réfrigérateur Américain Samsung French Door 520L Twin Cooling",
    # 2. Midea Inverter AC
    "Climatiseur Split Midea Inverter 1.5 CV 12000 BTU R410A",
    # 3. LG Smart TV 4K
    "Smart TV LG 55 Pouces 4K UHD ThinQ AI webOS 24",
    # 4. Beko 5-burner gas cooker
    "Cuisinière Beko 5 Feux Gaz 90x60 cm Grande Capacité 112L",
    # 5. LG NeoChef Microwave Mirror
    "Four Micro-Ondes LG NeoChef 25L Smart Inverter Miroir",
    # 6. Philips Espresso Machine
    "Cafetière Expresso Broyeur à Grains Philips Série 2200",
    # 7. LG Dual Inverter AC
    "Climatiseur Split LG Dual Inverter 2 CV 18000 BTU Gold Fin",
    # 8. Moulinex DoubleForce Food Processor
    "Robot Multifonction Moulinex DoubleForce 1000W 31 Fonctions",
]

for name in flagship_names:
    p = Product.objects.filter(name__icontains=name.split()[0]).filter(name__icontains=name.split()[-1]).first()
    if p:
        p.is_featured = True
        p.save()
        print(f"Set featured: {p.name} ({p.primary_image.image.url if p.primary_image else 'NO IMG'})")

# Ensure at least 8 featured products
current_featured = Product.objects.filter(is_featured=True).count()
if current_featured < 8:
    for p in Product.objects.filter(is_featured=False)[:8-current_featured]:
        p.is_featured = True
        p.save()

print(f"Total featured products: {Product.objects.filter(is_featured=True).count()}")

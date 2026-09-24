import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product

# 1. Reset all sale_price to None first
Product.objects.all().update(sale_price=None)

# 2. Select 4 flagship heroes for Flash Sales
deals = [
    # (Category keyword, brand, original, sale)
    ("French Door", "Samsung", 850000, 749000),
    ("Inverter 1.5 CV", "Midea", 320000, 275000),
    ("55 Pouces", "LG", 480000, 399000),
    ("5 Feux Gaz", "Beko", 410000, 345000),
]

for kw, brand, orig, sale in deals:
    p = Product.objects.filter(name__icontains=kw, brand__name__icontains=brand).first()
    if not p:
        p = Product.objects.filter(name__icontains=kw).first()
    if p:
        p.price = orig
        p.sale_price = sale
        p.save()
        print(f"Flash deal: {p.name} | {sale} FCFA (au lieu de {orig} FCFA) -> {p.primary_image.image.url if p.primary_image else 'NO IMG'}")

print(f"Total sale products: {Product.objects.filter(sale_price__isnull=False).count()}")

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from shop.models import Product, Category

# Reset is_new
Product.objects.all().update(is_new=False)

# Pick 1 or 2 premier products from each category to be is_new
categories = Category.objects.all()
for cat in categories:
    prods = Product.objects.filter(category=cat)[:2]
    for p in prods:
        p.is_new = True
        p.save()
        print(f"Set new: [{cat.name}] {p.name} -> {p.primary_image.image.url if p.primary_image else 'NO IMG'}")

print(f"Total new products: {Product.objects.filter(is_new=True).count()}")

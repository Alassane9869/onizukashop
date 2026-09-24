import os
import sys
import random
from datetime import timedelta
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')
django.setup()

from django.utils import timezone
from django.contrib.auth.models import User
from shop.models import Product
from orders.models import Order, OrderItem

# Clients de test à Bamako
customers = [
    {"name": "Moussa Traoré", "phone": "+223 70 00 00 01", "district": "Hamdallaye ACI 2000", "addr": "Rue 312, Porte 45, près de la Bougie"},
    {"name": "Fatoumata Diarra", "phone": "+223 76 12 34 56", "district": "Badalabougou", "addr": "Secteur 3, villa 108"},
    {"name": "Ibrahim Coulibaly", "phone": "+223 65 98 76 54", "district": "Hippodrome", "addr": "Rue 214, face clinique Pasteur"},
    {"name": "Aminata Sanogo", "phone": "+223 79 45 67 89", "district": "Baco-Djicoroni ACI", "addr": "Près du Golf Club, Porte 12"},
    {"name": "Ousmane Keita", "phone": "+223 72 33 44 55", "district": "Sébénikoro", "addr": "Cité Wafi, Rue 40"},
    {"name": "Kadiatou Touré", "phone": "+223 66 11 22 33", "district": "Kalaban Coura", "addr": "Avenue OUA, Immeuble Albarika"},
    {"name": "Modibo Sidibé", "phone": "+223 77 88 99 00", "district": "Faladié SEMA", "addr": "Face marché de Faladié"},
    {"name": "Mariam Koné", "phone": "+223 68 55 44 33", "district": "Torokorobougou", "addr": "Près du pont des Martyrs"},
]

client_user = User.objects.filter(username='client').first()
products = list(Product.objects.filter(is_active=True))

if not products:
    print("No products found to seed orders!")
    exit(0)

statuses = [
    ('pending', 'cash_delivery', False),
    ('pending', 'orange_money', False),
    ('confirmed', 'wave', True),
    ('processing', 'orange_money', True),
    ('shipped', 'cash_delivery', False),
    ('delivered', 'orange_money', True),
    ('delivered', 'wave', True),
    ('delivered', 'cash_delivery', True),
    ('delivered', 'orange_money', True),
    ('delivered', 'bank_transfer', True),
]

now = timezone.now()

Order.objects.all().delete()
print("Cleared old orders.")

for i, (status, p_method, p_status) in enumerate(statuses):
    c = customers[i % len(customers)]
    days_ago = (len(statuses) - 1 - i) * 0.7
    created_date = now - timedelta(days=days_ago, hours=random.randint(1, 12))
    
    order = Order.objects.create(
        user=client_user if i % 3 == 0 else None,
        delivery_name=c['name'],
        delivery_phone=c['phone'],
        delivery_city='Bamako',
        delivery_district=c['district'],
        delivery_address=c['addr'],
        payment_method=p_method,
        payment_status=p_status,
        payment_reference=f"TXN-{random.randint(1000000, 9999999)}" if p_status else "",
        status=status,
        delivery_fee=0,
        subtotal=0,
        total=0,
    )
    # Set created_at explicitly
    Order.objects.filter(pk=order.pk).update(created_at=created_date, updated_at=created_date)
    
    # 1 to 3 items per order
    selected_prods = random.sample(products, k=random.randint(1, min(3, len(products))))
    order_subtotal = 0
    for p in selected_prods:
        qty = random.randint(1, 2)
        item_tot = p.current_price * qty
        order_subtotal += item_tot
        OrderItem.objects.create(
            order=order,
            product=p,
            product_name=p.name,
            product_sku=p.sku,
            quantity=qty,
            unit_price=p.current_price,
            total_price=item_tot
        )
    
    order.subtotal = order_subtotal
    order.total = order_subtotal
    order.save()

print(f"Successfully seeded {len(statuses)} demo orders!")

import os
import sys
from pathlib import Path

# Ajouter la racine du projet
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from shop.models import Category, Product, Brand, ProductImage
from orders.models import Order, OrderItem
from payments.models import Payment
from backoffice.models import ShopSetting

User = get_user_model()

print("=" * 60)
print("ONIZOUKA SHOP - RAPPORT D'AUDIT GLOBAL DU SYSTEME")
print("=" * 60)

print("\n[1] ETAT DES DONNEES ET MODELES")
print(f"  - Utilisateurs : {User.objects.count()} inscrits")
print(f"    * Super-admin IT  : {User.objects.filter(is_superuser=True).count()}")
print(f"    * Membres Staff   : {User.objects.filter(is_staff=True, is_superuser=False).count()}")
print(f"    * Clients standards : {User.objects.filter(is_staff=False, is_superuser=False).count()}")

print(f"\n  - Catalogue Produits :")
print(f"    * Categories : {Category.objects.count()}")
print(f"    * Marques    : {Brand.objects.count()}")
print(f"    * Produits   : {Product.objects.count()} au total")
print(f"      > Actifs     : {Product.objects.filter(is_active=True).count()}")
print(f"      > En stock   : {Product.objects.filter(stock__gt=0).count()}")
print(f"      > En rupture : {Product.objects.filter(stock=0).count()}")
print(f"      > En promo   : {Product.objects.filter(sale_price__isnull=False).count()}")
print(f"    * Photos HD  : {ProductImage.objects.count()} images enregistrées")

print(f"\n  - Commandes & Ventes :")
print(f"    * Commandes totales : {Order.objects.count()}")
print(f"    * Articles commandés: {OrderItem.objects.count()}")
print(f"    * Transactions Pmt  : {Payment.objects.count()}")

print("\n[2] CONFIGURATION CENTRALE (ShopSetting)")
cfg = ShopSetting.get_settings()
print(f"  - Nom commercial  : {cfg.site_name}")
print(f"  - Raison sociale  : {cfg.company_name} (NIF: {cfg.nif} | RCCM: {cfg.rccm})")
print(f"  - Siege social    : {cfg.address}")
print(f"  - Contact officiel: {cfg.phone_contact} (WhatsApp: {cfg.phone_whatsapp})")
print(f"  - Monnaie active  : {cfg.currency}")
print(f"  - Frais livraison : {cfg.default_delivery_fee} FCFA (Gratuit des {cfg.free_delivery_threshold} FCFA)")
print(f"  - Vente Flash     : {'Active' if cfg.flash_sale_active else 'Desactivee'} (Fin: {cfg.flash_sale_end_iso})")

print("\n[3] TESTS D'ACCESSIBILITE ET STATUTS HTTP (Client Web)")
c = Client()
public_endpoints = [
    ('/', 'Page d\'Accueil'),
    ('/catalogue/', 'Catalogue Boutique'),
    ('/panier/', 'Panier d\'achat'),
    ('/contact/', 'Contact & Magasin'),
    ('/accounts/login/', 'Page Connexion (Allauth)'),
    ('/accounts/signup/', 'Page Inscription (Allauth)'),
]

for url, label in public_endpoints:
    resp = c.get(url)
    status = "OK (200)" if resp.status_code == 200 else f"ERREUR ({resp.status_code})"
    print(f"  - {label:24} {url:24} : {status}")

sample_prod = Product.objects.filter(is_active=True).first()
if sample_prod:
    p_url = sample_prod.get_absolute_url()
    p_resp = c.get(p_url)
    status = "OK (200)" if p_resp.status_code == 200 else f"ERREUR ({p_resp.status_code})"
    print(f"  - {'Fiche Produit':24} {p_url:24} : {status}")

sample_cat = Category.objects.first()
if sample_cat:
    cat_url = f"/catalogue/{sample_cat.slug}/"
    cat_resp = c.get(cat_url)
    status = "OK (200)" if cat_resp.status_code == 200 else f"ERREUR ({cat_resp.status_code})"
    print(f"  - {'Filtre Categorie':24} {cat_url:24} : {status}")

print("\n[4] TESTS DE SECURITE & RESTRICTION DU BACKOFFICE")
backoffice_urls = [
    '/gestion/',
    '/gestion/commandes/',
    '/gestion/produits/',
    '/gestion/stocks/',
    '/gestion/utilisateurs/',
    '/gestion/parametres/',
]

print("  A. Test utilisateur Anonyme (Doit bloquer et rediriger vers login):")
for b_url in backoffice_urls:
    resp = c.get(b_url)
    is_safe = resp.status_code in [302, 403]
    state = "SECURISE (Redirection/Interdit)" if is_safe else f"FAILLE ({resp.status_code})"
    print(f"    * {b_url:25} -> {state}")

print("\n  B. Test membre Direction / Staff authentifie:")
staff_user = User.objects.filter(is_staff=True, is_superuser=False).first()
if not staff_user:
    staff_user = User.objects.filter(is_staff=True).first()

if staff_user:
    c.force_login(staff_user)
    for b_url in backoffice_urls:
        resp = c.get(b_url)
        state = "OK (200)" if resp.status_code == 200 else f"ERREUR ({resp.status_code})"
        print(f"    * {b_url:25} -> {state}")
    
    # Verification confidentialite super-admin IT
    user_page = c.get('/gestion/utilisateurs/')
    it_super = User.objects.filter(is_superuser=True).first()
    if it_super and not staff_user.is_superuser:
        has_it_leaked = it_super.username in user_page.content.decode('utf-8', errors='ignore')
        if not has_it_leaked:
            print("    * Confidentialite IT : SECURISE (Le compte Root IT est strictement invisible aux gestionnaires)")
        else:
            print("    * Confidentialite IT : ATTENTION (Le compte Root IT apparait dans la liste)")

print("\n[5] VERIFICATION DU PANIER & DES COMMANDES")
c_anon = Client()
if sample_prod and sample_prod.stock > 0:
    add_resp = c_anon.post(f"/panier/ajouter/{sample_prod.pk}/", {'quantity': 1, 'next': '/panier/'}, follow=True)
    cart_resp = c_anon.get('/panier/')
    in_cart = sample_prod.name[:15] in cart_resp.content.decode('utf-8', errors='ignore')
    print(f"  - Ajout panier visiteur : {'FONCTIONNEL (Produit present)' if in_cart else 'A VERIFIER'}")

print("\n" + "=" * 60)
print("AUDIT TERMINE AVEC SUCCES")
print("=" * 60)

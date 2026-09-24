"""
=============================================================================
ONIZOUKA SHOP - SUITE DE TESTS HAUT NIVEAU ET AUDIT SYSTEME
=============================================================================
Recense tous les types de problemes potentiels :
1. Configuration & Securite (ALLOWED_HOSTS, SSL, CSRF, SECRET_KEY)
2. Connectivite BDD & Latence (SQLite / PostgreSQL)
3. Cache & Sessions
4. Fichiers Statiques & Logos de Paiement (Wave, Orange Money, Cash)
5. Integrite des Donnees (Prix FCFA, Stocks, Categories, Images)
6. Cycle de vie Panier (Ajout, MAJ quantite, Suppression, Calculs)
7. Scanner HTTP des Endpoints (Local, Django Client, ou Prod en direct)

Usage :
  python scripts/test_system_health.py                    # Test interne Django complet
  python scripts/test_system_health.py --remote https://onizouka.danayaplus.com  # Scan HTTP Prod
  python scripts/test_system_health.py --all              # Test interne + Scan Prod
=============================================================================
"""

import os
import sys
import time
import argparse
from pathlib import Path

# Setup Django Environment
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

import django
django.setup()

from django.conf import settings
from django.db import connection
from django.core.cache import cache
from django.contrib.auth.models import User
from shop.models import Product, Category, Brand, ProductImage
from orders.models import Cart, CartItem, Order, Coupon
from shop.views import get_or_create_cart


# Couleurs ANSI pour terminal
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

issues_found = []
warnings_found = []
successes = []

def log_pass(title, details=""):
    print(f"  {GREEN}[SUCCÈS]{RESET} {BOLD}{title}{RESET} {details}", flush=True)
    successes.append(title)

def log_warn(title, details=""):
    print(f"  {YELLOW}[ATTENTION]{RESET} {BOLD}{title}{RESET} : {details}", flush=True)
    warnings_found.append((title, details))

def log_fail(title, details=""):
    print(f"  {RED}[ERREUR]{RESET} {BOLD}{title}{RESET} : {details}", flush=True)
    issues_found.append((title, details))


def section(name):
    print(f"\n{CYAN}{BOLD}{'='*60}{RESET}", flush=True)
    print(f"{CYAN}{BOLD}  {name.upper()}{RESET}", flush=True)
    print(f"{CYAN}{BOLD}{'='*60}{RESET}", flush=True)



def audit_configuration():
    section("1. Configuration & Environnement")
    
    # DEBUG
    if settings.DEBUG:
        log_warn("DEBUG = True", "Active en local. Doit etre False en production pour la securite.")
    else:
        log_pass("DEBUG = False", "(Mode production securise)")

    # ALLOWED_HOSTS
    hosts = settings.ALLOWED_HOSTS
    if '*' in hosts:
        log_pass("ALLOWED_HOSTS", f"{hosts} (Accepte tous les reverse-proxies sans erreur 400 DisallowedHost)")
    elif 'onizouka.danayaplus.com' in hosts:
        log_pass("ALLOWED_HOSTS", f"{hosts} (Domaine de production bien declare)")
    else:
        log_fail("ALLOWED_HOSTS", f"{hosts} -> 'onizouka.danayaplus.com' absent ! Risque d'erreur 400.")

    # Reverse Proxy SSL
    if getattr(settings, 'SECURE_PROXY_SSL_HEADER', None) == ('HTTP_X_FORWARDED_PROTO', 'https'):
        log_pass("SECURE_PROXY_SSL_HEADER", "Correctement configure pour o2switch / Nginx / Passenger.")
    else:
        log_warn("SECURE_PROXY_SSL_HEADER", "Non configure. Les requetes HTTPS reverse-proxy peuvent etre vues en HTTP.")

    # Base de donnees
    db_engine = settings.DATABASES['default']['ENGINE']
    db_name = settings.DATABASES['default']['NAME']
    t0 = time.time()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            cursor.fetchone()
        latency = (time.time() - t0) * 1000
        log_pass(f"Base de donnees ({db_engine.split('.')[-1]})", f"Latence : {latency:.2f}ms | Base : {db_name}")
    except Exception as e:
        log_fail("Connexion BDD", f"Echec de connexion : {e}")

    # Cache
    t0 = time.time()
    try:
        cache.set('test_health_key', 'ok_123', 10)
        val = cache.get('test_health_key')
        latency = (time.time() - t0) * 1000
        if val == 'ok_123':
            log_pass("Systeme de Cache", f"Fonctionnel (Latence : {latency:.2f}ms)")
        else:
            log_warn("Systeme de Cache", "Cache inactif ou Redis injoignable (Repli automatique actif)")
    except Exception as e:
        log_warn("Systeme de Cache", f"Cache indisponible ou degrade ({e})")



def audit_static_and_media():
    section("2. Fichiers Statiques & Logos Paiement")
    
    # Logos de Paiement
    static_root = settings.BASE_DIR / 'static'
    payment_files = [
        ('Wave SVG', static_root / 'images' / 'payments' / 'wave.svg'),
        ('Orange Money SVG', static_root / 'images' / 'payments' / 'orange_money.svg'),
        ('Cash SVG', static_root / 'images' / 'payments' / 'cash.svg'),
        ('CSS Principal', static_root / 'css' / 'main.css'),
    ]

    for label, path in payment_files:
        if path.exists():
            size = path.stat().st_size
            log_pass(f"Asset : {label}", f"Existe ({size} octets)")
        else:
            log_fail(f"Asset : {label}", f"Fichier introuvable à {path}")

    # Media folder
    media_root = Path(settings.MEDIA_ROOT)
    if media_root.exists() and os.access(media_root, os.W_OK):
        log_pass("Dossier Media", f"Accessible en ecriture : {media_root}")
    else:
        log_warn("Dossier Media", f"Dossier inexistant ou en lecture seule : {media_root}")


def audit_data_integrity():
    section("3. Integrite du Catalogue & Prix FCFA")
    
    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    in_stock = Product.objects.filter(is_active=True, stock__gt=0).count()
    
    log_pass(f"Catalogue Produits", f"{total_products} au total ({active_products} actifs, {in_stock} en stock)")

    # Verification des Prix FCFA (Sans virgule, > 0)
    invalid_prices = Product.objects.filter(price__lte=0).count()
    if invalid_prices > 0:
        log_fail("Prix invalides", f"{invalid_prices} produit(s) avec un prix <= 0 FCFA")
    else:
        log_pass("Prix des produits", "Tous les prix sont strictement positifs (> 0 FCFA)")

    # Verification des Promos (sale_price < price)
    from django.db.models import F
    bad_promos = Product.objects.filter(sale_price__isnull=False, sale_price__gte=F('price')).count()
    if bad_promos > 0:
        log_warn("Promotions incoherentes", f"{bad_promos} produit(s) ont un prix promo >= prix normal")
    else:
        log_pass("Promotions", "Toutes les promotions sont coherentes (prix promo < prix initial)")


    # Images des produits actifs
    products_without_images = Product.objects.filter(is_active=True, images__isnull=True).count()
    if products_without_images > 0:
        log_warn("Produits sans image", f"{products_without_images} produit(s) actifs n'ont aucune photo")
    else:
        log_pass("Images Catalogue", "Tous les produits actifs possedent au moins une photo")

    # Categories
    cat_count = Category.objects.filter(is_active=True).count()
    root_cats = Category.objects.filter(is_active=True, parent__isnull=True).count()
    log_pass("Categories", f"{cat_count} categories actives ({root_cats} au menu racine)")

    # Marques
    brand_count = Brand.objects.filter(is_active=True).count()
    log_pass("Marques", f"{brand_count} marques actives (Samsung, Haier, Philips, etc.)")


def audit_cart_lifecycle():
    section("4. Cycle de Vie du Panier & Sessions")
    
    product = Product.objects.filter(is_active=True, stock__gt=2).first()
    if not product:
        log_fail("Test Panier", "Aucun produit actif en stock disponible pour le test")
        return

    import uuid
    test_session_key = f"health_test_{uuid.uuid4().hex[:16]}"
    
    try:
        # Creation panier
        cart = Cart.objects.create(session_key=test_session_key)
        log_pass("Creation Panier", f"ID Panier: {cart.id} lie a la cle session: {test_session_key}")

        # Ajout d'article
        item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 2})
        if created and item.quantity == 2:
            log_pass("Ajout Article", f"{item.quantity}x {product.name} (Sous-total: {item.get_subtotal()} FCFA)")
        else:
            log_fail("Ajout Article", "Echec creation CartItem")

        # Calcul du total
        total = cart.get_total()
        expected = product.current_price * 2
        if total == expected:
            log_pass("Calcul Total Panier", f"{total} FCFA (Exact)")
        else:
            log_fail("Calcul Total Panier", f"Calcule : {total} FCFA != Attendu : {expected} FCFA")


        # WhatsApp URL format
        wa_url = cart.get_whatsapp_cart_url()
        if "22392673799" in wa_url and "Onizouka" in wa_url:
            log_pass("Lien WhatsApp Panier", "Numero officiel +223 92 67 37 99 et recapitulatif conformes")
        else:
            log_fail("Lien WhatsApp Panier", f"URL incorrecte : {wa_url[:60]}...")

        # Nettoyage
        cart.delete()
        log_pass("Nettoyage Panier Test", "Panier et articles temporaires supprimes proprement")

    except Exception as e:
        log_fail("Test Panier Exception", f"Erreur critique lors du test du panier : {e}")


def audit_http_endpoints_internal():
    section("5. Diagnostic HTTP Interne (Django Test Client)")
    from django.test import Client
    client = Client()

    product = Product.objects.filter(is_active=True).first()
    product_slug = product.slug if product else "test"
    product_id = product.id if product else 1

    routes_to_test = [
        ("Accueil", "/", 200, "GET"),
        ("Catalogue", "/catalogue/", 200, "GET"),
        ("Recherche", "/recherche/?q=samsung", 200, "GET"),
        ("Fiche Produit", f"/produit/{product_slug}/", 200, "GET"),
        ("Panier (GET)", "/panier/", 200, "GET"),
        ("Ajout Panier (POST)", f"/panier/ajouter/{product_id}/", [200, 302], "POST", {'quantity': 1}),
        ("Ajout Panier (GET fallback)", f"/panier/ajouter/{product_id}/", [200, 302], "GET"),
        ("Commande (Redirection Login)", "/panier/commander/", 302, "GET"),
        ("Contact", "/contact/", 200, "GET"),
        ("Portail Direction", "/gestion/", 302, "GET"),
        ("Admin Root", "/admin/", 302, "GET"),
    ]

    for entry in routes_to_test:
        label = entry[0]
        url = entry[1]
        expected_status = entry[2]
        method = entry[3]
        data = entry[4] if len(entry) > 4 else None

        t0 = time.time()
        try:
            # secure=True pour simuler HTTPS et ne pas declencher SECURE_SSL_REDIRECT
            if method == 'POST':
                resp = client.post(url, data or {}, secure=True)
            else:
                resp = client.get(url, secure=True)
            duration = (time.time() - t0) * 1000

            valid = resp.status_code == expected_status if isinstance(expected_status, int) else resp.status_code in expected_status
            if valid:
                log_pass(f"{method} {url} [{label}]", f"HTTP {resp.status_code} ({duration:.1f}ms)")
            else:
                log_fail(f"{method} {url} [{label}]", f"HTTP {resp.status_code} (Attendu: {expected_status})")
        except Exception as e:
            log_fail(f"{method} {url} [{label}]", f"Exception non interceptee : {e}")


def audit_remote_endpoints(base_url):
    section(f"6. Scan HTTP Live Réseau : {base_url}")
    import urllib.request
    import urllib.error

    product = Product.objects.filter(is_active=True).first()
    product_slug = product.slug if product else "test"
    product_id = product.id if product else 1

    urls = [
        ("Accueil", f"{base_url}/"),
        ("Catalogue", f"{base_url}/catalogue/"),
        ("Fiche Produit", f"{base_url}/produit/{product_slug}/"),
        ("Panier (GET)", f"{base_url}/panier/"),
        ("Ajouter au Panier (GET/POST)", f"{base_url}/panier/ajouter/{product_id}/"),
        ("Contact", f"{base_url}/contact/"),
        ("Livraison & Garantie", f"{base_url}/livraison-garantie/"),
        ("Mentions Legales", f"{base_url}/mentions-legales/"),
        ("Portail Gestion", f"{base_url}/gestion/"),
    ]


    for label, full_url in urls:
        t0 = time.time()
        req = urllib.request.Request(
            full_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) OnizoukaHealthScanner/1.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
        )
        try:
            res = urllib.request.urlopen(req, timeout=10)
            latency = (time.time() - t0) * 1000
            log_pass(f"{label} -> {full_url}", f"HTTP {res.status} ({latency:.1f}ms)")
        except urllib.error.HTTPError as e:
            latency = (time.time() - t0) * 1000
            if e.code in [301, 302]:
                log_pass(f"{label} -> {full_url}", f"HTTP {e.code} Redirection ({latency:.1f}ms)")
            elif e.code == 400:
                log_fail(f"{label} -> {full_url}", f"HTTP 400 Bad Request ! (Verifier ALLOWED_HOSTS ou Session)")
            elif e.code == 403:
                log_fail(f"{label} -> {full_url}", f"HTTP 403 Interdit ! (Erreur CSRF ou Permissions)")
            elif e.code == 404:
                log_warn(f"{label} -> {full_url}", f"HTTP 404 Page introuvable")
            elif e.code == 500:
                log_fail(f"{label} -> {full_url}", f"HTTP 500 Erreur Interne Serveur !")
            else:
                log_warn(f"{label} -> {full_url}", f"HTTP {e.code}")
        except Exception as e:
            log_fail(f"{label} -> {full_url}", f"Echec de connexion : {e}")


def print_summary():
    print(f"\n{CYAN}{BOLD}{'='*60}{RESET}", flush=True)
    print(f"{CYAN}{BOLD}  BILAN DU DIAGNOSTIC COMPLET ONIZOUKA SHOP{RESET}", flush=True)
    print(f"{CYAN}{BOLD}{'='*60}{RESET}", flush=True)
    print(f"  {GREEN}Tests Reussis  : {len(successes)}{RESET}", flush=True)
    print(f"  {YELLOW}Avertissements : {len(warnings_found)}{RESET}", flush=True)
    print(f"  {RED}Erreurs / Bugs : {len(issues_found)}{RESET}", flush=True)

    if issues_found:
        print(f"\n{RED}{BOLD}DETAILS DES ANOMALIES A CORRIGER :{RESET}", flush=True)
        for idx, (title, details) in enumerate(issues_found, 1):
            print(f"  {idx}. {BOLD}{title}{RESET} : {details}", flush=True)
    else:
        print(f"\n{GREEN}{BOLD}TOUS LES SYSTEMES SONT 100% FONCTIONNELS ET VALIDES !{RESET}", flush=True)
    print(f"{CYAN}{BOLD}{'='*60}{RESET}\n", flush=True)



def main():
    parser = argparse.ArgumentParser(description="Audit et suite de tests de haut niveau Onizouka Shop")
    parser.add_argument('--remote', help="URL de base pour tester le serveur distant (ex: https://onizouka.danayaplus.com)")
    parser.add_argument('--all', action='store_true', help="Execute le test complet local + scan distant")
    args = parser.parse_args()

    audit_configuration()
    audit_static_and_media()
    audit_data_integrity()
    audit_cart_lifecycle()
    audit_http_endpoints_internal()

    remote_url = args.remote
    if args.all and not remote_url:
        remote_url = "https://onizouka.danayaplus.com"

    if remote_url:
        audit_remote_endpoints(remote_url)

    print_summary()

    if issues_found:
        sys.exit(1)

if __name__ == '__main__':
    main()

"""
ONIZOUKA SHOP - Commande pour initialiser des données de démo ultra-réalistes
"""
from django.core.management.base import BaseCommand
from shop.models import Category, Brand, Product
from orders.models import Coupon


class Command(BaseCommand):
    help = "Initialise les catégories, marques, produits et coupons de démonstration"

    def handle(self, *args, **options):
        self.stdout.write("Initialisation des données de démonstration...")

        # 1. Marques
        brands_data = [
            {'name': 'Samsung', 'slug': 'samsung'},
            {'name': 'LG Electronics', 'slug': 'lg'},
            {'name': 'Hisense', 'slug': 'hisense'},
            {'name': 'TCL', 'slug': 'tcl'},
            {'name': 'Midea', 'slug': 'midea'},
            {'name': 'Beko', 'slug': 'beko'},
        ]
        brands = {}
        for b in brands_data:
            obj, _ = Brand.objects.get_or_create(slug=b['slug'], defaults={'name': b['name'], 'is_active': True})
            brands[b['slug']] = obj

        # 2. Catégories
        categories_data = [
            {'name': 'Réfrigérateurs & Congélateurs', 'slug': 'refrigerateurs', 'icon': 'fridge', 'order': 1},
            {'name': 'Climatisation & Ventilation', 'slug': 'climatisation', 'icon': 'air-conditioner', 'order': 2},
            {'name': 'Téléviseurs & Son', 'slug': 'televiseurs', 'icon': 'tv', 'order': 3},
            {'name': 'Cuisinières & Fours', 'slug': 'cuisinieres', 'icon': 'stove', 'order': 4},
            {'name': 'Petit Électroménager', 'slug': 'petit-electromenager', 'icon': 'blender', 'order': 5},
        ]
        categories = {}
        for c in categories_data:
            obj, _ = Category.objects.get_or_create(
                slug=c['slug'],
                defaults={'name': c['name'], 'icon': c['icon'], 'order': c['order'], 'is_active': True}
            )
            categories[c['slug']] = obj

        # 3. Produits
        products_data = [
            {
                'name': 'Réfrigérateur Combiné Samsung No Frost 385L',
                'slug': 'refrigerateur-combine-samsung-385l',
                'sku': 'SAM-RF-385NF',
                'category': categories['refrigerateurs'],
                'brand': brands['samsung'],
                'short_description': 'Froid ventilé intégral Multi Flow, compresseur Digital Inverter garanti 10 ans.',
                'description': 'Ce réfrigérateur Samsung offre une capacité de 385 litres avec technologie No Frost évitant le givre. Économe en énergie et conçu pour résister aux variations de tension électrique fréquentes en Afrique de l\'Ouest.',
                'price': 525000,
                'sale_price': 485000,
                'cost_price': 400000,
                'stock': 12,
                'is_featured': True,
                'is_new': True,
                'specifications': {
                    'Capacité': '385 Litres',
                    'Technologie': 'No Frost (Ventilé)',
                    'Compresseur': 'Digital Inverter',
                    'Classe énergétique': 'A+',
                    'Couleur': 'Inox Métallisé',
                    'Tension': '220-240V / 50Hz (Protection surtension)'
                }
            },
            {
                'name': 'Climatiseur Split Midea Inverter 1.5 CV R32',
                'slug': 'climatiseur-split-midea-inverter-1-5cv',
                'sku': 'MID-AC-15CV',
                'category': categories['climatisation'],
                'brand': brands['midea'],
                'short_description': 'Refroidissement ultra-rapide Tropical Inverter avec traitement anti-corrosion Gold Fin.',
                'description': 'Idéal pour le climat chaud de Bamako, le climatiseur Midea Tropicalisé résiste jusqu\'à 55°C extérieur. Sa technologie Inverter permet d\'économiser jusqu\'à 60% d\'énergie électrique.',
                'price': 310000,
                'sale_price': 275000,
                'cost_price': 230000,
                'stock': 18,
                'is_featured': True,
                'is_new': True,
                'specifications': {
                    'Puissance': '1.5 CV (12000 BTU)',
                    'Gaz réfrigérant': 'R32 Écologique',
                    'Technologie': 'Tropical Inverter Quattros',
                    'Filtre': 'Haute densité anti-poussière',
                    'Garantie compresseur': '5 ans'
                }
            },
            {
                'name': 'Smart TV LG 55 pouces 4K UHD ThinQ AI',
                'slug': 'smart-tv-lg-55-pouces-4k-uhd',
                'sku': 'LG-TV-55UQ80',
                'category': categories['televiseurs'],
                'brand': brands['lg'],
                'short_description': 'Téléviseur intelligent webOS, processeur α5 Gen5 AI 4K, HDR10 Pro.',
                'description': 'Plongez dans des images 4K époustouflantes avec la Smart TV LG 55". Accédez facilement à YouTube, Netflix, Prime Video et profitez de la télécommande magique Magic Remote incluse.',
                'price': 420000,
                'sale_price': 380000,
                'cost_price': 320000,
                'stock': 9,
                'is_featured': True,
                'is_new': False,
                'specifications': {
                    'Taille écran': '55 pouces (139 cm)',
                    'Résolution': '4K Ultra HD (3840 x 2160)',
                    'Système': 'webOS 22',
                    'Connectivité': '3x HDMI 2.0, 2x USB, Wi-Fi, Bluetooth',
                    'Audio': '20W Ultra Surround'
                }
            },
            {
                'name': 'Cuisinière Beko 4 Feux Gaz avec Four Électrique 60x60',
                'slug': 'cuisiniere-beko-4-feux-gaz-four-electrique',
                'sku': 'BEK-CS-4F60',
                'category': categories['cuisinieres'],
                'brand': brands['beko'],
                'short_description': 'Brûleurs haute efficacité, sécurité thermocouple et four multifonction.',
                'description': 'Cuisinez pour toute la famille en toute sérénité grâce à la cuisinière Beko en acier inoxydable. Brûleurs puissants à allumage intégré et four avec chaleur tournante.',
                'price': 240000,
                'sale_price': None,
                'cost_price': 185000,
                'stock': 7,
                'is_featured': False,
                'is_new': False,
                'specifications': {
                    'Configuration': '4 feux gaz + four combiné',
                    'Dimensions': '60 x 60 x 85 cm',
                    'Sécurité': 'Thermocouple coupe-gaz',
                    'Finition': 'Inox résistant aux rayures'
                }
            },
            {
                'name': 'Congélateur Coffre Hisense 250 Litres Tropicalisé',
                'slug': 'congelateur-coffre-hisense-250l',
                'sku': 'HIS-CC-250T',
                'category': categories['refrigerateurs'],
                'brand': brands['hisense'],
                'short_description': 'Super congélation rapide, isolation thermique renforcée en cas de coupure.',
                'description': 'Conservez vos denrées jusqu\'à 36 heures sans électricité grâce à l\'isolation thermique extra-épaisse de ce congélateur coffre Hisense, parfait pour un usage domestique ou commercial.',
                'price': 225000,
                'sale_price': 199000,
                'cost_price': 160000,
                'stock': 15,
                'is_featured': True,
                'is_new': True,
                'specifications': {
                    'Volume': '250 Litres',
                    'Autonomie coupure': 'Jusqu\'à 36h',
                    'Panier amovible': 'Inclus',
                    'Serrure': 'Clé incluse'
                }
            },
            {
                'name': 'Smart TV TCL 43 pouces FHD Android TV',
                'slug': 'smart-tv-tcl-43-pouces-fhd-android',
                'sku': 'TCL-TV-43S54',
                'category': categories['televiseurs'],
                'brand': brands['tcl'],
                'short_description': 'Écran sans bordure métallique, Dolby Audio et Chromecast intégré.',
                'description': 'Une TV moderne et compacte avec Google Play Store, commande vocale Google Assistant et qualité d\'affichage Full HD aux couleurs vives.',
                'price': 195000,
                'sale_price': 175000,
                'cost_price': 140000,
                'stock': 20,
                'is_featured': False,
                'is_new': True,
                'specifications': {
                    'Taille écran': '43 pouces (108 cm)',
                    'Résolution': 'Full HD 1080p',
                    'Système': 'Android TV avec Google Play',
                    'Connectivité': 'Wi-Fi, Bluetooth, HDMI, USB'
                }
            }
        ]

        for p_data in products_data:
            Product.objects.get_or_create(
                slug=p_data['slug'],
                defaults=p_data
            )

        # 4. Coupons
        Coupon.objects.get_or_create(
            code='BIENVENUE10',
            defaults={
                'discount_type': 'percent',
                'discount_value': 10,
                'min_order_amount': 50000,
                'max_uses': 100,
                'is_active': True,
            }
        )
        Coupon.objects.get_or_create(
            code='ONIZOUKA5000',
            defaults={
                'discount_type': 'fixed',
                'discount_value': 5000,
                'min_order_amount': 100000,
                'max_uses': 50,
                'is_active': True,
            }
        )

        self.stdout.write(self.style.SUCCESS("Données de démo créées avec succès !"))

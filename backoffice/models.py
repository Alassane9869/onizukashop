"""
ONIZOUKA SHOP - Modèles du Backoffice & Paramètres Direction
"""
from django.db import models


class ShopSetting(models.Model):
    """Configuration centrale de la boutique et paramètres opérationnels de l'entreprise."""

    # Entreprise & Siège Bamako
    site_name = models.CharField("Nom de la boutique", max_length=150, default="ONIZOUKA SHOP")
    company_name = models.CharField("Raison sociale légale", max_length=200, default="ONIZOUKA SHOP SARL")
    nif = models.CharField("Numéro d'Identification Fiscale (NIF)", max_length=100, blank=True, default="085123456M")
    rccm = models.CharField("Registre du Commerce (RCCM)", max_length=100, blank=True, default="MA-BKO-2024-B-12345")
    address = models.CharField(
        "Adresse Boutique", 
        max_length=255, 
        default="Grand Marché de Bamako, Dabanani, Bamako, Mali"
    )
    phone_contact = models.CharField("Téléphone Service Client", max_length=50, default="+223 92 67 37 99")
    phone_whatsapp = models.CharField("WhatsApp Commercial", max_length=50, default="+223 92 67 37 99")
    email_contact = models.EmailField("Email officiel", default="contact@onizoukashop.com")
    email_orders = models.EmailField("Email alertes commandes Direction", default="direction@onizoukashop.com")

    # Logistique & Livraison
    currency = models.CharField("Devise", max_length=10, default="FCFA")
    default_delivery_fee = models.DecimalField(
        "Frais de livraison forfaitaires Bamako (FCFA)", 
        max_digits=10, 
        decimal_places=0, 
        default=2000
    )
    free_delivery_threshold = models.DecimalField(
        "Seuil de livraison gratuite (FCFA)", 
        max_digits=12, 
        decimal_places=0, 
        default=500000
    )
    delivery_delay_text = models.CharField("Délai moyen affiché", max_length=100, default="Sous 24h ouvrées")
    store_pickup_active = models.BooleanField("Activer retrait gratuit magasin 15 min", default=True)

    # Moyens de Paiement
    orange_money_number = models.CharField("Numéro / Code Marchand Orange Money", max_length=50, default="+223 92 67 37 99")
    wave_number = models.CharField("Numéro Wave Mobile Money", max_length=50, default="+223 92 67 37 99")
    cash_on_delivery_active = models.BooleanField("Activer le paiement en espèces à la livraison", default=True)

    # Gestion des Stocks
    default_min_stock_alert = models.PositiveIntegerField("Seuil alerte rupture par défaut", default=5)
    block_order_on_out_of_stock = models.BooleanField("Bloquer l'achat si rupture de stock", default=True)

    # Notifications & Emails
    email_notifications_active = models.BooleanField("Envoyer les emails automatiques aux clients", default=True)
    whatsapp_notifications_active = models.BooleanField("Activer les alertes rapides WhatsApp", default=True)

    # Campagnes Commerciales & Ventes Flash (Page d'accueil)
    flash_sale_active = models.BooleanField("Activer la section Ventes Flash sur l'accueil", default=True)
    flash_sale_title = models.CharField("Titre de la Vente Flash", max_length=150, default="Ventes Flash de la Semaine")
    flash_sale_subtitle = models.CharField("Sous-titre descriptif", max_length=255, default="Tarifs remisés disponibles immédiatement en stock à Bamako")
    flash_sale_end_date = models.DateTimeField("Date et heure de fin du compte à rebours", null=True, blank=True)

    # Intégration Meta Business / Facebook Ads & Tracking
    meta_pixel_id = models.CharField(
        "ID Pixel Facebook (Meta)", 
        max_length=50, 
        blank=True, 
        default="",
        help_text="Identifiant numérique Meta Pixel à 15-16 chiffres fourni par Meta Events Manager"
    )
    meta_domain_verification = models.CharField(
        "Code de vérification de domaine Meta", 
        max_length=100, 
        blank=True, 
        default="",
        help_text="Code meta name='facebook-domain-verification' fourni par Meta Business Suite"
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paramètres de la Boutique"
        verbose_name_plural = "Paramètres de la Boutique"

    def __str__(self):
        return f"Configuration {self.site_name} (Mise à jour: {self.updated_at.strftime('%d/%m/%Y')})"

    @classmethod
    def get_settings(cls):
        """Récupère l'unique configuration ou la crée avec les valeurs d'origine."""
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    @property
    def whatsapp_raw(self):
        """Format épuré pour lien wa.me (ex: 22392673799)"""
        import re
        clean = re.sub(r'[^0-9]', '', str(self.phone_whatsapp or '22392673799'))
        return clean or '22392673799'

    @property
    def whatsapp(self):
        return self.phone_whatsapp or '+223 92 67 37 99'

    @property
    def phone(self):
        return self.phone_contact or '+223 92 67 37 99'

    @property
    def flash_sale_end_iso(self):
        """Format ISO 8601 pour JavaScript (ex: 2026-09-30T23:59:59)."""
        if self.flash_sale_end_date:
            return self.flash_sale_end_date.strftime("%Y-%m-%dT%H:%M:%S")
        from django.utils import timezone
        from datetime import timedelta
        # Si date non renseignée, fin dans 3 jours à 23:59
        now = timezone.now()
        future = now + timedelta(days=3)
        return future.strftime("%Y-%m-%dT23:59:59")

"""
ONIZOUKA SHOP - Modeles de donnees
App: shop
Contient: Category, Brand, Product, ProductImage, Review
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from mptt.models import MPTTModel, TreeForeignKey
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill


class Category(MPTTModel):
    """Categories hierarchiques (arbre infini avec MPTT)"""
    name = models.CharField(max_length=200, verbose_name='Nom')
    slug = models.SlugField(max_length=200, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children', verbose_name='Categorie parente')
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name='Image')
    description = models.TextField(blank=True, verbose_name='Description')
    icon = models.CharField(max_length=50, blank=True, help_text='Material Icons name', verbose_name='Icone')
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta titre SEO')
    meta_description = models.TextField(max_length=500, blank=True, verbose_name='Meta description SEO')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordre')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['order', 'name']

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:category', kwargs={'slug': self.slug})

    def get_products_count(self):
        return self.products.filter(is_active=True).count()

    @property
    def short_name(self):
        """Nom concis style Apple pour les barres de navigation"""
        short_map = {
            'refrigerateurs': 'Réfrigérateurs',
            'climatisation': 'Climatiseurs',
            'televiseurs': 'Smart TV',
            'cuisinieres': 'Cuisinières',
            'congelateurs': 'Congélateurs',
            'petit-electromenager': 'Petit Électro',
        }
        for key, val in short_map.items():
            if key in self.slug:
                return val
        if '&' in self.name:
            return self.name.split('&')[0].strip()
        return self.name


class Brand(models.Model):
    """Marques des produits (Samsung, LG, Haier, etc.)"""
    name = models.CharField(max_length=100, verbose_name='Nom')
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='brands/', blank=True, verbose_name='Logo')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Produit electronique (frigo, clim, TV, etc.)"""

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Actif'
        INACTIVE = 'inactive', 'Inactif'
        OUT_OF_STOCK = 'out_of_stock', 'Rupture de stock'
        COMING_SOON = 'coming_soon', 'Prochainement'

    # Infos de base
    name = models.CharField(max_length=300, verbose_name='Nom du produit')
    slug = models.SlugField(max_length=300, unique=True, verbose_name='URL slug')
    sku = models.CharField(max_length=100, unique=True, verbose_name='Reference SKU')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products',
                                 verbose_name='Categorie')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='products', verbose_name='Marque')

    # Description
    short_description = models.TextField(max_length=500, blank=True, verbose_name='Description courte')
    description = models.TextField(verbose_name='Description complete')
    specifications = models.JSONField(default=dict, blank=True,
                                      help_text='Specs techniques en JSON {"Capacite": "350L", "Classe": "A+++"}',
                                      verbose_name='Specifications techniques')

    # Prix
    price = models.DecimalField(max_digits=12, decimal_places=0,
                                validators=[MinValueValidator(0)],
                                verbose_name='Prix normal (FCFA)')
    sale_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True,
                                     validators=[MinValueValidator(0)],
                                     verbose_name='Prix promo (FCFA)')
    cost_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True,
                                     validators=[MinValueValidator(0)],
                                     verbose_name='Prix de revient (FCFA)')

    # Stock
    stock = models.PositiveIntegerField(default=0, verbose_name='Quantite en stock')
    min_stock = models.PositiveIntegerField(default=5, verbose_name='Stock minimum (alerte)')
    track_stock = models.BooleanField(default=True, verbose_name='Gerer le stock')

    # Caracteristiques physiques
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                                 verbose_name='Poids (kg)')
    dimensions = models.CharField(max_length=100, blank=True,
                                  help_text='LxlxH en cm', verbose_name='Dimensions')

    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name='Meta titre SEO')
    meta_description = models.TextField(max_length=500, blank=True, verbose_name='Meta description SEO')

    # Statut et dates
    status = models.CharField(max_length=20, choices=Status.choices,
                               default=Status.ACTIVE, verbose_name='Statut')
    is_active = models.BooleanField(default=True, verbose_name='Visible')
    is_featured = models.BooleanField(default=False, verbose_name='Produit vedette')
    is_new = models.BooleanField(default=True, verbose_name='Nouveau')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date creation')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Derniere modif')

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['stock']),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            import uuid
            self.sku = f'ONZ-{uuid.uuid4().hex[:8].upper()}'
        # Mettre a jour le statut selon le stock
        if self.track_stock and self.stock == 0:
            self.status = self.Status.OUT_OF_STOCK
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('shop:product', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        """Retourne le prix actuel (promo ou normal)"""
        if self.sale_price and self.sale_price < self.price:
            return self.sale_price
        return self.price

    @property
    def discount_percentage(self):
        """Calcule le pourcentage de remise"""
        if self.sale_price and self.sale_price < self.price:
            discount = ((self.price - self.sale_price) / self.price) * 100
            return int(discount)
        return 0

    @property
    def is_on_sale(self):
        return bool(self.sale_price and self.sale_price < self.price)

    @property
    def is_in_stock(self):
        if not self.track_stock:
            return True
        return self.stock > 0

    @property
    def is_low_stock(self):
        return self.track_stock and 0 < self.stock <= self.min_stock

    @property
    def primary_image(self):
        """Retourne l'image principale du produit"""
        img = self.images.filter(is_primary=True).first()
        if not img:
            img = self.images.first()
        return img

    def get_average_rating(self):
        reviews = self.reviews.filter(is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    def get_reviews_count(self):
        return self.reviews.filter(is_approved=True).count()

    def get_formatted_price(self):
        return f"{int(self.current_price):,} FCFA".replace(",", " ")

    def get_specifications_list(self):
        """Retourne les specs comme liste de tuples"""
        return list(self.specifications.items())


class ProductImage(models.Model):
    """Images des produits (plusieurs par produit)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images', verbose_name='Produit')
    image = models.ImageField(upload_to='products/', verbose_name='Image')

    # Versions optimisees automatiques via django-imagekit
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(300, 300)],
                               format='WEBP',
                               options={'quality': 85})
    medium = ImageSpecField(source='image',
                            processors=[ResizeToFit(600, 600)],
                            format='WEBP',
                            options={'quality': 90})
    large = ImageSpecField(source='image',
                           processors=[ResizeToFit(1200, 1200)],
                           format='WEBP',
                           options={'quality': 92})

    alt_text = models.CharField(max_length=200, blank=True, verbose_name='Texte alternatif')
    is_primary = models.BooleanField(default=False, verbose_name='Image principale')
    order = models.PositiveIntegerField(default=0, verbose_name='Ordre')

    class Meta:
        verbose_name = 'Image produit'
        verbose_name_plural = 'Images produits'
        ordering = ['-is_primary', 'order']

    def __str__(self):
        return f"Image de {self.product.name}"

    def save(self, *args, **kwargs):
        # Si c'est la premiere image, la definir comme principale
        if not self.pk and not self.product.images.exists():
            self.is_primary = True
        # Une seule image principale par produit
        if self.is_primary:
            self.product.images.exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)


class Review(models.Model):
    """Avis et notes des clients sur les produits"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='reviews', verbose_name='Produit')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='reviews', verbose_name='Client')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='Note (1-5)'
    )
    title = models.CharField(max_length=200, verbose_name='Titre de l\'avis')
    body = models.TextField(verbose_name='Contenu de l\'avis')
    is_verified = models.BooleanField(default=False, verbose_name='Achat verifie')
    is_approved = models.BooleanField(default=True, verbose_name='Approuve')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Avis'
        verbose_name_plural = 'Avis'
        ordering = ['-created_at']
        unique_together = ['product', 'user']  # Un avis par produit par client

    def __str__(self):
        return f"Avis de {self.user.get_full_name()} sur {self.product.name} ({self.rating}/5)"

    def get_stars_range(self):
        return range(self.rating)

    def get_empty_stars_range(self):
        return range(5 - self.rating)


class Wishlist(models.Model):
    """Favoris et coups de cœur des clients"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items', verbose_name='Client')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlist_entries', verbose_name='Appareil favori')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favori'
        verbose_name_plural = 'Favoris'
        unique_together = ['user', 'product']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ♥ {self.product.name}"
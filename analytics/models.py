"""
ONIZOUKA SHOP - Modeles Analytics
App: analytics
"""
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class ProductView(models.Model):
    """Vue d'un produit (tracking)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='views_log')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vue produit'
        verbose_name_plural = 'Vues produits'
        ordering = ['-viewed_at']

    def __str__(self):
        return f'Vue {self.product.name} - {self.viewed_at:%d/%m/%Y}'


class SearchQuery(models.Model):
    """Requetes de recherche (analytics)"""
    query = models.CharField(max_length=300, verbose_name='Recherche')
    results_count = models.PositiveIntegerField(default=0, verbose_name='Nb resultats')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_key = models.CharField(max_length=40, blank=True)
    searched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recherche'
        verbose_name_plural = 'Recherches'
        ordering = ['-searched_at']

    def __str__(self):
        return f'"{self.query}" ({self.results_count} resultats)'


class DailyStat(models.Model):
    """Statistiques journalieres du site"""
    date = models.DateField(unique=True, verbose_name='Date')
    visitors = models.PositiveIntegerField(default=0, verbose_name='Visiteurs')
    page_views = models.PositiveIntegerField(default=0, verbose_name='Pages vues')
    orders_count = models.PositiveIntegerField(default=0, verbose_name='Commandes')
    revenue = models.DecimalField(max_digits=14, decimal_places=0, default=0, verbose_name='Chiffre d\'affaires (FCFA)')
    new_users = models.PositiveIntegerField(default=0, verbose_name='Nouveaux inscrits')

    class Meta:
        verbose_name = 'Statistique journaliere'
        verbose_name_plural = 'Statistiques journalieres'
        ordering = ['-date']

    def __str__(self):
        return f'Stats {self.date} - {int(self.revenue):,} FCFA'.replace(',', ' ')

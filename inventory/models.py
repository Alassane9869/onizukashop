"""
ONIZOUKA SHOP - Gestion du Stock
App: inventory
"""
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Supplier(models.Model):
    """Fournisseur"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    contact_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fournisseur"
        verbose_name_plural = "Fournisseurs"

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    """Mouvement de stock (entree/sortie)"""

    class MovementType(models.TextChoices):
        IN = 'in', 'Entree stock'
        OUT = 'out', 'Sortie stock'
        ADJUSTMENT = 'adjustment', 'Ajustement'
        RETURN = 'return', 'Retour client'

    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='stock_movements', verbose_name="Produit")
    movement_type = models.CharField(max_length=20, choices=MovementType.choices, verbose_name="Type")
    quantity = models.IntegerField(verbose_name="Quantite")
    stock_before = models.IntegerField(verbose_name="Stock avant")
    stock_after = models.IntegerField(verbose_name="Stock apres")
    unit_cost = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True,
                                    verbose_name="Cout unitaire (FCFA)")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    reference = models.CharField(max_length=200, blank=True, verbose_name="Reference (bon, commande...)")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mouvement de stock"
        verbose_name_plural = "Mouvements de stock"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.product.name} ({self.quantity})"
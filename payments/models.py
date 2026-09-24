"""
ONIZOUKA SHOP - Paiements
App: payments
"""
from django.db import models
from orders.models import Order


class Payment(models.Model):
    """Enregistrement d un paiement"""

    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        COMPLETED = 'completed', 'Complete'
        FAILED = 'failed', 'Echoue'
        REFUNDED = 'refunded', 'Rembourse'

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    method = models.CharField(max_length=30, verbose_name="Methode")
    amount = models.DecimalField(max_digits=12, decimal_places=0)
    currency = models.CharField(max_length=10, default='FCFA')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    transaction_id = models.CharField(max_length=200, blank=True, verbose_name="ID Transaction")
    provider_reference = models.CharField(max_length=200, blank=True)
    raw_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Paiement {self.method} - {self.amount} FCFA - {self.get_status_display()}"
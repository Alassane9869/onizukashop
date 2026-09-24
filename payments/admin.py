"""
ONIZOUKA SHOP - Admin Paiements
"""
from django.contrib import admin
from unfold.admin import ModelAdmin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    list_display = ['id', 'order', 'method', 'amount', 'status', 'transaction_id', 'created_at']
    list_filter = ['status', 'method', 'created_at']
    search_fields = ['order__order_number', 'transaction_id', 'provider_reference']
    readonly_fields = ['created_at', 'updated_at', 'raw_response']
    ordering = ['-created_at']

    fieldsets = (
        ('Commande', {
            'fields': ('order',)
        }),
        ('Paiement', {
            'fields': ('method', 'amount', 'currency', 'status')
        }),
        ('References', {
            'fields': ('transaction_id', 'provider_reference', 'raw_response'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

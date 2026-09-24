"""
ONIZOUKA SHOP - Admin Inventaire
"""
from django.contrib import admin
from unfold.admin import ModelAdmin
from inventory.models import Supplier, StockMovement


@admin.register(Supplier)
class SupplierAdmin(ModelAdmin):
    list_display = ['name', 'contact_name', 'phone', 'email', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'contact_name', 'phone', 'email']
    list_editable = ['is_active']


@admin.register(StockMovement)
class StockMovementAdmin(ModelAdmin):
    list_display = [
        'product', 'movement_type', 'quantity',
        'stock_before', 'stock_after', 'supplier',
        'reference', 'created_by', 'created_at'
    ]
    list_filter = ['movement_type', 'created_at', 'supplier']
    search_fields = ['product__name', 'reference', 'product__sku']
    readonly_fields = ['stock_before', 'stock_after', 'created_at']
    autocomplete_fields = ['product']
    ordering = ['-created_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            obj.stock_before = obj.product.stock
            # Calculer le stock apres
            if obj.movement_type == 'in' or obj.movement_type == 'return':
                obj.stock_after = obj.stock_before + obj.quantity
            elif obj.movement_type == 'out':
                obj.stock_after = max(0, obj.stock_before - obj.quantity)
            else:  # adjustment
                obj.stock_after = obj.quantity
            # Mettre a jour le stock du produit
            obj.product.stock = obj.stock_after
            obj.product.save(update_fields=['stock'])
        super().save_model(request, obj, form, change)

"""
ONIZOUKA SHOP - Admin Commandes (Unfold premium)
Gestion: Order, OrderItem, Coupon, Address, Cart
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display
from .models import Order, OrderItem, Coupon, Address, Cart, CartItem


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'product_name', 'product_sku', 'unit_price', 'quantity', 'total_price')
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = (
        'order_number',
        'customer_display',
        'delivery_phone',
        'delivery_city',
        'status_badge',
        'payment_method_display',
        'payment_badge',
        'formatted_total_display',
        'created_at',
    )
    list_filter = ('status', 'payment_method', 'payment_status', 'delivery_city', 'created_at')
    search_fields = (
        'order_number',
        'delivery_name',
        'delivery_phone',
        'user__username',
        'user__email',
        'delivery_address',
    )
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'subtotal', 'total')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Informations Commande', {
            'fields': ('order_number', 'user', 'status')
        }),
        ('Adresse & Contact de Livraison', {
            'fields': ('delivery_name', 'delivery_phone', 'delivery_city', 'delivery_district', 'delivery_address')
        }),
        ('Paiement', {
            'fields': ('payment_method', 'payment_status', 'payment_reference', 'coupon')
        }),
        ('Totaux (FCFA)', {
            'fields': ('subtotal', 'delivery_fee', 'discount', 'total')
        }),
        ('Instructions & Notes', {
            'fields': ('notes', 'admin_notes')
        }),
        ('Horodatage', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',),
        }),
    )

    @display(description='Client')
    def customer_display(self, obj):
        if obj.user:
            return f"{obj.delivery_name} (@{obj.user.username})"
        return f"{obj.delivery_name} (Invité)"

    @display(description='Statut', ordering='status')
    def status_badge(self, obj):
        status_styles = {
            'pending': ('#fef3c7', '#92400e', 'En attente'),
            'confirmed': ('#dbeafe', '#1e40af', 'Confirmée'),
            'processing': ('#e0e7ff', '#3730a3', 'En préparation'),
            'shipped': ('#f3e8ff', '#6b21a8', 'Expédiée'),
            'delivered': ('#dcfce7', '#166534', 'Livrée'),
            'cancelled': ('#fee2e2', '#991b1b', 'Annulée'),
            'refunded': ('#f3f4f6', '#374151', 'Remboursée'),
        }
        bg, color, label = status_styles.get(obj.status, ('#f3f4f6', '#374151', obj.get_status_display()))
        return format_html(
            '<span style="background:{};color:{};padding:3px 10px;border-radius:9999px;font-weight:700;font-size:11px;">{}</span>',
            bg, color, label
        )

    @display(description='Méthode')
    def payment_method_display(self, obj):
        return obj.get_payment_method_display()

    @display(description='Paiement')
    def payment_badge(self, obj):
        if obj.payment_status:
            return format_html(
                '<span style="background:#dcfce7;color:#166534;padding:2px 8px;border-radius:9999px;font-weight:700;font-size:11px;">Payé</span>'
            )
        return format_html(
            '<span style="background:#fee2e2;color:#991b1b;padding:2px 8px;border-radius:9999px;font-weight:700;font-size:11px;">Non payé</span>'
        )

    @display(description='Total', ordering='total')
    def formatted_total_display(self, obj):
        return format_html(
            '<strong style="color:#ca8a04;font-size:13px;">{}</strong>',
            obj.get_formatted_total()
        )


@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = (
        'code',
        'discount_type',
        'discount_value',
        'min_order_amount',
        'current_uses',
        'max_uses',
        'is_active',
        'expires_at',
    )
    list_filter = ('discount_type', 'is_active', 'expires_at')
    search_fields = ('code',)


@admin.register(Address)
class AddressAdmin(ModelAdmin):
    list_display = ('full_name', 'user', 'phone', 'city', 'district', 'is_default')
    list_filter = ('city', 'is_default')
    search_fields = ('full_name', 'phone', 'city', 'district', 'address_line')


class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'get_subtotal')
    readonly_fields = ('get_subtotal',)


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('__str__', 'user', 'session_key', 'items_count_display', 'total_display', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [CartItemInline]

    @display(description='Nb Articles')
    def items_count_display(self, obj):
        return obj.get_items_count()

    @display(description='Total Estimé')
    def total_display(self, obj):
        return obj.get_formatted_total()

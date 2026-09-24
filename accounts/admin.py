"""
ONIZOUKA SHOP - Admin Comptes Utilisateurs (Unfold premium)
"""
from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.decorators import display
from accounts.models import UserProfile, EmailOTP


@admin.register(UserProfile)
class UserProfileAdmin(ModelAdmin):
    list_display = [
        'user', 'show_full_name', 'phone', 'is_email_verified',
        'date_of_birth', 'newsletter', 'show_orders_count',
        'show_total_spent', 'created_at'
    ]
    list_filter = ['is_email_verified', 'newsletter', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'show_total_spent', 'show_orders_count']

    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'is_email_verified')
        }),
        ('Coordonnées & Informations', {
            'fields': ('phone', 'avatar', 'date_of_birth', 'newsletter')
        }),
        ('Statistiques d\'achats', {
            'fields': ('show_orders_count', 'show_total_spent'),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @display(description='Nom complet')
    def show_full_name(self, obj):
        return obj.get_full_name()

    @display(description='Commandes')
    def show_orders_count(self, obj):
        return obj.get_orders_count()

    @display(description='Total dépensé')
    def show_total_spent(self, obj):
        return obj.get_formatted_total_spent()


@admin.register(EmailOTP)
class EmailOTPAdmin(ModelAdmin):
    list_display = ['email', 'code', 'user', 'is_used', 'attempts', 'expires_at', 'created_at']
    list_filter = ['is_used', 'created_at']
    search_fields = ['email', 'code', 'user__username', 'user__email']
    readonly_fields = ['created_at', 'expires_at']


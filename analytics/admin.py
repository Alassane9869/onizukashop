"""
ONIZOUKA SHOP - Admin Analytics (Unfold premium)
"""
from django.contrib import admin
from unfold.admin import ModelAdmin
from analytics.models import ProductView, SearchQuery, DailyStat


@admin.register(ProductView)
class ProductViewAdmin(ModelAdmin):
    list_display = ['product', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['product__name', 'product__sku', 'ip_address', 'user__username']
    readonly_fields = ['product', 'user', 'session_key', 'ip_address', 'user_agent', 'viewed_at']
    ordering = ['-viewed_at']


@admin.register(SearchQuery)
class SearchQueryAdmin(ModelAdmin):
    list_display = ['query', 'results_count', 'user', 'searched_at']
    list_filter = ['searched_at']
    search_fields = ['query', 'user__username']
    readonly_fields = ['query', 'results_count', 'user', 'session_key', 'searched_at']
    ordering = ['-searched_at']


@admin.register(DailyStat)
class DailyStatAdmin(ModelAdmin):
    list_display = ['date', 'visitors', 'page_views', 'orders_count', 'revenue', 'new_users']
    list_filter = ['date']
    readonly_fields = ['date']
    ordering = ['-date']

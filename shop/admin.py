"""
ONIZOUKA SHOP - Admin Shop (Unfold premium)
Gestion: Category, Brand, Product, ProductImage, Review
"""
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Avg
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline, StackedInline
from unfold.decorators import display
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Brand, Product, ProductImage, Review


# ─── CATEGORY ────────────────────────────────────────────────────────────────

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, ModelAdmin):
    list_display = ('tree_actions', 'indented_title', 'is_active', 'show_products_count', 'order')
    list_display_links = ('indented_title',)
    list_filter = ('is_active',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active', 'order')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Informations', {
            'fields': ('name', 'slug', 'parent', 'icon', 'image', 'description', 'order', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @display(description='Produits', ordering='-products_count')
    def show_products_count(self, obj):
        count = obj.get_products_count()
        return format_html(
            '<span style="background:#ca8a04;color:white;padding:2px 8px;border-radius:12px;font-weight:600">{}</span>',
            count
        )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('products'))


# ─── BRAND ───────────────────────────────────────────────────────────────────

@admin.register(Brand)
class BrandAdmin(ModelAdmin):
    list_display = ('show_logo', 'name', 'is_active', 'show_products_count')
    list_editable = ('is_active',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    @display(description='Logo')
    def show_logo(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:40px;width:auto;border-radius:4px;" />', obj.logo.url)
        return '—'

    @display(description='Produits')
    def show_products_count(self, obj):
        count = obj.products.filter(is_active=True).count()
        return format_html(
            '<span style="background:#6366f1;color:white;padding:2px 8px;border-radius:12px;font-weight:600">{}</span>',
            count
        )


# ─── PRODUCT IMAGES INLINE ───────────────────────────────────────────────────

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 3
    fields = ('image', 'show_preview', 'alt_text', 'is_primary', 'order')
    readonly_fields = ('show_preview',)

    @display(description='Apercu')
    def show_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;width:auto;border-radius:4px;" />', obj.image.url)
        return '—'


# ─── REVIEW INLINE ───────────────────────────────────────────────────────────

class ReviewInline(StackedInline):
    model = Review
    extra = 0
    readonly_fields = ('user', 'rating', 'title', 'body', 'is_verified', 'created_at')
    fields = ('user', 'rating', 'title', 'body', 'is_verified', 'is_approved', 'created_at')
    can_delete = True
    show_change_link = False


# ─── PRODUCT ─────────────────────────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = (
        'show_image', 'name', 'sku', 'category', 'brand',
        'show_price', 'show_stock_badge', 'show_status_badge',
        'is_featured', 'is_new', 'show_rating', 'created_at'
    )
    list_display_links = ('show_image', 'name')
    list_filter = ('status', 'is_active', 'is_featured', 'is_new', 'category', 'brand')
    search_fields = ('name', 'sku', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_featured', 'is_new')
    readonly_fields = ('created_at', 'updated_at', 'show_main_image_preview')
    inlines = [ProductImageInline, ReviewInline]
    actions = ['make_active', 'make_inactive', 'make_featured', 'remove_featured']

    fieldsets = (
        ('Informations de base', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand', 'status', 'is_active', 'is_featured', 'is_new')
        }),
        ('Description', {
            'fields': ('short_description', 'description', 'specifications')
        }),
        ('Prix (FCFA)', {
            'fields': ('price', 'sale_price', 'cost_price')
        }),
        ('Stock', {
            'fields': ('stock', 'min_stock', 'track_stock')
        }),
        ('Caracteristiques physiques', {
            'fields': ('weight', 'dimensions'),
            'classes': ('collapse',),
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    @display(description='Image')
    def show_image(self, obj):
        img = obj.primary_image
        if img and img.image:
            return format_html('<img src="{}" style="height:50px;width:50px;object-fit:cover;border-radius:8px;" />', img.image.url)
        return format_html('<div style="height:50px;width:50px;background:#eab308;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#0f172a;font-weight:800;font-size:12px;">ONZ</div>')

    @display(description='Image principale')
    def show_main_image_preview(self, obj):
        img = obj.primary_image
        if img and img.image:
            return format_html('<img src="{}" style="max-height:200px;border-radius:8px;" />', img.image.url)
        return '—'

    @display(description='Prix', ordering='price')
    def show_price(self, obj):
        if obj.is_on_sale:
            return format_html(
                '<div><span style="font-weight:700;color:#ca8a04">{}</span><br>'
                '<span style="text-decoration:line-through;color:#9ca3af;font-size:12px">{}</span>'
                '<span style="background:#ef4444;color:white;padding:1px 5px;border-radius:4px;font-size:11px;margin-left:4px">-{}%</span></div>',
                obj.get_formatted_price(),
                f"{int(obj.price):,} FCFA".replace(",", " "),
                obj.discount_percentage
            )
        return format_html('<span style="font-weight:600">{}</span>', obj.get_formatted_price())

    @display(description='Stock', ordering='stock')
    def show_stock_badge(self, obj):
        if obj.stock == 0:
            color = '#ef4444'
            label = 'Rupture'
        elif obj.is_low_stock:
            color = '#ca8a04'
            label = f'{obj.stock} restants'
        else:
            color = '#10b981'
            label = f'{obj.stock} unités'
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:600">{}</span>',
            color, label
        )

    @display(description='Statut', ordering='status')
    def show_status_badge(self, obj):
        colors = {
            'active': '#10b981',
            'inactive': '#6b7280',
            'out_of_stock': '#ef4444',
            'coming_soon': '#8b5cf6',
        }
        labels = {
            'active': 'Actif',
            'inactive': 'Inactif',
            'out_of_stock': 'Rupture',
            'coming_soon': 'Bientôt',
        }
        color = colors.get(obj.status, '#6b7280')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;font-weight:600">{}</span>',
            color, label
        )

    @display(description='Note')
    def show_rating(self, obj):
        rating = obj.get_average_rating()
        count = obj.get_reviews_count()
        if rating > 0:
            stars = '★' * int(rating) + '☆' * (5 - int(rating))
            return format_html(
                '<span style="color:#ca8a04">{}</span> <small style="color:#6b7280">({} avis)</small>',
                stars, count
            )
        return format_html('<span style="color:#d1d5db">☆☆☆☆☆</span>')

    @admin.action(description='Activer les produits sélectionnés')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True, status='active')
        self.message_user(request, f'{updated} produit(s) activé(s).')

    @admin.action(description='Désactiver les produits sélectionnés')
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False, status='inactive')
        self.message_user(request, f'{updated} produit(s) désactivé(s).')

    @admin.action(description='Mettre en vedette les produits sélectionnés')
    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f'{updated} produit(s) mis en vedette.')

    @admin.action(description='Retirer de la vedette')
    def remove_featured(self, request, queryset):
        updated = queryset.update(is_featured=False)
        self.message_user(request, f'{updated} produit(s) retiré(s) de la vedette.')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category', 'brand').prefetch_related('images')


# ─── REVIEW ──────────────────────────────────────────────────────────────────

@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = ('product', 'user', 'show_rating_stars', 'title', 'is_verified', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'is_verified', 'rating')
    search_fields = ('product__name', 'user__first_name', 'user__last_name', 'title', 'body')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)
    actions = ['approve_reviews', 'reject_reviews']

    @display(description='Note', ordering='rating')
    def show_rating_stars(self, obj):
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        colors = {1: '#ef4444', 2: '#f97316', 3: '#eab308', 4: '#84cc16', 5: '#10b981'}
        return format_html(
            '<span style="color:{};font-size:16px">{}</span>',
            colors.get(obj.rating, '#ca8a04'), stars
        )

    @admin.action(description='Approuver les avis sélectionnés')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} avis approuvé(s).')

    @admin.action(description='Rejeter les avis sélectionnés')
    def reject_reviews(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} avis rejeté(s).')
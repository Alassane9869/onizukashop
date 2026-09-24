"""
ONIZOUKA SHOP - URLs du shop
"""
from django.urls import path
from shop import views

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogue/', views.catalog, name='catalog'),
    path('catalogue/<slug:slug>/', views.category_detail, name='catalog_category'),
    path('recherche/', views.search, name='search'),
    path('categorie/<slug:slug>/', views.category_detail, name='category'),
    path('produit/<slug:slug>/', views.product_detail, name='product'),
    path('produit/<slug:slug>/avis/', views.add_review, name='add_review'),
    path('favoris/', views.wishlist_view, name='wishlist'),
    path('favoris/toggle/<int:product_id>/', views.wishlist_toggle, name='wishlist_toggle'),
    path('contact/', views.contact, name='contact'),
    path('cgv/', views.terms_view, name='terms'),
    path('confidentialite/', views.privacy_view, name='privacy'),
    path('mentions-legales/', views.legal_view, name='legal'),
    path('livraison-garantie/', views.shipping_warranty_view, name='shipping_warranty'),
]

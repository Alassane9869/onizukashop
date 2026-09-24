"""
ONIZOUKA SHOP - URLs Backoffice Direction (/gestion/)
"""
from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    # Tableau de bord principal
    path('', views.dashboard_view, name='dashboard'),
    
    # Gestion des commandes
    path('commandes/', views.orders_view, name='orders'),
    path('commandes/export-csv/', views.export_orders_csv_view, name='export_orders_csv'),
    path('commandes/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('commandes/<int:order_id>/facture/', views.order_invoice_view, name='order_invoice'),
    path('commandes/<int:order_id>/status-htmx/', views.update_order_status_htmx, name='order_status_htmx'),

    # Catalogue & Produits
    path('produits/', views.products_view, name='products'),
    path('produits/export-csv/', views.export_products_csv_view, name='export_products_csv'),
    path('produits/modele-csv/', views.download_product_template_csv_view, name='product_template_csv'),
    path('produits/import-csv/', views.import_products_csv_view, name='import_products_csv'),
    path('produits/nouveau/', views.product_create_view, name='product_create'),
    path('produits/<int:product_id>/modifier/', views.product_edit_view, name='product_edit'),
    path('produits/<int:product_id>/toggle-active/', views.product_toggle_active_htmx, name='product_toggle_active'),

    # Stocks & Réapprovisionnement
    path('stocks/', views.stocks_view, name='stocks'),

    # Clients & Carnet d'adresses
    path('clients/', views.clients_view, name='clients'),
    path('clients/<int:client_id>/', views.client_detail_view, name='client_detail'),

    # Paramètres de l'Entreprise & Boutique
    path('parametres/', views.settings_view, name='settings'),

    # Utilisateurs, Équipe & Rôles
    path('utilisateurs/', views.users_view, name='users'),
    path('utilisateurs/nouveau/', views.user_create_view, name='user_create'),
    path('utilisateurs/<int:user_id>/modifier-role/', views.user_edit_role_view, name='user_edit_role'),
    path('utilisateurs/<int:user_id>/toggle-status/', views.user_toggle_status_view, name='user_toggle_status'),
]

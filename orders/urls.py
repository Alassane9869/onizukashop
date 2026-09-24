"""
ONIZOUKA SHOP - URLs des commandes
"""
from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('ajouter/<int:product_id>/', views.cart_add, name='cart_add'),
    path('supprimer/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('modifier/<int:item_id>/', views.cart_update, name='cart_update'),
    path('coupon/', views.apply_coupon, name='apply_coupon'),
    path('coupon/retirer/', views.remove_coupon, name='remove_coupon'),
    path('commander/', views.checkout, name='checkout'),
    path('valider/', views.place_order, name='place_order'),
    path('confirmation/<str:order_number>/', views.order_confirmation, name='confirmation'),
    path('mes-commandes/', views.order_history, name='history'),
    path('mes-commandes/<str:order_number>/', views.order_detail, name='order_detail'),
    path('mes-commandes/<str:order_number>/facture/', views.order_invoice, name='invoice'),
]

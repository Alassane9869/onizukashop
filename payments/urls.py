"""
ONIZOUKA SHOP - URLs paiements
"""
from django.urls import path
from payments import views

app_name = 'payments'

urlpatterns = [
    path('<str:order_number>/', views.payment_process, name='process'),
    path('<str:order_number>/livraison/', views.payment_cash_on_delivery, name='cash_delivery'),
    path('<str:order_number>/succes/', views.payment_success, name='success'),
    path('<str:order_number>/echec/', views.payment_failure, name='failure'),
]

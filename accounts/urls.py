"""
ONIZOUKA SHOP - URLs du compte
"""
from django.urls import path
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('profil/', views.profile_edit, name='profile_edit'),
    path('adresses/ajouter/', views.address_add, name='address_add'),
    path('adresses/<int:pk>/supprimer/', views.address_delete, name='address_delete'),
    path('adresses/<int:pk>/defaut/', views.address_set_default, name='address_set_default'),
    path('commandes/', views.order_list, name='order_list'),
    path('redirection/', views.login_redirect, name='login_redirect'),
]

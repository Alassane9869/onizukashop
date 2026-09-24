"""
ONIZOUKA SHOP - URLs principales
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gestion/', include('backoffice.urls', namespace='backoffice')),
    path('accounts/', include('allauth.urls')),
    path('compte/', include('accounts.urls', namespace='accounts')),
    path('panier/', include('orders.urls', namespace='orders')),
    path('paiement/', include('payments.urls', namespace='payments')),
    # Redirections transparentes de l'ancien préfixe /boutique/
    path('boutique/', RedirectView.as_view(url='/', permanent=False)),
    path('boutique/<path:subpath>', RedirectView.as_view(url='/%(subpath)s', permanent=False)),
    path('', include('shop.urls', namespace='shop')),
]

from django.urls import re_path
from django.views.static import serve

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
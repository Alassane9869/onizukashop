"""
ONIZOUKA SHOP - URLs principales
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

import os
import mimetypes
from django.http import FileResponse, Http404

def serve_media(request, path):
    file_path = os.path.join(str(settings.MEDIA_ROOT), path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        content_type, _ = mimetypes.guess_type(file_path)
        return FileResponse(open(file_path, 'rb'), content_type=content_type or 'application/octet-stream')
    raise Http404("Media not found")

from django.urls import re_path

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve_media, name='serve_media'),
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

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
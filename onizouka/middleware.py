"""
ONIZOUKA SHOP - Middleware Personnalisé
Normalisation HTTPS et résilience Reverse Proxy cPanel / Passenger / o2switch
"""
import logging

logger = logging.getLogger(__name__)


class PassengerSslMiddleware:
    """
    Middleware garantissant la détection correcte de HTTPS derrière Apache / Passenger sur cPanel (o2switch).
    Sous cPanel / Passenger, Apache gère le certificat SSL et relaie la requête au worker Python via WSGI.
    Apache fournit souvent HTTPS='on' ou REQUEST_SCHEME='https' ou SERVER_PORT='443' ou HTTP_X_FORWARDED_PROTO='https'.
    Si Django ne détecte pas HTTPS, request.is_secure() renvoie False, provoquant le blocage CSRF 403
    'Referer checking failed' lors de la validation des formulaires.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        meta = request.META
        # Indicateurs typiques de terminaison SSL par Apache / cPanel / LiteSpeed / Cloudflare
        is_https = (
            meta.get('HTTPS') in ('on', '1', True)
            or meta.get('REQUEST_SCHEME') == 'https'
            or meta.get('SERVER_PORT') in ('443', 443)
            or meta.get('HTTP_X_FORWARDED_PROTO') == 'https'
            or meta.get('HTTP_X_FORWARDED_SSL') in ('on', '1')
            or meta.get('HTTP_X_FORWARDED_SCHEME') == 'https'
            or meta.get('HTTP_CF_VISITOR') == '{"scheme":"https"}'
            or meta.get('wsgi.url_scheme') == 'https'
        )

        if is_https:
            meta['HTTP_X_FORWARDED_PROTO'] = 'https'
            meta['wsgi.url_scheme'] = 'https'

        return self.get_response(request)

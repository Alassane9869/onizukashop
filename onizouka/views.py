"""
ONIZOUKA SHOP - Vues Globales Système
Gestionnaires d'erreurs HTTP & Récupération CSRF
"""
import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    """
    Vue sur-mesure de secours lors d'un échec de vérification CSRF (403).
    Affiche un message élégant et offre un bouton de rechargement automatique
    au lieu de la page brute d'erreur par défaut de Django.
    """
    logger.warning(
        "CSRF Failure sur Onizouka Shop: %s - URL: %s - Referer: %s - Host: %s - Scheme: %s",
        reason,
        request.path,
        request.META.get('HTTP_REFERER', 'N/A'),
        request.get_host(),
        request.scheme
    )
    return render(
        request, 
        '403_csrf.html', 
        {
            'reason': reason,
            'current_path': request.get_full_path(),
        }, 
        status=403
    )

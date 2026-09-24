"""
ONIZOUKA SHOP - Allauth Account Adapter
Routage intelligent unifié post-connexion selon le statut de l'utilisateur :
- Direction / Staff / Superadmin -> Espace de Gestion ERP (/gestion/)
- Client Acheteur -> Tableau de bord client (/compte/)
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from django.http import HttpRequest


class CustomAccountAdapter(DefaultAccountAdapter):
    """Adaptateur personnalisé pour gérer les redirections intelligentes selon le statut du compte."""

    def get_login_redirect_url(self, request: HttpRequest) -> str:
        """
        Redirection automatique après connexion :
        1. Si un paramètre 'next' explicite est présent (ex: finalisation panier / checkout), on le respecte.
        2. Si l'utilisateur est membre du personnel (is_staff ou superuser), redirection immédiate vers le Backoffice Direction (/gestion/).
        3. Si c'est un client classique, redirection vers son espace client (/compte/).
        """
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and next_url != '/' and not next_url.startswith('/accounts/login'):
            return next_url

        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return resolve_url('backoffice:dashboard')
            return resolve_url('accounts:dashboard')

        return resolve_url('shop:home')

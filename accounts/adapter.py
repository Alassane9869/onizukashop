"""
ONIZOUKA SHOP - Allauth Account Adapter
Routage intelligent unifié post-connexion selon le statut de l'utilisateur :
- Direction / Staff / Superadmin -> Espace de Gestion ERP (/gestion/)
- Client Acheteur -> Tableau de bord client (/compte/)
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url
from django.http import HttpRequest
import logging

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):
    """Adaptateur personnalisé pour gérer les redirections intelligentes et la vérification OTP."""

    def save_user(self, request, user, form, commit=True):
        """Enregistre le nouvel utilisateur et déclenche l'envoi immédiat du code PIN OTP par email."""
        user = super().save_user(request, user, form, commit=commit)

        # Création ou récupération du profil
        from accounts.models import UserProfile, EmailOTP
        from accounts.emails import send_otp_email

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.is_email_verified = False
        profile.save(update_fields=['is_email_verified'])

        # Génération du code OTP et envoi email
        if user.email:
            try:
                otp = EmailOTP.generate_otp(user, user.email)
                send_otp_email(user, user.email, otp.code)
            except Exception as e:
                logger.error(f"Erreur envoi OTP lors du signup: {e}", exc_info=True)

        if hasattr(request, 'session'):
            request.session['pending_verification_user_id'] = user.id

        return user

    def get_login_redirect_url(self, request: HttpRequest) -> str:
        """Redirection intelligente post-connexion."""
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and next_url != '/' and not next_url.startswith('/accounts/login'):
            return next_url

        if request.user.is_authenticated:
            # Vérifier si le compte client est bien vérifié
            if not request.user.is_staff and not request.user.is_superuser:
                profile = getattr(request.user, 'profile', None)
                if profile and not profile.is_email_verified:
                    return resolve_url('accounts:verify_email')

            if request.user.is_staff or request.user.is_superuser:
                return resolve_url('backoffice:dashboard')
            return resolve_url('accounts:dashboard')

        return resolve_url('shop:home')

    def get_signup_redirect_url(self, request: HttpRequest) -> str:
        """Redirige les nouveaux inscrits directement vers la page de saisie du code PIN OTP."""
        return resolve_url('accounts:verify_email')


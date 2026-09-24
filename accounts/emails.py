"""
ONIZOUKA SHOP - Envoi des emails pour les comptes utilisateurs
"""
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def send_otp_email(user, email, code):
    """
    Envoie le code PIN OTP de vérification de compte par email via SMTP.
    """
    subject = f"Votre code de vérification Onizouka Shop : {code}"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <admin@onizouka.danayaplus.com>')
    to = [email]

    user_name = user.get_full_name() or user.username

    context = {
        'user': user,
        'user_name': user_name,
        'code': code,
        'email': email,
    }

    try:
        html_content = render_to_string('emails/otp_verification.html', context)
        text_content = render_to_string('emails/otp_verification.txt', context)
    except Exception as e:
        logger.error(f"Erreur rendu template email OTP: {e}")
        text_content = f"Votre code de vérification Onizouka Shop est : {code} (valable 10 minutes)."
        html_content = f"<p>Votre code de vérification Onizouka Shop est : <strong>{code}</strong> (valable 10 minutes).</p>"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send(fail_silently=False)
        logger.info(f"Email OTP {code} envoyé avec succès à {email}")
        return True
    except Exception as e:
        logger.error(f"Échec envoi email OTP à {email}: {e}", exc_info=True)
        return False

import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger(__name__)


def _get_shop_settings():
    """Récupère les paramètres de la boutique ou un fallback par défaut."""
    try:
        from backoffice.models import ShopSetting
        return ShopSetting.get_settings()
    except Exception:
        return None


def send_order_confirmation_email(order):
    """
    Envoie l'email officiel de confirmation de commande au client.
    """
    recipient_email = None
    if order.user and order.user.email:
        recipient_email = order.user.email

    if not recipient_email:
        logger.warning(f"[EMAIL] Aucun email trouvé pour le client de la commande #{order.order_number}")
        return False

    shop_settings = _get_shop_settings()
    subject = f"Confirmation de votre commande #{order.order_number} - Onizouka Shop"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <commandes@onizoukashop.com>')

    context = {
        'order': order,
        'settings': shop_settings,
    }

    try:
        html_content = render_to_string('emails/order_confirmation.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[recipient_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"[EMAIL] Confirmation envoyée à {recipient_email} pour la commande #{order.order_number}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Erreur lors de l'envoi de confirmation #{order.order_number}: {e}")
        return False


def send_admin_order_alert(order):
    """
    Alerte la direction / équipe commerciale de l'arrivée d'une nouvelle commande.
    """
    shop_settings = _get_shop_settings()
    admin_email = getattr(shop_settings, 'notification_email', None) or 'direction@onizoukashop.com'
    subject = f"[Nouvelle Commande] #{order.order_number} - {int(order.total):,} FCFA".replace(',', ' ')
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <commandes@onizoukashop.com>')

    context = {
        'order': order,
        'settings': shop_settings,
    }

    try:
        html_content = render_to_string('emails/admin_new_order_alert.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[admin_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"[EMAIL] Alerte admin envoyée à {admin_email} pour la commande #{order.order_number}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Erreur alerte admin commande #{order.order_number}: {e}")
        return False


def send_order_status_update_email(order):
    """
    Notifie le client lors d'un changement de statut de sa commande.
    """
    recipient_email = None
    if order.user and order.user.email:
        recipient_email = order.user.email

    if not recipient_email:
        return False

    shop_settings = _get_shop_settings()
    subject = f"Mise à jour Commande #{order.order_number} : {order.get_status_display()} - Onizouka Shop"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <commandes@onizoukashop.com>')

    context = {
        'order': order,
        'settings': shop_settings,
    }

    try:
        html_content = render_to_string('emails/order_status_update.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[recipient_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"[EMAIL] Notification statut envoyée à {recipient_email} pour la commande #{order.order_number}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Erreur notification statut #{order.order_number}: {e}")
        return False


def send_contact_message_email(name, phone, email, subject, message):
    """
    Alerte la direction lors de la soumission d'un message sur la page contact.
    """
    shop_settings = _get_shop_settings()
    admin_email = getattr(shop_settings, 'notification_email', None) or 'direction@onizoukashop.com'
    email_subject = f"[Contact Boutique] Nouveau message de {name} ({phone})"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <commandes@onizoukashop.com>')

    context = {
        'name': name,
        'phone': phone,
        'email': email,
        'subject': subject,
        'message': message,
        'settings': shop_settings,
    }

    try:
        html_content = render_to_string('emails/admin_contact_message.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=from_email,
            to=[admin_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"[EMAIL] Alerte message contact envoyée à {admin_email} pour {name}")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Erreur lors de l'envoi de l'alerte contact: {e}")
        return False


def send_low_stock_alert_email(products):
    """
    Alerte la direction lorsqu'un ou plusieurs produits atteignent un stock bas ou une rupture.
    """
    if not products:
        return False

    shop_settings = _get_shop_settings()
    admin_email = getattr(shop_settings, 'notification_email', None) or 'direction@onizoukashop.com'
    count = len(products)
    email_subject = f"[Alerte Stock] {count} article{'s' if count > 1 else ''} sous le seuil d'alerte en magasin"
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Onizouka Shop <commandes@onizoukashop.com>')

    context = {
        'products': products,
        'settings': shop_settings,
    }

    try:
        html_content = render_to_string('emails/admin_low_stock_alert.html', context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=email_subject,
            body=text_content,
            from_email=from_email,
            to=[admin_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        logger.info(f"[EMAIL] Alerte stock bas envoyée à {admin_email} pour {count} article(s)")
        return True
    except Exception as e:
        logger.error(f"[EMAIL] Erreur lors de l'envoi de l'alerte stock: {e}")
        return False


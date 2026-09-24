"""
ONIZOUKA SHOP - Signaux pour l'application Orders
Fusionne automatiquement le panier anonyme pré-connexion avec le compte utilisateur connecté
"""
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from orders.models import Cart, CartItem


@receiver(user_logged_in)
def merge_cart_on_login(sender, request, user, **kwargs):
    """
    Lors de la connexion d'un client, rapatrie tous les articles
    qu'il avait ajoutés à son panier en tant qu'invité (anonyme).
    """
    if not request or not hasattr(request, 'session'):
        return

    try:
        user_cart, _ = Cart.objects.get_or_create(user=user)

        session_cart_id = request.session.get('cart_id')
        session_carts = []

        if session_cart_id:
            c = Cart.objects.filter(id=session_cart_id).exclude(id=user_cart.id).first()
            if c:
                session_carts.append(c)

        session_key = getattr(request.session, 'session_key', None)
        if session_key:
            for sc in Cart.objects.filter(session_key=session_key).exclude(id=user_cart.id):
                if sc not in session_carts:
                    session_carts.append(sc)

        for sc in session_carts:
            for item in sc.items.select_related('product').all():
                cart_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    product=item.product,
                    defaults={'quantity': item.quantity}
                )
                if not created:
                    cart_item.quantity += item.quantity
                    cart_item.save(update_fields=['quantity'])
            sc.delete()

        request.session['cart_id'] = user_cart.id
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Erreur merge_cart_on_login: {e}", exc_info=True)

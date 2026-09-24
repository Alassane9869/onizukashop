"""
ONIZOUKA SHOP - Context Processors
Injecte dans tous les templates : panier, categories, etc.
"""
from shop.models import Category
from orders.models import Cart


def cart_count(request):
    """Nombre d'articles dans le panier (header)"""
    count = 0
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            session_key = request.session.session_key
            if session_key:
                cart = Cart.objects.filter(session_key=session_key).first()
            else:
                cart = None
        if cart:
            count = cart.get_items_count()
    except Exception:
        count = 0
    return {'cart_count': count}


def categories_menu(request):
    """Categories racines pour le menu de navigation"""
    try:
        root_categories = Category.objects.filter(
            parent__isnull=True,
            is_active=True
        ).prefetch_related('children').order_by('order', 'name')
    except Exception:
        root_categories = []
    return {'menu_categories': root_categories}


def shop_settings(request):
    """Paramètres officiels de l'entreprise (téléphones, WhatsApp, adresses, devises)"""
    try:
        from backoffice.models import ShopSetting
        settings_obj = ShopSetting.get_settings()
    except Exception:
        settings_obj = None
    return {'shop_settings': settings_obj}
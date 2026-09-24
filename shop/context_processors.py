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


from django.core.cache import cache

def categories_menu(request):
    """Categories racines pour le menu de navigation (avec cache mémoire 10 min)"""
    try:
        root_categories = cache.get('menu_categories_cached')
        if root_categories is None:
            root_categories = list(Category.objects.filter(
                parent__isnull=True,
                is_active=True
            ).prefetch_related('children').order_by('order', 'name'))
            cache.set('menu_categories_cached', root_categories, 600)
    except Exception:
        root_categories = []
    return {'menu_categories': root_categories}


def shop_settings(request):
    """Paramètres officiels de l'entreprise (avec cache mémoire 10 min)"""
    try:
        settings_obj = cache.get('shop_settings_cached')
        if settings_obj is None:
            from backoffice.models import ShopSetting
            settings_obj = ShopSetting.get_settings()
            cache.set('shop_settings_cached', settings_obj, 600)
    except Exception:
        settings_obj = None
    return {'shop_settings': settings_obj}
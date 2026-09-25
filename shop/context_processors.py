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
        if hasattr(request, 'user') and request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = None
            if hasattr(request, 'session'):
                session_cart_id = request.session.get('cart_id')
                if session_cart_id:
                    cart = Cart.objects.filter(id=session_cart_id).first()
            if not cart:
                session_key = getattr(request.session, 'session_key', None)
                if session_key:
                    cart = Cart.objects.filter(session_key=session_key).first()
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


def wishlist_data(request):
    """IDs des produits favoris et total pour l'utilisateur connecté"""
    ids = set()
    count = 0
    try:
        if hasattr(request, 'user') and request.user.is_authenticated:
            ids = set(request.user.wishlist_items.values_list('product_id', flat=True))
            count = len(ids)
    except Exception:
        pass
    return {'user_wishlist_ids': ids, 'wishlist_count': count}
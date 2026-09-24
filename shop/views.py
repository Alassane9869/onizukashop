"""
ONIZOUKA SHOP - Views du shop
homepage, catalog, product_detail, search, category
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Avg, Count, Min, Max
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django_htmx.http import trigger_client_event

from shop.models import Product, Category, Brand, Review
from orders.models import Cart, CartItem

import django_filters


# ---------------------------------------------------------------------------
# Filtres
# ---------------------------------------------------------------------------

class ProductFilter(django_filters.FilterSet):
    prix_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='Prix min')
    prix_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='Prix max')
    marque = django_filters.ModelMultipleChoiceFilter(
        field_name='brand',
        queryset=Brand.objects.filter(is_active=True),
        label='Marque',
    )
    en_promo = django_filters.BooleanFilter(
        field_name='sale_price', lookup_expr='isnull', exclude=True, label='En promo'
    )
    en_stock = django_filters.BooleanFilter(method='filter_stock', label='En stock')
    tri = django_filters.OrderingFilter(
        fields=(
            ('price', 'prix_asc'),
            ('-price', 'prix_desc'),
            ('-created_at', 'nouveautes'),
            ('name', 'nom'),
        ),
        field_name='tri',
        label='Trier par',
    )

    class Meta:
        model = Product
        fields = ['prix_min', 'prix_max', 'marque', 'en_promo']

    def filter_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock__gt=0)
        return queryset


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_or_create_cart(request):
    """Recupere ou cree le panier pour l'utilisateur / la session de maniere ultra-robuste et atomique."""
    if hasattr(request, 'user') and request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)

        # Fusionner panier session (via cart_id stocke en session ou session_key)
        session_cart_id = request.session.get('cart_id') if hasattr(request, 'session') else None
        session_carts = []

        if session_cart_id:
            c = Cart.objects.filter(id=session_cart_id).exclude(id=cart.id).first()
            if c and c not in session_carts:
                session_carts.append(c)

        if hasattr(request, 'session') and request.session.session_key:
            for sc in Cart.objects.filter(session_key=request.session.session_key).exclude(id=cart.id):
                if sc not in session_carts:
                    session_carts.append(sc)

        for sc in session_carts:
            for item in sc.items.select_related('product').all():
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=item.product,
                    defaults={'quantity': item.quantity}
                )
                if not created:
                    cart_item.quantity += item.quantity
                    cart_item.save(update_fields=['quantity'])
            sc.delete()

        if hasattr(request, 'session'):
            request.session['cart_id'] = cart.id
        return cart

    # Utilisateur anonyme
    session_key = None
    if hasattr(request, 'session'):
        if not request.session.session_key:
            try:
                request.session.save()
            except Exception:
                pass
        session_key = request.session.session_key

    # Verifier si un cart_id valide existe deja en session
    cart = None
    if hasattr(request, 'session'):
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart = Cart.objects.filter(id=session_cart_id, user__isnull=True).first()

    if not cart and session_key:
        cart = Cart.objects.filter(session_key=session_key).first()

    if not cart:
        if not session_key:
            import uuid
            session_key = uuid.uuid4().hex[:32]
        try:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
        except Exception:
            cart = Cart.objects.filter(session_key=session_key).first()
            if not cart:
                import uuid
                cart = Cart.objects.create(session_key=uuid.uuid4().hex[:32])

    if hasattr(request, 'session'):
        request.session['cart_id'] = cart.id

    return cart




# ---------------------------------------------------------------------------
# Homepage
# ---------------------------------------------------------------------------

def home(request):
    """Page d'accueil : produits vedettes, nouveautes, categories"""
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True, status='active'
    ).select_related('brand', 'category').prefetch_related('images')[:8]

    new_products = Product.objects.filter(
        is_active=True, is_new=True, status='active'
    ).select_related('brand', 'category').prefetch_related('images').order_by('-created_at')[:8]

    sale_products = Product.objects.filter(
        is_active=True, sale_price__isnull=False, status='active'
    ).select_related('brand', 'category').prefetch_related('images')[:8]

    root_categories = Category.objects.filter(
        parent__isnull=True, is_active=True
    ).order_by('order', 'name')[:8]

    brands = list(Brand.objects.filter(is_active=True).order_by('name'))
    brand_specialties = {
        'samsung': ('Compresseur 10 Ans • Froid & TV', 'Leader Froid'),
        'lg': ('Smart Inverter & Écrans OLED 4K', 'N°1 OLED'),
        'midea': ('Climatisation T3 • EDM -60%', 'Spécialiste T3'),
        'hisense': ('Laser TV & Froid No Frost', 'Smart 4K'),
        'beko': ('Made in Europe • Froid Certifié', 'Norme UE'),
        'haier': ('Congélateurs & Froid Pro', 'Froid Expert'),
        'philips': ('Airfryer & Petit Déjeuner', 'Maison & Soin'),
        'moulinex': ('Robots & Préparation Culinaire', 'Cuisine Pro'),
        'sony': ('Cinéma 4K & Son Haute Définition', 'Audio & Vidéo'),
        'tcl': ('Smart TV QLED & Mini-LED', 'Écrans QLED'),
        'binatone': ('Ventilation & Électroménager', 'Robuste & Fiable'),
        'gree': ('Climatiseurs Tropicalisés T3', 'Anti-Canicule'),
        'tefal': ('Cuisson & Poêles Anti-adhésives', 'Culinaire'),
        'sharp': ('Micro-ondes & Purificateurs d\'Air', 'Japon Tech'),
        'westpool': ('Congélateurs Coffres Tropicaux', 'Grand Froid'),
        'ocean': ('Cuisinières & Fours Gaz Inox', 'Cuisson Gaz'),
    }
    for b in brands:
        spec, badge = brand_specialties.get(b.slug, ('Garantie Constructeur 24 Mois', 'Officiel'))
        b.specialty = spec
        b.badge = badge

    climatiseurs = Product.objects.filter(
        category__slug__in=['climatisation', 'climatiseurs'],
        is_active=True, status='active'
    ).select_related('brand', 'category').prefetch_related('images')[:4]
    if not climatiseurs.exists():
        climatiseurs = Product.objects.filter(
            name__icontains='climatiseur', is_active=True, status='active'
        ).select_related('brand', 'category').prefetch_related('images')[:4]

    context = {
        'featured_products': featured_products,
        'new_products': new_products,
        'sale_products': sale_products,
        'climatiseurs': climatiseurs,
        'root_categories': root_categories,
        'brands': brands,
        'page_title': 'Onizouka Shop - Electronique premium au Mali',
        'meta_description': "Achetez vos appareils electroniques au meilleur prix en FCFA. Frigos, climatiseurs, TV et plus de 1000 produits disponibles.",
    }
    return render(request, 'shop/home.html', context)


# ---------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------

def catalog(request):
    """Catalogue general avec filtres et pagination"""
    products_qs = Product.objects.filter(
        is_active=True
    ).select_related('brand', 'category').prefetch_related('images').order_by('-created_at')

    f = ProductFilter(request.GET, queryset=products_qs)
    products_filtered = f.qs

    # Tri manuel
    sort = request.GET.get('tri', 'nouveautes')
    sort_map = {
        'prix_asc': 'price',
        'prix_desc': '-price',
        'nouveautes': '-created_at',
        'nom': 'name',
        'promo': '-sale_price',
    }
    products_filtered = products_filtered.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(products_filtered, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    # Stats pour la sidebar
    price_range = products_qs.aggregate(min_p=Min('price'), max_p=Max('price'))
    brands = Brand.objects.filter(is_active=True, products__is_active=True).distinct()

    selected_brands = request.GET.getlist('marque')

    context = {
        'products': page_obj,
        'filter': f,
        'brands': brands,
        'selected_brands': selected_brands,
        'price_min': price_range['min_p'] or 0,
        'price_max': price_range['max_p'] or 10000000,
        'total_count': products_filtered.count(),
        'sort': sort,
        'page_title': 'Catalogue - Onizouka Shop',
        'meta_description': 'Parcourez notre catalogue de plus de 1000 produits electroniques.',
    }

    if request.htmx:
        return render(request, 'shop/partials/product_grid.html', context)
    return render(request, 'shop/catalog.html', context)


# ---------------------------------------------------------------------------
# Categorie
# ---------------------------------------------------------------------------

def category_detail(request, slug):
    """Produits d'une categorie (et sous-categories)"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    descendants = category.get_descendants(include_self=True)

    products_qs = Product.objects.filter(
        is_active=True, category__in=descendants
    ).select_related('brand', 'category').prefetch_related('images')

    f = ProductFilter(request.GET, queryset=products_qs)
    products_filtered = f.qs

    sort = request.GET.get('tri', 'nouveautes')
    sort_map = {
        'prix_asc': 'price',
        'prix_desc': '-price',
        'nouveautes': '-created_at',
        'nom': 'name',
    }
    products_filtered = products_filtered.order_by(sort_map.get(sort, '-created_at'))

    paginator = Paginator(products_filtered, 24)
    page_obj = paginator.get_page(request.GET.get('page'))

    price_range = products_qs.aggregate(min_p=Min('price'), max_p=Max('price'))
    brands = Brand.objects.filter(
        is_active=True, products__is_active=True, products__category__in=descendants
    ).distinct()

    selected_brands = request.GET.getlist('marque')

    context = {
        'category': category,
        'products': page_obj,
        'filter': f,
        'brands': brands,
        'selected_brands': selected_brands,
        'price_min': price_range['min_p'] or 0,
        'price_max': price_range['max_p'] or 10000000,
        'total_count': products_filtered.count(),
        'sort': sort,
        'breadcrumbs': list(category.get_ancestors(include_self=True)),
        'page_title': f'{category.name} - Onizouka Shop',
        'meta_description': category.meta_description or f'Produits {category.name} au Mali.',
    }

    if request.htmx:
        return render(request, 'shop/partials/product_grid.html', context)
    return render(request, 'shop/catalog.html', context)


# ---------------------------------------------------------------------------
# Fiche produit
# ---------------------------------------------------------------------------

def product_detail(request, slug):
    """Fiche produit complete"""
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category').prefetch_related('images', 'reviews__user'),
        slug=slug, is_active=True
    )

    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')
    avg_rating = product.get_average_rating()

    # Produits similaires
    related_products = Product.objects.filter(
        is_active=True, category=product.category
    ).exclude(pk=product.pk).select_related('brand').prefetch_related('images')[:4]

    # L'utilisateur a-t-il deja un avis ?
    user_review = None
    can_review = False
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()
        # Verifier si l'utilisateur a achete le produit
        from orders.models import OrderItem
        has_bought = OrderItem.objects.filter(
            order__user=request.user,
            product=product,
            order__status='delivered'
        ).exists()
        can_review = has_bought and not user_review

    context = {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_products': related_products,
        'user_review': user_review,
        'can_review': can_review,
        'stars_range': range(1, 6),
        'breadcrumbs': list(product.category.get_ancestors(include_self=True)),
        'page_title': product.meta_title or f'{product.name} - Onizouka Shop',
        'meta_description': product.meta_description or product.short_description,
    }
    return render(request, 'shop/product_detail.html', context)


# ---------------------------------------------------------------------------
# Recherche
# ---------------------------------------------------------------------------

def search(request):
    """Recherche fulltext dans les produits"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    total = 0

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query) |
            Q(brand__name__icontains=query) |
            Q(sku__icontains=query),
            is_active=True
        ).select_related('brand', 'category').prefetch_related('images').distinct()

        total = products.count()

        paginator = Paginator(products, 24)
        products = paginator.get_page(request.GET.get('page'))

    context = {
        'query': query,
        'products': products,
        'total': total,
        'page_title': f'Recherche : {query} - Onizouka Shop' if query else 'Recherche - Onizouka Shop',
    }

    if request.htmx:
        return render(request, 'shop/partials/product_grid.html', context)
    return render(request, 'shop/search.html', context)


# ---------------------------------------------------------------------------
# Avis produit (POST HTMX)
# ---------------------------------------------------------------------------

def add_review(request, slug):
    """Soumettre un avis sur un produit (POST uniquement)"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Connexion requise'}, status=401)
    if request.method != 'POST':
        return redirect('shop:product', slug=slug)

    product = get_object_or_404(Product, slug=slug, is_active=True)

    if Review.objects.filter(product=product, user=request.user).exists():
        messages.error(request, 'Vous avez deja laisse un avis sur ce produit.')
        return redirect('shop:product', slug=slug)

    rating = int(request.POST.get('rating', 0))
    title = request.POST.get('title', '').strip()
    body = request.POST.get('body', '').strip()

    if not (1 <= rating <= 5) or not title or not body:
        messages.error(request, 'Veuillez remplir tous les champs.')
        return redirect('shop:product', slug=slug)

    Review.objects.create(
        product=product,
        user=request.user,
        rating=rating,
        title=title,
        body=body,
    )
    messages.success(request, 'Votre avis a ete soumis. Merci !')
    return redirect('shop:product', slug=slug)


# ---------------------------------------------------------------------------
# Contact & Boutique Bamako
# ---------------------------------------------------------------------------

def contact(request):
    """Page de contact officielle et Boutique Bamako"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if name and phone and message:
            try:
                from orders.emails import send_contact_message_email
                send_contact_message_email(name, phone, email, subject, message)
            except Exception:
                pass

            messages.success(
                request,
                f"Merci {name} ! Votre message a bien été reçu par notre équipe de Bamako. Un conseiller vous contactera rapidement par appel ou WhatsApp."
            )
            return redirect('shop:contact')
        else:
            messages.error(request, "Veuillez renseigner au minimum votre nom, votre numéro de téléphone et votre message.")

    context = {
        'page_title': 'Contact & Boutique Grand Marché - Onizouka Shop',
        'meta_description': 'Contactez notre boutique au Grand Marché de Bamako. Service client WhatsApp 7j/7, devis et assistance après-vente garantie.',
    }
    return render(request, 'shop/contact.html', context)


def terms_view(request):
    """Conditions Générales de Vente (CGV)."""
    return render(request, 'shop/cgv.html', {'page_title': 'Conditions Générales de Vente - Onizouka Shop'})


def privacy_view(request):
    """Politique de Confidentialité et Protection des Données."""
    return render(request, 'shop/privacy.html', {'page_title': 'Politique de Confidentialité - Onizouka Shop'})


def legal_view(request):
    """Mentions Légales de la Société."""
    return render(request, 'shop/legal.html', {'page_title': 'Mentions Légales - Onizouka Shop'})


def shipping_warranty_view(request):
    """Politique de Livraison à Bamako, Retrait Magasin & Garantie Constructeur."""
    return render(request, 'shop/shipping_warranty.html', {'page_title': 'Livraison & Garantie - Onizouka Shop'})


@login_required
@require_POST
def add_review(request, slug):
    """Soumettre un avis client sur un produit"""
    from .models import Review
    product = get_object_or_404(Product, slug=slug, is_active=True)

    try:
        rating = int(request.POST.get('rating', 5))
        if rating < 1 or rating > 5:
            rating = 5
    except (ValueError, TypeError):
        rating = 5

    title = request.POST.get('title', '').strip()
    body = request.POST.get('body', '').strip()

    if not body:
        messages.error(request, 'Veuillez saisir votre commentaire pour publier votre avis.')
        return redirect(f"{product.get_absolute_url()}#avis")

    from orders.models import OrderItem
    has_bought = OrderItem.objects.filter(
        order__user=request.user,
        product=product,
        order__status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).exists()

    review, created = Review.objects.update_or_create(
        product=product,
        user=request.user,
        defaults={
            'rating': rating,
            'title': title or f"Avis de {request.user.first_name or request.user.username}",
            'body': body,
            'is_verified': has_bought,
            'is_approved': True,
        }
    )

    action_word = "enregistré" if created else "mis à jour"
    messages.success(request, f"Votre avis a été {action_word} avec succès. Merci pour votre retour !")
    return redirect(f"{product.get_absolute_url()}#avis")


@login_required
def wishlist_toggle(request, product_id):
    """Ajouter ou retirer un produit des favoris du client"""
    from .models import Wishlist
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    fav = Wishlist.objects.filter(user=request.user, product=product).first()

    if fav:
        fav.delete()
        is_favorited = False
        msg = f"« {product.name} » a été retiré de vos favoris."
    else:
        Wishlist.objects.create(user=request.user, product=product)
        is_favorited = True
        msg = f"« {product.name} » a été ajouté à vos favoris !"

    total_favs = Wishlist.objects.filter(user=request.user).count()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'success': True,
            'is_favorited': is_favorited,
            'count': total_favs,
            'message': msg
        })

    messages.info(request, msg)
    next_url = request.META.get('HTTP_REFERER') or 'shop:wishlist'
    return redirect(next_url)


@login_required
def wishlist_view(request):
    """Afficher la liste des produits favoris du client"""
    from .models import Wishlist
    wishlist_items = (
        Wishlist.objects
        .filter(user=request.user)
        .select_related('product__brand', 'product__category')
        .prefetch_related('product__images')
        .order_by('-created_at')
    )
    products = [item.product for item in wishlist_items if item.product.is_active]

    context = {
        'products': products,
        'total_count': len(products),
        'page_title': 'Mes Favoris - Onizouka Shop',
    }
    return render(request, 'shop/wishlist.html', context)




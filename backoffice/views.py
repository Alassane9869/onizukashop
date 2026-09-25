"""
ONIZOUKA SHOP - Vues du Backoffice Direction & Gestion
Corrections audit : N+1 SQL, erreurs silencieuses, HTML hardcodé, endpoints sécurisés
"""
import csv
import io
from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.conf import settings

from orders.models import Order, OrderItem, Address
from shop.models import Product, Category, Brand, ProductImage
from inventory.models import StockMovement, Supplier
from accounts.models import UserProfile
from orders.emails import send_order_status_update_email
from .forms import ProductForm, StockSupplyForm, OrderUpdateForm


# ---------------------------------------------------------------------------
# Décorateur de sécurité
# ---------------------------------------------------------------------------

def staff_required(view_func):
    """Décorateur : seul le personnel Onizouka Shop (is_staff) peut accéder."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Veuillez vous connecter avec vos identifiants Direction.")
            login_url = getattr(settings, 'LOGIN_URL', '/accounts/login/')
            return redirect(f"{login_url}?next={request.path}")
        if not request.user.is_staff:
            messages.error(request, "Accès refusé : espace réservé exclusivement à la Direction Onizouka Shop.")
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# ---------------------------------------------------------------------------
# Tableau de bord exécutif
# ---------------------------------------------------------------------------

@staff_required
def dashboard_view(request):
    """Tableau de bord exécutif de la Direction Onizouka Shop."""
    now = timezone.now()
    first_day_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    valid_statuses_exclude = [Order.Status.CANCELLED, Order.Status.REFUNDED]

    valid_orders = Order.objects.exclude(status__in=valid_statuses_exclude)
    total_revenue = valid_orders.aggregate(total=Sum('total'))['total'] or 0
    month_revenue = (
        valid_orders
        .filter(created_at__gte=first_day_month)
        .aggregate(total=Sum('total'))['total'] or 0
    )

    total_orders_count = Order.objects.count()
    pending_orders_count = Order.objects.filter(
        status__in=[Order.Status.PENDING, Order.Status.CONFIRMED, Order.Status.PROCESSING]
    ).count()

    # Alertes stock : UNE seule queryset, count() + slice séparés
    low_stock_qs = Product.objects.filter(
        track_stock=True,
        stock__lte=F('min_stock'),
        is_active=True
    ).select_related('category', 'brand').order_by('stock')
    low_stock_count = low_stock_qs.count()
    low_stock_products = low_stock_qs[:6]

    # Clients : exclure aussi les superusers
    total_customers_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    # 8 dernières commandes
    recent_orders = (
        Order.objects
        .select_related('user')
        .prefetch_related('items')
        .order_by('-created_at')[:8]
    )

    # Statistiques paiement : 2 requêtes annotées au lieu de N×2 requêtes en boucle
    count_by_payment = {
        r['payment_method']: r['count']
        for r in Order.objects.values('payment_method').annotate(count=Count('id'))
    }
    volume_by_payment = {
        r['payment_method']: r['volume'] or 0
        for r in (
            Order.objects
            .exclude(status__in=valid_statuses_exclude)
            .values('payment_method')
            .annotate(volume=Sum('total'))
        )
    }
    payment_methods_stats = [
        {
            'code': code,
            'label': label,
            'count': count_by_payment.get(code, 0),
            'volume': volume_by_payment.get(code, 0),
        }
        for code, label in Order.PaymentMethod.choices
    ]

    total_stock_units = (
        Product.objects.filter(track_stock=True).aggregate(units=Sum('stock'))['units'] or 0
    )

    context = {
        'total_revenue': total_revenue,
        'month_revenue': month_revenue,
        'total_orders_count': total_orders_count,
        'pending_orders_count': pending_orders_count,
        'low_stock_count': low_stock_count,
        'low_stock_products': low_stock_products,
        'total_customers_count': total_customers_count,
        'total_stock_units': total_stock_units,
        'recent_orders': recent_orders,
        'payment_methods_stats': payment_methods_stats,
        'current_page': 'dashboard',
    }
    return render(request, 'backoffice/dashboard.html', context)


# ---------------------------------------------------------------------------
# Commandes
# ---------------------------------------------------------------------------

@staff_required
def orders_view(request):
    """Gestion complète des commandes clients avec filtres et recherche."""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('q', '').strip()
    payment_filter = request.GET.get('payment', '')

    orders_qs = (
        Order.objects
        .select_related('user')
        .prefetch_related('items__product')
        .order_by('-created_at')
    )

    if status_filter and status_filter != 'all':
        orders_qs = orders_qs.filter(status=status_filter)
    if payment_filter:
        orders_qs = orders_qs.filter(payment_method=payment_filter)
    if search_query:
        orders_qs = orders_qs.filter(
            Q(order_number__icontains=search_query) |
            Q(delivery_name__icontains=search_query) |
            Q(delivery_phone__icontains=search_query) |
            Q(delivery_district__icontains=search_query) |
            Q(delivery_city__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    # Comptage des statuts : UNE seule requête annotée au lieu de 7 COUNT séparés
    count_by_status = {
        r['status']: r['count']
        for r in Order.objects.values('status').annotate(count=Count('id'))
    }
    status_counts = {
        'all': sum(count_by_status.values()),
        'pending': count_by_status.get(Order.Status.PENDING, 0),
        'confirmed': count_by_status.get(Order.Status.CONFIRMED, 0),
        'processing': count_by_status.get(Order.Status.PROCESSING, 0),
        'shipped': count_by_status.get(Order.Status.SHIPPED, 0),
        'delivered': count_by_status.get(Order.Status.DELIVERED, 0),
        'cancelled': count_by_status.get(Order.Status.CANCELLED, 0),
    }

    paginator = Paginator(orders_qs, 20)
    page_number = request.GET.get('page', 1)
    orders = paginator.get_page(page_number)

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_counts': status_counts,
        'search_query': search_query,
        'payment_filter': payment_filter,
        'payment_choices': Order.PaymentMethod.choices,
        'status_choices': Order.Status.choices,
        'current_page': 'orders',
    }
    return render(request, 'backoffice/orders_list.html', context)


@staff_required
def order_detail_view(request, order_id):
    """Détail complet et modification du statut d'une commande."""
    order = get_object_or_404(
        Order.objects.select_related('user', 'coupon').prefetch_related('items__product__images'),
        id=order_id,
    )

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            prev_status = order.status
            updated_order = form.save(commit=False)
            # Horodatage livraison sans double save()
            if updated_order.status == Order.Status.DELIVERED and prev_status != Order.Status.DELIVERED:
                updated_order.delivered_at = timezone.now()
            updated_order.save()
            
            # Notification par email si le statut a changé
            if prev_status != updated_order.status:
                send_order_status_update_email(updated_order)
                
            messages.success(request, f"La commande #{order.order_number} a été mise à jour avec succès.")
            return redirect('backoffice:order_detail', order_id=order.id)
    else:
        form = OrderUpdateForm(instance=order)

    client_previous_orders = []
    if order.user:
        client_previous_orders = (
            Order.objects
            .filter(user=order.user)
            .exclude(id=order.id)
            .order_by('-created_at')[:5]
        )

    context = {
        'order': order,
        'form': form,
        'client_previous_orders': client_previous_orders,
        'status_choices': Order.Status.choices,
        'current_page': 'orders',
    }
    return render(request, 'backoffice/order_detail.html', context)


@staff_required
def order_invoice_view(request, order_id):
    """Bordereau de livraison / Facture officiel Onizouka Shop imprimable."""
    order = get_object_or_404(
        Order.objects.select_related('user').prefetch_related('items__product'),
        id=order_id,
    )
    return render(request, 'backoffice/order_invoice.html', {'order': order})


@staff_required
@require_POST  # Sécurité : endpoint HTMX accessible en POST uniquement
def update_order_status_htmx(request, order_id):
    """Changement de statut rapide en 1 clic via HTMX."""
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')

    if new_status in dict(Order.Status.choices):
        prev_status = order.status
        order.status = new_status
        if new_status == Order.Status.DELIVERED and not order.delivered_at:
            order.delivered_at = timezone.now()
        order.save(update_fields=['status', 'delivered_at'])
        
        # Envoi de la notification client par email
        if prev_status != new_status:
            send_order_status_update_email(order)

    return render(request, 'backoffice/partials/order_status_badge.html', {'order': order})


# ---------------------------------------------------------------------------
# Catalogue & Produits
# ---------------------------------------------------------------------------

@staff_required
def products_view(request):
    """Catalogue complet des produits avec prix, stocks et statut."""
    category_slug = request.GET.get('category', '')
    brand_id = request.GET.get('brand', '')
    stock_status = request.GET.get('stock', '')
    search_query = request.GET.get('q', '').strip()

    products_qs = (
        Product.objects
        .select_related('category', 'brand')
        .prefetch_related('images')
        .order_by('-created_at')
    )

    if category_slug:
        products_qs = products_qs.filter(category__slug=category_slug)
    if brand_id:
        products_qs = products_qs.filter(brand_id=brand_id)
    if search_query:
        products_qs = products_qs.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(brand__name__icontains=search_query)
        )
    if stock_status == 'low':
        products_qs = products_qs.filter(track_stock=True, stock__lte=F('min_stock'), stock__gt=0)
    elif stock_status == 'out':
        products_qs = products_qs.filter(track_stock=True, stock=0)
    
    featured_filter = request.GET.get('featured', '')
    if featured_filter == '1':
        products_qs = products_qs.filter(is_featured=True)

    categories = Category.objects.filter(is_active=True).order_by('name')
    brands = Brand.objects.filter(is_active=True).order_by('name')

    total_filtered_count = products_qs.count()
    total_products_count = Product.objects.count()

    paginator = Paginator(products_qs, 25)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'selected_category': category_slug,
        'selected_brand': brand_id,
        'selected_stock': stock_status,
        'selected_featured': featured_filter,
        'search_query': search_query,
        'total_filtered_count': total_filtered_count,
        'total_products_count': total_products_count,
        'current_page': 'products',
    }
    return render(request, 'backoffice/products_list.html', context)


@staff_required
def product_create_view(request):
    """Ajout d'un nouveau produit par la Direction."""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            if 'primary_image' in request.FILES:
                ProductImage.objects.create(
                    product=product,
                    image=request.FILES['primary_image'],
                    is_primary=True,
                    alt_text=product.name,
                )
            messages.success(request, f"Produit « {product.name} » ajouté avec succès !")
            return redirect('backoffice:products')
    else:
        form = ProductForm()

    return render(request, 'backoffice/product_form.html', {
        'form': form,
        'title': 'Nouveau Produit Électronique',
        'current_page': 'products',
    })


@staff_required
def product_edit_view(request, product_id):
    """Modification complète d'un produit existant."""
    product = get_object_or_404(Product.objects.prefetch_related('images'), id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            if 'primary_image' in request.FILES:
                primary = product.images.filter(is_primary=True).first()
                if primary:
                    primary.image = request.FILES['primary_image']
                    primary.save()
                else:
                    ProductImage.objects.create(
                        product=product,
                        image=request.FILES['primary_image'],
                        is_primary=True,
                        alt_text=product.name,
                    )
            messages.success(request, f"Produit « {product.name} » mis à jour avec succès.")
            return redirect('backoffice:products')
    else:
        form = ProductForm(instance=product)

    return render(request, 'backoffice/product_form.html', {
        'form': form,
        'product': product,
        'title': f'Modifier {product.name}',
        'current_page': 'products',
    })


@staff_required
@require_POST  # Sécurité + anti-pattern : rendu via template, plus de HTML dans Python
def product_toggle_active_htmx(request, product_id):
    """Activer ou désactiver un produit via HTMX — POST uniquement, rendu par partial."""
    product = get_object_or_404(Product, id=product_id)
    product.is_active = not product.is_active
    product.save(update_fields=['is_active'])
    return render(request, 'backoffice/partials/product_active_toggle.html', {'product': product})


# ---------------------------------------------------------------------------
# Stocks & Réapprovisionnement
# ---------------------------------------------------------------------------

@staff_required
def stocks_view(request):
    """Gestion des stocks, alertes réapprovisionnement et entrées de marchandises."""
    supply_form = StockSupplyForm()
    form_has_errors = False

    if request.method == 'POST':
        supply_form = StockSupplyForm(request.POST)
        if supply_form.is_valid():
            product_id = supply_form.cleaned_data['product_id']
            qty = supply_form.cleaned_data['quantity']
            supplier = supply_form.cleaned_data['supplier']
            reference = supply_form.cleaned_data['reference']
            notes = supply_form.cleaned_data['notes']

            product = get_object_or_404(Product, id=product_id)
            stock_before = product.stock
            product.stock += qty
            if product.stock > 0 and product.status == Product.Status.OUT_OF_STOCK:
                product.status = Product.Status.ACTIVE
            product.save(update_fields=['stock', 'status'])

            StockMovement.objects.create(
                product=product,
                movement_type=StockMovement.MovementType.IN,
                quantity=qty,
                stock_before=stock_before,
                stock_after=product.stock,
                supplier=supplier,
                reference=reference,
                notes=notes,
                created_by=request.user,
            )
            messages.success(
                request,
                f"Stock approvisionné : +{qty} unités pour « {product.name} ». Nouveau stock : {product.stock}.",
            )
            return redirect('backoffice:stocks')
        else:
            # Formulaire invalide : rouvrir le modal avec les erreurs visibles
            form_has_errors = True
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire d'approvisionnement.")

    filter_urgency = request.GET.get('filter', 'all')
    search_q = request.GET.get('q', '').strip()

    products_qs = (
        Product.objects
        .filter(track_stock=True)
        .select_related('category', 'brand')
        .order_by('stock')
    )

    if filter_urgency == 'out':
        products_qs = products_qs.filter(stock=0)
    elif filter_urgency == 'low':
        products_qs = products_qs.filter(stock__lte=F('min_stock'), stock__gt=0)
    elif filter_urgency == 'critical':
        products_qs = products_qs.filter(stock__lte=F('min_stock'))

    if search_q:
        products_qs = products_qs.filter(
            Q(name__icontains=search_q) |
            Q(sku__icontains=search_q) |
            Q(brand__name__icontains=search_q)
        )

    # Chiffres globaux : UNE seule requête annotée au lieu de 3 COUNT séparés
    stock_agg = Product.objects.filter(track_stock=True).aggregate(
        total=Count('id'),
        out=Count('id', filter=Q(stock=0)),
        low=Count('id', filter=Q(stock__lte=F('min_stock'), stock__gt=0)),
    )
    total_tracked_products = stock_agg['total'] or 0
    out_of_stock_count = stock_agg['out'] or 0
    low_stock_count = stock_agg['low'] or 0

    recent_movements = (
        StockMovement.objects
        .select_related('product', 'supplier', 'created_by')
        .order_by('-created_at')[:15]
    )
    suppliers = Supplier.objects.filter(is_active=True).order_by('name')

    paginator = Paginator(products_qs, 20)
    page_number = request.GET.get('page', 1)
    products = paginator.get_page(page_number)

    context = {
        'products': products,
        'filter_urgency': filter_urgency,
        'search_q': search_q,
        'total_tracked_products': total_tracked_products,
        'out_of_stock_count': out_of_stock_count,
        'low_stock_count': low_stock_count,
        'recent_movements': recent_movements,
        'suppliers': suppliers,
        'supply_form': supply_form,
        'form_has_errors': form_has_errors,
        'current_page': 'stocks',
    }
    return render(request, 'backoffice/stocks.html', context)


# ---------------------------------------------------------------------------
# Clients
# ---------------------------------------------------------------------------

@staff_required
def clients_view(request):
    """Annuaire des clients, volumes d'achat et adresses de livraison."""
    search_query = request.GET.get('q', '').strip()

    # Calcul du total AVANT le filtre de recherche, sans prefetch inutile
    clients_base_qs = User.objects.filter(is_staff=False, is_superuser=False)
    total_clients_count = clients_base_qs.count()

    # prefetch 'orders' retiré : bombe mémoire pour 1000+ clients avec beaucoup de commandes
    clients_qs = (
        clients_base_qs
        .select_related('profile')
        .prefetch_related('addresses')
        .order_by('-date_joined')
    )

    if search_query:
        clients_qs = clients_qs.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__phone__icontains=search_query)
        )

    paginator = Paginator(clients_qs, 20)
    page_number = request.GET.get('page', 1)
    clients = paginator.get_page(page_number)

    context = {
        'clients': clients,
        'search_query': search_query,
        'total_clients_count': total_clients_count,
        'current_page': 'clients',
    }
    return render(request, 'backoffice/clients_list.html', context)


@staff_required
def client_detail_view(request, client_id):
    """Fiche détaillée d'un client avec adresses à Bamako et historique d'achats."""
    client = get_object_or_404(
        User.objects.select_related('profile'),
        id=client_id,
        is_staff=False,
        is_superuser=False,
    )
    orders = client.orders.order_by('-created_at')
    addresses = client.addresses.all()

    total_spent = (
        orders
        .exclude(status__in=[Order.Status.CANCELLED, Order.Status.REFUNDED])
        .aggregate(total=Sum('total'))['total'] or 0
    )

    context = {
        'client': client,
        'orders': orders,
        'addresses': addresses,
        'total_spent': total_spent,
        'orders_count': orders.count(),
        'current_page': 'clients',
    }
    return render(request, 'backoffice/client_detail.html', context)


# ---------------------------------------------------------------------------
# Paramètres & Configuration Générale de l'Entreprise
# ---------------------------------------------------------------------------

@staff_required
def settings_view(request):
    """Configuration générale de la boutique, logistique Bamako et identité société."""
    from .models import ShopSetting
    from .forms import ShopSettingForm

    settings_obj = ShopSetting.get_settings()

    if request.method == 'POST':
        form = ShopSettingForm(request.POST, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Les paramètres de la boutique et de l'entreprise ont été enregistrés avec succès.")
            return redirect('backoffice:settings')
        else:
            messages.error(request, "Veuillez vérifier les informations renseignées.")
    else:
        form = ShopSettingForm(instance=settings_obj)

    context = {
        'form': form,
        'settings': settings_obj,
        'current_page': 'settings',
    }
    return render(request, 'backoffice/settings.html', context)


# ---------------------------------------------------------------------------
# Gestion des Utilisateurs & Équipe
# ---------------------------------------------------------------------------

@staff_required
def users_view(request):
    """Gestion des comptes utilisateurs, direction, staff et clients."""
    from .forms import UserCreateForm

    search_query = request.GET.get('q', '').strip()
    role_filter = request.GET.get('role', 'all')

    users_qs = User.objects.select_related('profile').order_by('-date_joined')

    # Si l'utilisateur connecté n'est pas le superuser dev, masquer strictement les superutilisateurs
    if not request.user.is_superuser:
        users_qs = users_qs.filter(is_superuser=False)
        total_count = User.objects.filter(is_superuser=False).count()
        staff_count = User.objects.filter(is_staff=True, is_superuser=False).count()
    else:
        total_count = User.objects.count()
        staff_count = User.objects.filter(is_staff=True).count()

    if role_filter == 'staff':
        users_qs = users_qs.filter(is_staff=True)
    elif role_filter == 'clients':
        users_qs = users_qs.filter(is_staff=False, is_superuser=False)
    elif role_filter == 'superusers':
        if request.user.is_superuser:
            users_qs = users_qs.filter(is_superuser=True)
        else:
            users_qs = users_qs.none()

    if search_query:
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(profile__phone__icontains=search_query)
        )

    clients_count = User.objects.filter(is_staff=False, is_superuser=False).count()

    paginator = Paginator(users_qs, 25)
    page_number = request.GET.get('page', 1)
    users = paginator.get_page(page_number)

    create_form = UserCreateForm()

    context = {
        'users': users,
        'create_form': create_form,
        'search_query': search_query,
        'role_filter': role_filter,
        'total_count': total_count,
        'staff_count': staff_count,
        'clients_count': clients_count,
        'current_page': 'users',
    }
    return render(request, 'backoffice/users_list.html', context)


@staff_required
def user_create_view(request):
    """Création rapide d'un membre d'équipe ou client."""
    from .forms import UserCreateForm
    from accounts.models import Profile

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data.get('first_name', '')
            last_name = form.cleaned_data.get('last_name', '')
            phone = form.cleaned_data.get('phone', '')
            role = form.cleaned_data['role']

            if User.objects.filter(username=username).exists():
                messages.error(request, f"L'identifiant « {username} » est déjà utilisé.")
                return redirect('backoffice:users')

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            if role == 'direction':
                user.is_staff = True
                user.is_superuser = True if request.user.is_superuser else False
            elif role == 'gestionnaire':
                user.is_staff = True
                user.is_superuser = False
            else:
                user.is_staff = False
                user.is_superuser = False
            user.save()

            profile, _ = Profile.objects.get_or_create(user=user)
            if phone:
                profile.phone = phone
                profile.save()

            messages.success(request, f"Le compte de « {user.get_full_name() or user.username} » a été créé avec succès.")
        else:
            messages.error(request, "Erreur dans les champs du formulaire de création.")

    return redirect('backoffice:users')


@staff_required
@require_POST
def user_toggle_status_view(request, user_id):
    """Activer ou désactiver l'accès d'un compte utilisateur."""
    user_target = get_object_or_404(User, id=user_id)

    # Protection stricte : les membres de direction ne peuvent pas toucher au compte superuser dev
    if user_target.is_superuser and not request.user.is_superuser:
        messages.error(request, "Action non autorisée sur ce compte.")
        return redirect('backoffice:users')

    if user_target.id == request.user.id:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte d'administrateur.")
        return redirect('backoffice:users')

    user_target.is_active = not user_target.is_active
    user_target.save(update_fields=['is_active'])
    status_str = "activé" if user_target.is_active else "suspendu"
    messages.success(request, f"Le compte de {user_target.username} a été {status_str}.")
    return redirect('backoffice:users')


@staff_required
@require_POST
def user_edit_role_view(request, user_id):
    """Modifier le rôle et les informations de contact d'un utilisateur par la Direction."""
    from .forms import UserEditRoleForm
    from accounts.models import Profile

    user_target = get_object_or_404(User, id=user_id)

    # Protection superadmin : un staff ordinaire ne peut pas modifier un superadmin
    if user_target.is_superuser and not request.user.is_superuser:
        messages.error(request, "Action non autorisée sur ce compte super-administrateur.")
        return redirect('backoffice:users')

    form = UserEditRoleForm(request.POST, is_superuser=request.user.is_superuser)
    if form.is_valid():
        first_name = form.cleaned_data.get('first_name', '')
        last_name = form.cleaned_data.get('last_name', '')
        email = form.cleaned_data.get('email', '')
        phone = form.cleaned_data.get('phone', '')
        role = form.cleaned_data.get('role')

        # Empêcher l'administrateur connecté de se rétrograder lui-même
        if user_target.id == request.user.id and role == 'client':
            messages.error(request, "Vous ne pouvez pas révoquer vos propres droits d'administrateur.")
            return redirect('backoffice:users')

        user_target.first_name = first_name
        user_target.last_name = last_name
        user_target.email = email

        if role == 'direction' and request.user.is_superuser:
            user_target.is_staff = True
            user_target.is_superuser = True
        elif role == 'gestionnaire':
            user_target.is_staff = True
            user_target.is_superuser = False
        else:  # client
            user_target.is_staff = False
            user_target.is_superuser = False

        user_target.save()

        profile, _ = Profile.objects.get_or_create(user=user_target)
        if phone is not None:
            profile.phone = phone
            profile.save()

        role_display = "Gestionnaire Direction" if user_target.is_staff else "Client Acheteur"
        if user_target.is_superuser:
            role_display = "Super-Administrateur"
        messages.success(request, f"Le compte de {user_target.username} a été mis à jour avec succès (Rôle : {role_display}).")
    else:
        messages.error(request, "Erreur lors de la mise à jour du rôle utilisateur.")

    return redirect('backoffice:users')



@staff_required
def export_orders_csv_view(request):
    """Exporter les commandes en format CSV pour la comptabilité et gestion."""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M")
    filename = f"commandes_onizouka_{timestamp}.csv"

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # BOM pour compatibilité Excel
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'Reference',
        'Date_Commande',
        'Nom_Client',
        'Telephone',
        'Email',
        'Quartier_Ville',
        'Methode_Paiement',
        'Statut_Paiement',
        'Statut_Commande',
        'Sous_Total_FCFA',
        'Livraison_FCFA',
        'Total_FCFA',
        'Nb_Articles',
    ])

    orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')

    for order in orders:
        client_name = order.delivery_name or (order.user.get_full_name() if order.user else 'Client Anonyme')
        phone = order.delivery_phone or ''
        email = order.user.email if order.user else ''
        district = f"{order.delivery_district}, {order.delivery_city}".strip(', ')
        
        writer.writerow([
            order.order_number,
            order.created_at.strftime("%d/%m/%Y %H:%M"),
            client_name,
            phone,
            email,
            district,
            order.get_payment_method_display(),
            "Payé" if order.payment_status else "En attente",
            order.get_status_display(),
            int(order.subtotal or 0),
            int(order.delivery_fee or 0),
            int(order.total or 0),
            order.items.count(),
        ])

    return response


@staff_required
def export_products_csv_view(request):
    """Exporter tout le catalogue de produits en format CSV (compatible Excel Bamako/Mali)."""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M")
    filename = f"catalogue_produits_onizouka_{timestamp}.csv"

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # BOM UTF-8 pour ouverture directe dans Excel sans problème d'accents
    response.write('\ufeff')

    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'SKU',
        'Nom_Produit',
        'Categorie',
        'Marque',
        'Prix_Vente_FCFA',
        'Prix_Promo_FCFA',
        'Prix_Revient_FCFA',
        'Stock',
        'Stock_Minimum',
        'Statut',
        'Visible',
        'En_Vedette',
        'Nouveau',
        'Description_Courte',
    ])

    products = Product.objects.select_related('category', 'brand').order_by('category__name', 'name')

    for p in products:
        writer.writerow([
            p.sku or '',
            p.name,
            p.category.name if p.category else '',
            p.brand.name if p.brand else '',
            int(p.price) if p.price is not None else 0,
            int(p.sale_price) if p.sale_price is not None else '',
            int(p.cost_price) if p.cost_price is not None else '',
            p.stock,
            p.min_stock,
            p.status,
            'OUI' if p.is_active else 'NON',
            'OUI' if p.is_featured else 'NON',
            'OUI' if p.is_new else 'NON',
            (p.short_description or '').replace('\n', ' ').strip(),
        ])

    return response


@staff_required
def download_product_template_csv_view(request):
    """Télécharger le modèle CSV officiel pour l'import en masse de produits."""
    filename = "modele_import_produits_onizouka.csv"
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    response.write('\ufeff')
    writer = csv.writer(response, delimiter=';')
    writer.writerow([
        'SKU',
        'Nom_Produit',
        'Categorie',
        'Marque',
        'Prix_Vente_FCFA',
        'Prix_Promo_FCFA',
        'Prix_Revient_FCFA',
        'Stock',
        'Stock_Minimum',
        'Statut',
        'Visible',
        'En_Vedette',
        'Nouveau',
        'Description_Courte',
    ])

    # Exemples types représentatifs du magasin Onizouka Dabanani
    writer.writerow([
        'ONZ-REF-SAM-385',
        'Réfrigérateur Combiné Samsung 385L NoFrost Digital Inverter',
        'Réfrigérateurs',
        'Samsung',
        '450000',
        '425000',
        '360000',
        '12',
        '3',
        'active',
        'OUI',
        'OUI',
        'NON',
        'Capacité 385L, All-Around Cooling, compresseur Digital Inverter garanti 10 ans.',
    ])
    writer.writerow([
        'ONZ-CLM-HAI-12K',
        'Climatiseur Split Haier 12000 BTU R410A Tropicalisé',
        'Climatiseurs',
        'Haier',
        '245000',
        '',
        '195000',
        '25',
        '5',
        'active',
        'OUI',
        'NON',
        'OUI',
        'Refroidissement ultra-rapide, conçu pour les fortes chaleurs de Bamako.',
    ])

    return response


@staff_required
@require_POST
def import_products_csv_view(request):
    """Importer ou mettre à jour en masse des produits depuis un fichier CSV."""
    if 'csv_file' not in request.FILES:
        messages.error(request, "Veuillez sélectionner un fichier CSV à importer.")
        return redirect('backoffice:products')

    csv_file = request.FILES['csv_file']
    if not csv_file.name.endswith(('.csv', '.txt')):
        messages.error(request, "Format de fichier non valide. Veuillez importer un fichier .csv")
        return redirect('backoffice:products')

    try:
        content = csv_file.read()
        # Décodage intelligent (UTF-8 avec ou sans BOM, ou ISO-8859-1 / cp1252)
        try:
            decoded = content.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                decoded = content.decode('latin-1')
            except UnicodeDecodeError:
                decoded = content.decode('cp1252', errors='replace')

        # Détection du délimiteur (; ou ,)
        lines = decoded.splitlines()
        if not lines:
            messages.warning(request, "Le fichier CSV importé est vide.")
            return redirect('backoffice:products')

        first_line = lines[0]
        delimiter = ';' if ';' in first_line else ','

        reader = csv.DictReader(io.StringIO(decoded), delimiter=delimiter)

        created_count = 0
        updated_count = 0
        skipped_count = 0

        # Normaliser les clés d'en-tête (enlever espaces, minuscules, etc.)
        def clean_key(key):
            if not key:
                return ''
            k = key.strip().lower().replace(' ', '_').replace('é', 'e').replace('è', 'e').replace('ê', 'e')
            return k

        # Pré-chargement des catégories et marques existantes pour optimiser
        categories_cache = {c.name.lower(): c for c in Category.objects.all()}
        brands_cache = {b.name.lower(): b for b in Brand.objects.all()}

        # Catégorie par défaut si non précisée
        default_cat = Category.objects.filter(is_active=True).first()
        if not default_cat:
            default_cat = Category.objects.create(name="Électronique", slug="electronique")
            categories_cache["électronique"] = default_cat

        for row_idx, raw_row in enumerate(reader, start=2):
            row = {clean_key(k): (v.strip() if v else '') for k, v in raw_row.items() if k}

            sku = row.get('sku', '').strip()
            name = row.get('nom_produit', '') or row.get('nom', '') or row.get('name', '')

            if not name:
                skipped_count += 1
                continue

            # Traitement Catégorie
            cat_name = row.get('categorie', '') or row.get('category', '')
            category = None
            if cat_name:
                cat_lower = cat_name.lower()
                if cat_lower in categories_cache:
                    category = categories_cache[cat_lower]
                else:
                    cat_slug = slugify(cat_name)
                    category, _ = Category.objects.get_or_create(
                        slug=cat_slug,
                        defaults={'name': cat_name}
                    )
                    categories_cache[cat_lower] = category
            if not category:
                category = default_cat

            # Traitement Marque
            brand_name = row.get('marque', '') or row.get('brand', '')
            brand = None
            if brand_name:
                brand_lower = brand_name.lower()
                if brand_lower in brands_cache:
                    brand = brands_cache[brand_lower]
                else:
                    brand_slug = slugify(brand_name)
                    brand, _ = Brand.objects.get_or_create(
                        slug=brand_slug,
                        defaults={'name': brand_name}
                    )
                    brands_cache[brand_lower] = brand

            # Nettoyage des prix (enlever espaces, 'FCFA', etc.)
            def parse_int(val, default=0):
                if not val:
                    return default
                cleaned = ''.join(c for c in str(val) if c.isdigit())
                return int(cleaned) if cleaned else default

            price = parse_int(row.get('prix_vente_fcfa', '') or row.get('prix', '') or row.get('price', ''), 0)
            sale_price_raw = row.get('prix_promo_fcfa', '') or row.get('prix_promo', '') or row.get('sale_price', '')
            sale_price = parse_int(sale_price_raw, None) if sale_price_raw else None
            cost_price_raw = row.get('prix_revient_fcfa', '') or row.get('prix_revient', '') or row.get('cost_price', '')
            cost_price = parse_int(cost_price_raw, None) if cost_price_raw else None

            stock = parse_int(row.get('stock', ''), 0)
            min_stock = parse_int(row.get('stock_minimum', '') or row.get('min_stock', ''), 5)

            status = row.get('statut', '') or Product.Status.ACTIVE
            if status not in [choice[0] for choice in Product.Status.choices]:
                status = Product.Status.ACTIVE

            def parse_bool(val, default=True):
                if not val:
                    return default
                v = str(val).strip().upper()
                return v in ['OUI', '1', 'TRUE', 'VRAI', 'YES']

            is_active = parse_bool(row.get('visible', '') or row.get('is_active', ''), True)
            is_featured = parse_bool(row.get('en_vedette', '') or row.get('is_featured', ''), False)
            is_new = parse_bool(row.get('nouveau', '') or row.get('is_new', ''), False)
            short_desc = row.get('description_courte', '') or row.get('short_description', '')

            # Génération auto de SKU si vide
            if not sku:
                cat_prefix = category.slug[:3].upper() if category else 'ONZ'
                sku = f"ONZ-{cat_prefix}-{abs(hash(name)) % 10000:04d}"

            # Recherche si le produit existe déjà par SKU
            product = Product.objects.filter(sku=sku).first()

            if product:
                # Mise à jour
                product.name = name
                product.category = category
                product.brand = brand
                product.price = price
                product.sale_price = sale_price
                product.cost_price = cost_price
                product.stock = stock
                product.min_stock = min_stock
                product.status = status
                product.is_active = is_active
                product.is_featured = is_featured
                product.is_new = is_new
                if short_desc:
                    product.short_description = short_desc
                product.save()
                updated_count += 1
            else:
                # Création
                prod_slug = slugify(name)
                if Product.objects.filter(slug=prod_slug).exists():
                    prod_slug = f"{prod_slug}-{sku.lower()}"

                Product.objects.create(
                    sku=sku,
                    name=name,
                    slug=prod_slug,
                    category=category,
                    brand=brand,
                    price=price,
                    sale_price=sale_price,
                    cost_price=cost_price,
                    stock=stock,
                    min_stock=min_stock,
                    status=status,
                    is_active=is_active,
                    is_featured=is_featured,
                    is_new=is_new,
                    short_description=short_desc,
                    description=short_desc or name,
                )
                created_count += 1

        msg = f"Import terminé avec succès : {created_count} nouveaux produits créés, {updated_count} produits mis à jour."
        if skipped_count:
            msg += f" ({skipped_count} lignes vides ignorées)"
        messages.success(request, msg)

    except Exception as e:
        messages.error(request, f"Erreur lors de l'analyse du fichier CSV : {str(e)}")

    return redirect('backoffice:products')



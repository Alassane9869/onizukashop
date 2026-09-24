"""
ONIZOUKA SHOP - Views Commandes
cart_add, cart_remove, cart_update, cart_detail,
checkout, order_confirm, order_history, apply_coupon
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh

from shop.models import Product
from orders.models import Cart, CartItem, Order, OrderItem, Coupon, Address
from shop.views import get_or_create_cart
from orders.emails import send_order_confirmation_email, send_admin_order_alert


# ---------------------------------------------------------------------------
# Panier
# ---------------------------------------------------------------------------

def cart_detail(request):
    """Afficher le panier avec calcul de remise éventuelle par code promo"""
    try:
        cart = get_or_create_cart(request)
        items = cart.items.select_related('product', 'product__brand').prefetch_related('product__images')

        coupon = None
        coupon_id = request.session.get('coupon_id')
        if coupon_id:
            try:
                coupon = Coupon.objects.get(pk=coupon_id, is_active=True)
                if coupon.expires_at and coupon.expires_at < timezone.now():
                    coupon = None
                    del request.session['coupon_id']
                elif coupon.min_order_amount and cart.get_total() < coupon.min_order_amount:
                    # Trop bas pour ce coupon
                    pass
            except Coupon.DoesNotExist:
                coupon = None
                if 'coupon_id' in request.session:
                    del request.session['coupon_id']

        subtotal = cart.get_total()
        discount = coupon.calculate_discount(subtotal) if coupon else 0
        total = max(0, subtotal - discount)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Erreur cart_detail: {e}", exc_info=True)
        cart = None
        items = []
        coupon = None
        subtotal = 0
        discount = 0
        total = 0

    context = {
        'cart': cart,
        'items': items,
        'coupon': coupon,
        'subtotal': subtotal,
        'discount': discount,
        'total': total,
        'page_title': 'Mon panier - Onizouka Shop',
    }
    return render(request, 'orders/cart.html', context)


@require_POST
def apply_coupon(request):
    """Appliquer un code promo au panier"""
    code = request.POST.get('code', '').strip().upper()
    cart = get_or_create_cart(request)

    if not code:
        messages.error(request, 'Veuillez renseigner un code promo.')
        return redirect('orders:cart')

    try:
        coupon = Coupon.objects.get(code__iexact=code, is_active=True)
    except Coupon.DoesNotExist:
        messages.error(request, f'Le code promo « {code} » est introuvable ou inactif.')
        return redirect('orders:cart')

    now = timezone.now()
    if coupon.expires_at and coupon.expires_at < now:
        messages.error(request, f'Le code promo « {code} » a expiré.')
        return redirect('orders:cart')

    if coupon.max_uses and coupon.current_uses >= coupon.max_uses:
        messages.error(request, f'Le code promo « {code} » a atteint sa limite d\'utilisation.')
        return redirect('orders:cart')

    cart_total = cart.get_total()
    if coupon.min_order_amount and cart_total < coupon.min_order_amount:
        min_fmt = f"{int(coupon.min_order_amount):,} FCFA".replace(',', ' ')
        messages.error(request, f'Ce code nécessite un panier minimum de {min_fmt}.')
        return redirect('orders:cart')

    request.session['coupon_id'] = coupon.id
    val_str = f"-{coupon.discount_value}%" if coupon.discount_type == 'percentage' else f"-{int(coupon.discount_value):,} FCFA".replace(',', ' ')
    messages.success(request, f'Code promo « {coupon.code} » appliqué avec succès ({val_str}) !')
    return redirect('orders:cart')


def remove_coupon(request):
    """Retirer le code promo actif du panier"""
    if 'coupon_id' in request.session:
        del request.session['coupon_id']
        messages.info(request, 'Le code promo a été retiré de votre commande.')
    return redirect('orders:cart')



@csrf_exempt
def cart_add(request, product_id):
    """Ajouter un produit au panier (POST ou GET résilient, exempt CSRF)"""
    try:
        product = get_object_or_404(Product, pk=product_id, is_active=True)
        cart = get_or_create_cart(request)

        qty_raw = request.POST.get('quantity') or request.GET.get('quantity', 1)
        try:
            quantity = int(qty_raw)
        except (ValueError, TypeError):
            quantity = 1
        if quantity < 1:
            quantity = 1

        is_ajax = (
            getattr(request, 'htmx', False) or 
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or 
            'application/json' in request.headers.get('accept', '') or
            request.POST.get('format') == 'json'
        )

        # Verifier le stock
        if product.track_stock and product.stock < quantity:
            if is_ajax:
                return JsonResponse({'success': False, 'error': f'Stock insuffisant ({product.stock} dispo)'}, status=400)
            messages.error(request, f'Stock insuffisant. Seulement {product.stock} disponibles.')
            referer = request.META.get('HTTP_REFERER')
            return redirect(referer if referer else 'shop:product', slug=product.slug)

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            new_qty = cart_item.quantity + quantity
            if product.track_stock and product.stock < new_qty:
                new_qty = product.stock
            cart_item.quantity = new_qty
            cart_item.save(update_fields=['quantity'])
        else:
            cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

        cart_count = cart.get_items_count()

        if is_ajax:
            response = JsonResponse({
                'success': True,
                'cart_count': cart_count,
                'product_name': product.name,
                'message': f'"{product.name}" ajouté au panier !',
            })
            trigger_client_event(response, 'cartUpdated', {
                'count': cart_count,
                'message': f'"{product.name}" ajouté au panier !',
            })
            return response

        messages.success(request, f'"{product.name}" ajouté au panier !')
        next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER')
        if next_url and '/panier/ajouter/' not in next_url:
            return redirect(next_url)
        return redirect('orders:cart')
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Erreur cart_add: {e}", exc_info=True)
        is_ajax = (
            getattr(request, 'htmx', False) or 
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or 
            'application/json' in request.headers.get('accept', '')
        )
        if is_ajax:
            return JsonResponse({'success': False, 'message': "Erreur lors de l'ajout au panier"}, status=400)
        messages.error(request, "Impossible d'ajouter cet article au panier.")
        referer = request.META.get('HTTP_REFERER')
        if referer and '/panier/ajouter/' not in referer:
            return redirect(referer)
        return redirect('orders:cart')


@require_POST
def cart_remove(request, item_id):
    """Supprimer un article du panier"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    product_name = item.product.name
    item.delete()

    if request.htmx:
        cart.refresh_from_db()
        context = {
            'cart': cart,
            'items': cart.items.select_related('product').prefetch_related('product__images'),
        }
        response = render(request, 'orders/partials/cart_items.html', context)
        trigger_client_event(response, 'cartUpdated', {'count': cart.get_items_count()})
        return response

    messages.success(request, f'"{product_name}" retire du panier.')
    return redirect('orders:cart')


@require_POST
def cart_update(request, item_id):
    """Mettre a jour la quantite d'un article"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    quantity = int(request.POST.get('quantity', 1))

    if quantity <= 0:
        item.delete()
    else:
        if item.product.track_stock and item.product.stock < quantity:
            quantity = item.product.stock
        item.quantity = quantity
        item.save()

    if request.htmx:
        cart.refresh_from_db()
        context = {
            'cart': cart,
            'items': cart.items.select_related('product').prefetch_related('product__images'),
        }
        response = render(request, 'orders/partials/cart_items.html', context)
        trigger_client_event(response, 'cartUpdated', {'count': cart.get_items_count()})
        return response

    return redirect('orders:cart')


# ---------------------------------------------------------------------------
# Checkout
# ---------------------------------------------------------------------------

@login_required
def checkout(request):
    """Page de commande / livraison / paiement"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, 'Votre panier est vide.')
        return redirect('orders:cart')

    items = cart.items.select_related('product').prefetch_related('product__images')
    addresses = Address.objects.filter(user=request.user)
    default_address = addresses.filter(is_default=True).first() or addresses.first()

    # Code promo en session
    coupon = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(pk=coupon_id, is_active=True)
        except Coupon.DoesNotExist:
            del request.session['coupon_id']

    subtotal = cart.get_total()
    delivery_fee = 0  # Livraison gratuite pour l'instant
    discount = coupon.calculate_discount(subtotal) if coupon else 0
    total = subtotal + delivery_fee - discount

    context = {
        'cart': cart,
        'items': items,
        'addresses': addresses,
        'default_address': default_address,
        'coupon': coupon,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'discount': discount,
        'total': total,
        'payment_methods': Order.PaymentMethod.choices,
        'page_title': 'Finaliser la commande - Onizouka Shop',
    }
    return render(request, 'orders/checkout.html', context)


@login_required
@require_POST
def place_order(request):
    """Valider et creer la commande"""
    cart = get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, 'Votre panier est vide.')
        return redirect('orders:cart')

    # Recuperer les donnees du formulaire
    full_name = request.POST.get('full_name', '').strip()
    phone = request.POST.get('phone', '').strip()
    city = request.POST.get('city', '').strip()
    district = request.POST.get('district', '').strip()
    address_line = request.POST.get('address_line', '').strip()
    payment_method = request.POST.get('payment_method', Order.PaymentMethod.CASH_ON_DELIVERY)
    notes = request.POST.get('notes', '').strip()
    payment_reference = request.POST.get('payment_reference', '').strip()
    save_address = request.POST.get('save_address') == 'on'

    if not all([full_name, phone, city, address_line]):
        messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
        return redirect('orders:checkout')

    # Code promo
    coupon = None
    coupon_id = request.session.get('coupon_id')
    if coupon_id:
        try:
            coupon = Coupon.objects.get(pk=coupon_id, is_active=True)
        except Coupon.DoesNotExist:
            pass

    items = cart.items.select_related('product').all()
    subtotal = cart.get_total()
    delivery_fee = 0
    discount = coupon.calculate_discount(subtotal) if coupon else 0
    total = subtotal + delivery_fee - discount

    # Creer la commande
    order = Order.objects.create(
        user=request.user,
        delivery_name=full_name,
        delivery_phone=phone,
        delivery_city=city,
        delivery_district=district,
        delivery_address=address_line,
        payment_method=payment_method,
        payment_reference=payment_reference,
        coupon=coupon,
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        discount=discount,
        total=total,
        notes=notes,
    )

    # Creer les lignes de commande et surveiller les stocks bas
    low_stock_products = []
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_sku=item.product.sku,
            quantity=item.quantity,
            unit_price=item.product.current_price,
        )
        # Decrementer le stock
        if item.product.track_stock:
            item.product.stock = max(0, item.product.stock - item.quantity)
            item.product.save(update_fields=['stock', 'status'])
            if item.product.stock <= item.product.min_stock:
                low_stock_products.append(item.product)

    # Alerte email Direction si stock bas atteint
    if low_stock_products:
        try:
            from orders.emails import send_low_stock_alert_email
            send_low_stock_alert_email(low_stock_products)
        except Exception:
            pass

    # Incrementer utilisation coupon
    if coupon:
        coupon.current_uses += 1
        coupon.save(update_fields=['current_uses'])
        del request.session['coupon_id']

    # Sauvegarder l'adresse si demande
    if save_address:
        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            city=city,
            district=district,
            address_line=address_line,
            is_default=not Address.objects.filter(user=request.user).exists()
        )

    # Vider le panier
    cart.items.all().delete()

    # Envoi des emails transactionnels (Client & Direction)
    send_order_confirmation_email(order)
    send_admin_order_alert(order)

    messages.success(request, f'Commande #{order.order_number} confirmee ! Merci pour votre achat.')
    return redirect('orders:confirmation', order_number=order.order_number)


# ---------------------------------------------------------------------------
# Confirmation
# ---------------------------------------------------------------------------

@login_required
def order_confirmation(request, order_number):
    """Page de confirmation de commande avec possibilité d'ajouter la référence de paiement"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if request.method == 'POST':
        ref = request.POST.get('payment_reference', '').strip()
        if ref:
            order.payment_reference = ref
            order.save(update_fields=['payment_reference'])
            messages.success(request, f"Référence de transaction {ref} enregistrée. Notre équipe va vérifier le dépôt.")
            return redirect('orders:confirmation', order_number=order.order_number)

    items = order.items.select_related('product').prefetch_related('product__images')

    context = {
        'order': order,
        'items': items,
        'page_title': f'Commande #{order.order_number} confirmee - Onizouka Shop',
    }
    return render(request, 'orders/confirmation.html', context)


# ---------------------------------------------------------------------------
# Historique des commandes
# ---------------------------------------------------------------------------

@login_required
def order_history(request):
    """Liste des commandes de l'utilisateur"""
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')

    context = {
        'orders': orders,
        'page_title': 'Mes commandes - Onizouka Shop',
    }
    return render(request, 'orders/history.html', context)


@login_required
def order_detail(request, order_number):
    """Detail d'une commande"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    items = order.items.select_related('product').prefetch_related('product__images')

    context = {
        'order': order,
        'items': items,
        'page_title': f'Commande #{order.order_number} - Onizouka Shop',
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_invoice(request, order_number):
    """Facture et bordereau officiel téléchargeable/imprimable pour le client."""
    if request.user.is_staff:
        order = get_object_or_404(
            Order.objects.select_related('user').prefetch_related('items__product'),
            order_number=order_number
        )
    else:
        order = get_object_or_404(
            Order.objects.select_related('user').prefetch_related('items__product'),
            order_number=order_number,
            user=request.user
        )

    return render(request, 'backoffice/order_invoice.html', {
        'order': order,
        'is_client_view': True,
    })


"""
ONIZOUKA SHOP - Views Paiements
Gestion Orange Money, Wave, Paiement a la livraison
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from orders.models import Order
from payments.models import Payment


@login_required
def payment_process(request, order_number):
    """Page de paiement pour une commande"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    if order.payment_status:
        messages.info(request, 'Cette commande est deja payee.')
        return redirect('orders:confirmation', order_number=order.order_number)

    context = {
        'order': order,
        'page_title': f'Paiement commande #{order.order_number} - Onizouka Shop',
    }
    return render(request, 'payments/process.html', context)


@login_required
@require_POST
def payment_cash_on_delivery(request, order_number):
    """Confirmer paiement a la livraison"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    Payment.objects.create(
        order=order,
        method='cash_delivery',
        amount=order.total,
        status=Payment.Status.PENDING,
    )

    order.status = Order.Status.CONFIRMED
    order.payment_method = Order.PaymentMethod.CASH_ON_DELIVERY
    order.save(update_fields=['status', 'payment_method'])

    messages.success(request, f'Commande #{order.order_number} confirmee. Paiement a la livraison.')
    return redirect('orders:confirmation', order_number=order.order_number)


@login_required
def payment_success(request, order_number):
    """Enregistrement de la référence de dépôt transmise par le client (Orange Money / Wave)"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)

    reference = request.POST.get('payment_reference') or request.GET.get('payment_reference') or ''
    method = request.POST.get('payment_method') or request.GET.get('payment_method') or order.payment_method

    if reference:
        order.payment_reference = reference.strip()
    if method:
        order.payment_method = method

    order.save(update_fields=['payment_reference', 'payment_method'])

    # Création du paiement en statut 'pending' pour vérification par la Direction
    Payment.objects.get_or_create(
        order=order,
        defaults={
            'method': order.payment_method,
            'amount': order.total,
            'status': Payment.Status.PENDING,
            'transaction_id': order.payment_reference,
        }
    )

    messages.success(
        request, 
        f"Référence de transaction enregistrée avec succès. Notre équipe vérifie votre dépôt sur le +223 92 67 37 99."
    )
    return redirect('orders:confirmation', order_number=order.order_number)


@login_required
def payment_failure(request, order_number):
    """Callback echec de paiement"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    messages.error(request, 'Le paiement a echoue. Veuillez reessayer.')
    return redirect('payments:process', order_number=order.order_number)

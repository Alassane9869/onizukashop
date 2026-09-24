"""
ONIZOUKA SHOP - Callback de Tableau de bord Exécutif pour Django Unfold
Fournit les KPI en direct, les alertes de stock et les commandes récentes.
"""
from django.db.models import Sum, Count, Q
from django.utils import timezone
from orders.models import Order
from shop.models import Product, Brand, Category
from inventory.models import StockMovement


def dashboard_callback(request, context):
    """
    Injecte toutes les métriques de gestion e-commerce dans le tableau de bord Unfold.
    """
    # 1. Chiffre d'affaires & Commandes
    paid_revenue = Order.objects.filter(payment_status=True).aggregate(s=Sum('total'))['s'] or 0
    pending_orders_count = Order.objects.filter(status='pending').count()
    delivered_orders_count = Order.objects.filter(status='delivered').count()
    total_orders_count = Order.objects.count()

    # 2. Stocks et Catalogue
    low_stock_products = Product.objects.filter(stock__lte=5, is_active=True).order_by('stock')[:6]
    low_stock_count = Product.objects.filter(stock__lte=5, is_active=True).count()
    out_of_stock_count = Product.objects.filter(stock=0, is_active=True).count()
    total_products_count = Product.objects.filter(is_active=True).count()

    # 3. Dernières Commandes
    recent_orders = Order.objects.select_related('user').prefetch_related('items').order_by('-created_at')[:7]

    # 4. Répartition des méthodes de paiement
    payment_methods_raw = Order.objects.values('payment_method').annotate(
        total_amount=Sum('total'),
        count=Count('id')
    ).order_by('-total_amount')

    payment_method_labels = {
        'orange_money': ('Orange Money', '#ea580c', 'phone_android'),
        'wave': ('Wave Mobile', '#0284c7', 'account_balance_wallet'),
        'cash_delivery': ('Paiement à la livraison', '#16a34a', 'payments'),
        'bank_transfer': ('Virement bancaire', '#6b7280', 'account_balance'),
        'moov_money': ('Moov Money', '#2563eb', 'phone_iphone'),
    }

    payment_stats = []
    total_all_orders_amount = Order.objects.aggregate(s=Sum('total'))['s'] or 1
    for pm in payment_methods_raw:
        label, color, icon = payment_method_labels.get(
            pm['payment_method'],
            (pm['payment_method'], '#9ca3af', 'payment')
        )
        pct = round((pm['total_amount'] / total_all_orders_amount) * 100, 1) if total_all_orders_amount else 0
        payment_stats.append({
            'code': pm['payment_method'],
            'label': label,
            'color': color,
            'icon': icon,
            'count': pm['count'],
            'amount': pm['total_amount'],
            'formatted_amount': f"{int(pm['total_amount']):,} FCFA".replace(',', ' '),
            'percentage': pct,
        })

    # 5. Derniers Mouvements de stock
    recent_stock_movements = StockMovement.objects.select_related('product', 'created_by').order_by('-created_at')[:5]

    # Injection dans le contexte Unfold
    context.update({
        'kpi_total_revenue': f"{int(paid_revenue):,} FCFA".replace(',', ' '),
        'kpi_total_revenue_raw': paid_revenue,
        'kpi_pending_orders': pending_orders_count,
        'kpi_delivered_orders': delivered_orders_count,
        'kpi_total_orders': total_orders_count,
        'kpi_low_stock_count': low_stock_count,
        'kpi_out_of_stock_count': out_of_stock_count,
        'kpi_total_products': total_products_count,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'payment_stats': payment_stats,
        'recent_stock_movements': recent_stock_movements,
        'now': timezone.now(),
    })

    return context

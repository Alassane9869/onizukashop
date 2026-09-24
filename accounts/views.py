"""
ONIZOUKA SHOP - Views du compte utilisateur
dashboard, profile_edit, address management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST

from accounts.models import UserProfile
from orders.models import Order, Address


@login_required
def dashboard(request):
    """Tableau de bord du compte client"""
    profile = request.user.profile
    recent_orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items').order_by('-created_at')[:5]

    addresses = Address.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'recent_orders': recent_orders,
        'addresses': addresses,
        'orders_count': request.user.orders.count(),
        'total_spent': profile.get_formatted_total_spent(),
        'page_title': 'Mon compte - Onizouka Shop',
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile_edit(request):
    """Modifier le profil"""
    profile = request.user.profile

    if request.method == 'POST':
        # Infos utilisateur
        request.user.first_name = request.POST.get('first_name', '').strip()
        request.user.last_name = request.POST.get('last_name', '').strip()
        request.user.save(update_fields=['first_name', 'last_name'])

        # Infos profil
        profile.phone = request.POST.get('phone', '').strip()
        profile.newsletter = request.POST.get('newsletter') == 'on'

        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']

        profile.save()
        messages.success(request, 'Profil mis a jour avec succes.')
        return redirect('accounts:dashboard')

    context = {
        'profile': profile,
        'page_title': 'Modifier mon profil - Onizouka Shop',
    }
    return render(request, 'accounts/profile_edit.html', context)


# ---------------------------------------------------------------------------
# Adresses
# ---------------------------------------------------------------------------

@login_required
def address_add(request):
    """Ajouter une adresse"""
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        district = request.POST.get('district', '').strip()
        address_line = request.POST.get('address_line', '').strip()
        is_default = request.POST.get('is_default') == 'on'

        if not all([full_name, phone, city, address_line]):
            messages.error(request, 'Veuillez remplir tous les champs obligatoires.')
            return redirect('accounts:dashboard')

        if is_default:
            Address.objects.filter(user=request.user).update(is_default=False)

        Address.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            city=city,
            district=district,
            address_line=address_line,
            is_default=is_default or not Address.objects.filter(user=request.user).exists(),
        )
        messages.success(request, 'Adresse ajoutee.')
        return redirect('accounts:dashboard')

    context = {'page_title': 'Ajouter une adresse - Onizouka Shop'}
    return render(request, 'accounts/address_form.html', context)


@login_required
def address_delete(request, pk):
    """Supprimer une adresse"""
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Adresse supprimee.')
    return redirect('accounts:dashboard')


@login_required
def address_set_default(request, pk):
    """Definir adresse par defaut"""
    Address.objects.filter(user=request.user).update(is_default=False)
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    messages.success(request, 'Adresse par defaut mise a jour.')
    return redirect('accounts:dashboard')


# ---------------------------------------------------------------------------
# Commandes
# ---------------------------------------------------------------------------

@login_required
def order_list(request):
    """Historique des commandes"""
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items').order_by('-created_at')

    context = {
        'orders': orders,
        'page_title': 'Mes commandes - Onizouka Shop',
    }
    return render(request, 'accounts/order_list.html', context)


@login_required
def login_redirect(request):
    """
    Routage intelligent post-connexion selon le statut du compte :
    - Staff / Direction / Superadmin -> Espace de Gestion Backoffice (/gestion/)
    - Client Acheteur standard -> Espace Client Dashboard (/compte/)
    """
    next_url = request.GET.get('next') or request.POST.get('next')
    if next_url and next_url != '/' and not next_url.startswith('/accounts/login'):
        return redirect(next_url)

    if request.user.is_staff or request.user.is_superuser:
        return redirect('backoffice:dashboard')

    return redirect('accounts:dashboard')


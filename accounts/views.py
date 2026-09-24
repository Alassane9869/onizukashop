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


def mask_email(email):
    """Masque l'adresse email pour la sécurité (ex: al***@gmail.com)"""
    if not email or '@' not in email:
        return email
    parts = email.split('@')
    name = parts[0]
    domain = parts[1]
    if len(name) <= 2:
        masked_name = name[0] + '*'
    else:
        masked_name = name[:2] + '*' * (len(name) - 2)
    return f"{masked_name}@{domain}"


def verify_email(request):
    """
    Page de saisie du code PIN OTP à 6 chiffres pour valider l'adresse email.
    Accessible soit après inscription, soit pour un compte non encore vérifié.
    """
    from django.utils import timezone
    from accounts.models import EmailOTP
    from accounts.emails import send_otp_email

    target_user = None

    # 1. Utilisateur déjà authentifié mais non vérifié
    if request.user.is_authenticated:
        target_user = request.user
        if getattr(target_user, 'profile', None) and target_user.profile.is_email_verified:
            return redirect('accounts:dashboard')
    else:
        # 2. Utilisateur venant de s'inscrire
        pending_id = request.session.get('pending_verification_user_id')
        if pending_id:
            target_user = User.objects.filter(id=pending_id).first()

    if not target_user:
        messages.info(request, "Veuillez vous connecter ou créer un compte.")
        return redirect('account_login')

    if request.method == 'POST':
        action = request.POST.get('action', 'verify')

        # Action: Renvoyer un nouveau code PIN
        if action == 'resend':
            last_otp = EmailOTP.objects.filter(user=target_user).order_by('-created_at').first()
            if last_otp and (timezone.now() - last_otp.created_at).total_seconds() < 60:
                wait_secs = int(60 - (timezone.now() - last_otp.created_at).total_seconds())
                messages.warning(request, f"Veuillez patienter {wait_secs} secondes avant de demander un nouveau code.")
                return redirect('accounts:verify_email')

            new_otp = EmailOTP.generate_otp(target_user, target_user.email)
            send_otp_email(target_user, target_user.email, new_otp.code)
            messages.success(request, f"Un nouveau code de sécurité a été envoyé à {mask_email(target_user.email)}.")
            return redirect('accounts:verify_email')

        # Action: Vérification du code saisi
        code = request.POST.get('code', '').strip().replace(' ', '')
        if not code or len(code) != 6:
            messages.error(request, "Veuillez renseigner un code PIN valide à 6 chiffres.")
            return redirect('accounts:verify_email')

        otp = EmailOTP.objects.filter(user=target_user, is_used=False).order_by('-created_at').first()

        if not otp:
            messages.error(request, "Aucun code en attente. Veuillez cliquer sur 'Renvoyer le code'.")
            return redirect('accounts:verify_email')

        if not otp.is_valid():
            messages.error(request, "Ce code a expiré ou est invalide. Veuillez demander un nouveau code.")
            return redirect('accounts:verify_email')

        if otp.code == code:
            otp.is_used = True
            otp.save(update_fields=['is_used'])

            if hasattr(target_user, 'profile'):
                target_user.profile.is_email_verified = True
                target_user.profile.save(update_fields=['is_email_verified'])

            # Authentifier l'utilisateur s'il n'était pas déjà connecté
            if not request.user.is_authenticated:
                from django.contrib.auth import login as auth_login
                auth_login(request, target_user, backend='django.contrib.auth.backends.ModelBackend')

            if 'pending_verification_user_id' in request.session:
                del request.session['pending_verification_user_id']

            messages.success(request, "Votre adresse email a été confirmée avec succès ! Bienvenue sur Onizouka Shop.")

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and next_url != '/' and not next_url.startswith('/accounts/login'):
                return redirect(next_url)

            return redirect('accounts:dashboard')
        else:
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            remaining = max(0, 5 - otp.attempts)
            messages.error(request, f"Code PIN incorrect ({remaining} tentative(s) restante(s)).")
            return redirect('accounts:verify_email')

    context = {
        'masked_email': mask_email(target_user.email),
        'email': target_user.email,
        'page_title': 'Vérification Email par Code PIN - Onizouka Shop',
    }
    return render(request, 'account/verify_email.html', context)



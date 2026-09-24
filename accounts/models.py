"""
ONIZOUKA SHOP - Modele Profil utilisateur etendu
App: accounts
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Profil etendu lie a l'utilisateur Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telephone')
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='Photo de profil')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Date de naissance')
    newsletter = models.BooleanField(default=False, verbose_name='Abonne newsletter')
    is_email_verified = models.BooleanField(default=False, verbose_name='Email vérifié')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'

    def __str__(self):
        return f'Profil de {self.user.get_full_name() or self.user.username}'

    def get_full_name(self):
        return self.user.get_full_name() or self.user.username

    def get_orders_count(self):
        return self.user.orders.count()

    def get_total_spent(self):
        from django.db.models import Sum
        total = self.user.orders.filter(status='delivered').aggregate(
            total=Sum('total')
        )['total']
        return total or 0

    def get_formatted_total_spent(self):
        return f"{int(self.get_total_spent()):,} FCFA".replace(',', ' ')


class EmailOTP(models.Model):
    """Code PIN OTP à 6 chiffres pour la vérification de l'adresse email des nouveaux comptes"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes')
    email = models.EmailField(verbose_name='Adresse email cible')
    code = models.CharField(max_length=6, verbose_name='Code PIN à 6 chiffres')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name='Date d\'expiration')
    is_used = models.BooleanField(default=False, verbose_name='Déjà utilisé')
    attempts = models.PositiveIntegerField(default=0, verbose_name='Tentatives de saisie')

    class Meta:
        verbose_name = 'Code OTP Email'
        verbose_name_plural = 'Codes OTP Emails'
        ordering = ['-created_at']

    def __str__(self):
        return f"OTP {self.code} pour {self.email} ({'Utilisé' if self.is_used else 'Actif'})"

    @classmethod
    def generate_otp(cls, user, email):
        """Génère un code OTP aléatoire cryptographiquement sécurisé valable 10 minutes"""
        import secrets
        from datetime import timedelta
        from django.utils import timezone

        # Invalider les codes précédents pour cet utilisateur
        cls.objects.filter(user=user, is_used=False).update(is_used=True)

        # Générer 6 chiffres aléatoires sécurisés
        pin = f"{secrets.randbelow(900000) + 100000:06d}"
        expires = timezone.now() + timedelta(minutes=10)

        otp = cls.objects.create(
            user=user,
            email=email,
            code=pin,
            expires_at=expires,
        )
        return otp

    def is_valid(self):
        """Vérifie si le code n'est pas expiré, non utilisé et moins de 5 tentatives erronées"""
        from django.utils import timezone
        return not self.is_used and timezone.now() <= self.expires_at and self.attempts < 5


# Alias pour rétrocompatibilité
Profile = UserProfile




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Creer automatiquement un profil a la creation de l'utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarder le profil a chaque sauvegarde de l'utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        UserProfile.objects.create(user=instance)

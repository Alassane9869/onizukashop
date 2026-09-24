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

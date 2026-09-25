"""
ONIZOUKA SHOP - Formulaires du Backoffice Professionnel
"""
from django import forms
from shop.models import Product, Category, Brand
from orders.models import Order
from inventory.models import StockMovement, Supplier


class ProductForm(forms.ModelForm):
    """Formulaire complet d'ajout / modification de produit"""
    class Meta:
        model = Product
        fields = [
            'name', 'category', 'brand', 'price', 'sale_price', 'cost_price',
            'stock', 'min_stock', 'track_stock', 'status', 'is_active', 'is_featured', 'is_new',
            'short_description', 'description', 'dimensions', 'weight'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'placeholder': 'Ex: Samsung Frigo Side by Side 617L Inverter'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition bg-white'
            }),
            'brand': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition bg-white'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm font-semibold transition',
                'placeholder': 'Ex: 1250000'
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'placeholder': 'Optionnel (laisser vide si pas de promo)'
            }),
            'cost_price': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'placeholder': 'Prix d’achat fournisseur'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm font-bold transition'
            }),
            'min_stock': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition bg-white'
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'rows': 2,
                'placeholder': 'Résumé percutant des atouts du produit'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'rows': 5,
                'placeholder': 'Description détaillée avec fonctionnalités et fiche technique'
            }),
            'dimensions': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'placeholder': 'Ex: 91 x 72 x 178 cm'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'placeholder': 'Ex: 115'
            }),
        }


class StockSupplyForm(forms.Form):
    """Formulaire d'approvisionnement rapide de stock"""
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(
        min_value=1,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm font-bold text-slate-900',
            'placeholder': 'Quantité reçue'
        })
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.filter(is_active=True),
        required=False,
        empty_label="Sélectionner un fournisseur (optionnel)",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm bg-white'
        })
    )
    reference = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm',
            'placeholder': 'Ex: BL-2026-BKO-042'
        })
    )
    notes = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm',
            'placeholder': 'Notes ou motif de l\'ajout'
        })
    )


class OrderUpdateForm(forms.ModelForm):
    """Mise à jour rapide de commande depuis la gestion"""
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'admin_notes']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm font-medium bg-white'
            }),
            'payment_status': forms.CheckboxInput(attrs={
                'class': 'w-5 h-5 text-amber-600 rounded border-slate-300 focus:ring-amber-500'
            }),
            'admin_notes': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2.5 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none text-sm transition',
                'rows': 3,
                'placeholder': 'Notes internes (livreur assigné, confirmation téléphonique, etc.)'
            })
        }


class ShopSettingForm(forms.ModelForm):
    """Formulaire de configuration générale de la boutique et de l'entreprise."""
    from .models import ShopSetting

    class Meta:
        from .models import ShopSetting
        model = ShopSetting
        fields = [
            'site_name', 'company_name', 'nif', 'rccm', 'address',
            'phone_contact', 'phone_whatsapp', 'email_contact', 'email_orders',
            'currency', 'default_delivery_fee', 'free_delivery_threshold', 'delivery_delay_text', 'store_pickup_active',
            'orange_money_number', 'wave_number', 'cash_on_delivery_active',
            'default_min_stock_alert', 'block_order_on_out_of_stock',
            'email_notifications_active', 'whatsapp_notifications_active',
            'flash_sale_active', 'flash_sale_title', 'flash_sale_subtitle', 'flash_sale_end_date'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'company_name': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'nif': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'rccm': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'phone_contact': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono text-slate-800 transition'}),
            'phone_whatsapp': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono text-slate-800 transition'}),
            'email_contact': forms.EmailInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'email_orders': forms.EmailInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'currency': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-bold text-slate-800 transition'}),
            'default_delivery_fee': forms.NumberInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-bold text-slate-800 transition'}),
            'free_delivery_threshold': forms.NumberInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-bold text-slate-800 transition'}),
            'delivery_delay_text': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'orange_money_number': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono text-slate-800 transition'}),
            'wave_number': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono text-slate-800 transition'}),
            'default_min_stock_alert': forms.NumberInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-bold text-slate-800 transition'}),
            'store_pickup_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'cash_on_delivery_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'block_order_on_out_of_stock': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'email_notifications_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'whatsapp_notifications_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'flash_sale_active': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-amber-500 rounded border-slate-300 focus:ring-amber-500'}),
            'flash_sale_title': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'flash_sale_subtitle': forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs text-slate-800 transition'}),
            'flash_sale_end_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono text-slate-800 transition'
                }
            ),
        }


class UserCreateForm(forms.Form):
    """Création d'un nouvel utilisateur ou collaborateur depuis la Direction."""
    ROLE_CHOICES = [
        ('direction', 'Direction Générale (Super-Administrateur IT)'),
        ('gestionnaire', 'Gestionnaire Commercial & Stocks (Staff Direction)'),
        ('client', 'Client Acheteur Standard'),
    ]

    username = forms.CharField(
        label="Identifiant de connexion",
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono'})
    )
    first_name = forms.CharField(
        label="Prénom",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    last_name = forms.CharField(
        label="Nom de famille",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    phone = forms.CharField(
        label="Numéro de Téléphone (Mali)",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono', 'placeholder': '+223 ...'})
    )
    role = forms.ChoiceField(
        label="Rôle et niveau d'accès",
        choices=ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs bg-white'})
    )
    password = forms.CharField(
        label="Mot de passe initial",
        widget=forms.PasswordInput(attrs={'class': 'w-full px-3 py-1.5 rounded-md border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )


class UserEditRoleForm(forms.Form):
    """Modification du rôle et des permissions d'un utilisateur par la Direction."""
    ROLE_CHOICES_STAFF = [
        ('gestionnaire', 'Gestionnaire Direction (Accès Backoffice ERP)'),
        ('client', 'Client Acheteur Standard (Accès Boutique uniquement)'),
    ]
    ROLE_CHOICES_SUPERUSER = [
        ('direction', 'Super-Administrateur Technique (Contrôle Total)'),
        ('gestionnaire', 'Gestionnaire Direction (Accès Backoffice ERP)'),
        ('client', 'Client Acheteur Standard (Accès Boutique uniquement)'),
    ]

    first_name = forms.CharField(
        label="Prénom",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    last_name = forms.CharField(
        label="Nom de famille",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs'})
    )
    phone = forms.CharField(
        label="Téléphone Mali",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs font-mono', 'placeholder': '+223 ...'})
    )
    role = forms.ChoiceField(
        label="Rôle attribué",
        choices=ROLE_CHOICES_STAFF,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-xl border border-slate-200 focus:border-amber-500 focus:ring-1 focus:ring-amber-500 outline-none text-xs bg-white'})
    )

    def __init__(self, *args, is_superuser=False, **kwargs):
        super().__init__(*args, **kwargs)
        if is_superuser:
            self.fields['role'].choices = self.ROLE_CHOICES_SUPERUSER
        else:
            self.fields['role'].choices = self.ROLE_CHOICES_STAFF


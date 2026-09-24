# ONIZOUKA SHOP - Contexte Projet pour Agents IA

## A lire OBLIGATOIREMENT avant de continuer ce projet

---

## Description du projet
Site e-commerce ultra-premium pour electronique (frigos, clims, TV, 1000+ produits).
- Client : vendeur electronique au Mali / Afrique de l'Ouest
- Boutique physique & Siège : Grand Marché de Bamako (Dabanani, Bamako)
- Téléphone & WhatsApp officiel : +223 92 67 37 99 (wa.me/22392673799)
- Monnaie : FCFA (aucune decimale sur les prix)
- Langue : Francais
- Fuseau horaire : Africa/Bamako
- Paiements P1 : Orange Money, Wave, Paiement a la livraison

---

## Stack technique

| Composant | Choix | Version |
|-----------|-------|---------|
| Backend | Django | 5.1.15 |
| Admin | django-unfold | 0.96.0 |
| Auth | django-allauth | 65.19.4 |
| Categories | django-mptt | 0.18.0 |
| Images | django-imagekit + Pillow | 6.1.1 / 12.3.0 |
| HTMX | django-htmx | 1.27.0 |
| Formulaires | crispy-forms + crispy-tailwind | 2.5 / 1.0.3 |
| Fichiers statiques | whitenoise | 6.12.0 |
| Config | python-decouple | 3.8 |
| BDD dev | SQLite | - |
| BDD prod | PostgreSQL | psycopg2-binary 2.9.13 |
| Cache | Redis + django-redis + Celery | 6.0.0 / 5.6.3 |
| Filtres | django-filter | 25.1 |
| CSS | Tailwind CDN (dev) + static/css/main.css | - |
| JS | HTMX + Alpine.js | - |

---

## Commandes utiles (à exécuter dans le terminal utilisateur)

  cd c:/Censure/OnizoukShop
  .\venv\Scripts\python.exe manage.py runserver

### Identifiants des Comptes de Test et d'Administration

1. **Super-Administrateur Technique Développeur (Superuser Django Root / IT - Contrôle Total)** :
   - **Identifiant** : `alasko_ff`
   - **Email** : `alasko6e6ui3e@gmail.com`
   - **Mot de passe** : `www.Diarra9869.com`
   - **Rôle** : Contrôle technique complet du système Django, de la BDD et du code.
   - **Sécurité & Confidentialité** : Strictement masqué et invisible pour les membres de la Direction dans l'ERP (`/gestion/utilisateurs/`). Aucun membre de l'équipe ne peut voir, modifier ou suspendre ce compte.

2. **Administrateur / Gérant de l'Entreprise (Direction Onizouka Shop)** :
   - **Identifiant** : `admin_onizouka`
   - **Email** : `direction@onizoukashop.com`
   - **Mot de passe** : `onizouka123`
   - **Rôle** : Gestionnaire d'entreprise (`is_staff=True`, non-superuser), accès au Tableau de bord exécutif, gestion des commandes, validation des paiements Orange Money / Wave, réapprovisionnement des stocks, catalogue et prix.

3. **Compte Client Acheteur de Test** :
   - **Identifiant** : `client`
   - **Email** : `client@onizoukashop.com`
   - **Mot de passe** : `client123`
   - **Rôle** : Client standard pour tester le parcours d'achat, le panier et le suivi de commande.

- **Portail de Gestion Direction (Sur-mesure)** : http://127.0.0.1:8000/gestion/
- **Boutique Public** : http://127.0.0.1:8000/
- **Django Admin Root (Technique IT)** : http://127.0.0.1:8000/admin/

---

## Design System

- Couleur principale : Jaune Premium #eab308 / #f59e0b (Gold & Amber de luxe)
- Police : Outfit (titres) + Inter (corps) via Google Fonts
- Grille : 8-point grid
- Admin Unfold : palette orange dans settings.py
- Mobile-first : 320px a 1536px
- Skeleton loaders (pas de spinners)
- 4 etats UI : loading / empty / error / success

---

## Etat des fichiers

COMPLETS (100% de la base de code rédigée) :
  - onizouka/settings.py
  - onizouka/urls.py
  - shop/models.py, shop/admin.py, shop/views.py, shop/urls.py, shop/context_processors.py
  - orders/models.py, orders/admin.py, orders/views.py, orders/urls.py
  - accounts/models.py, accounts/admin.py, accounts/views.py, accounts/urls.py
  - payments/models.py, payments/admin.py, payments/views.py, payments/urls.py
  - inventory/models.py, inventory/admin.py
  - analytics/models.py, analytics/admin.py
  - static/css/main.css
  - requirements.txt
  - templates/base.html
  - templates/shop/home.html
  - templates/shop/catalog.html
  - templates/shop/product_detail.html
  - templates/shop/search.html
  - templates/shop/partials/product_card.html
  - templates/shop/partials/product_grid.html
  - templates/orders/cart.html
  - templates/orders/checkout.html
  - templates/orders/confirmation.html
  - templates/orders/history.html
  - templates/orders/order_detail.html
  - templates/orders/partials/cart_items.html
  - templates/payments/process.html
  - templates/accounts/dashboard.html
  - templates/accounts/profile_edit.html
  - templates/accounts/address_form.html
  - templates/accounts/order_list.html
  - templates/backoffice/ (dashboard, orders, products_list with CSV import/export modal, stocks, users, settings, order_invoice)
  - shop/management/commands/backup_system.py (Sauvegarde automatique BDD + Médias en ZIP)
  - scripts/backup_db.py (Script autonome d'archivage)
  - .env.example (Modèle de déploiement sécurisé en production)

---

## Outils d'exploitation & Commandes Pratiques

### 1. Sauvegarde automatique du système (BDD SQLite + Médias)
```bash
.\venv\Scripts\python.exe manage.py backup_system
# ou directement :
.\venv\Scripts\python.exe scripts/backup_db.py
```
*Archive générée dans `backups/backup_onizouka_YYYYMMDD_HHMMSS.zip` (BDD compressée + dossier média complet).*

### 2. Import & Export en Masse du Catalogue
- **Export CSV** : `http://127.0.0.1:8000/gestion/produits/export-csv/` (Téléchargeable en 1 clic au format Excel UTF-8).
- **Modèle CSV** : `http://127.0.0.1:8000/gestion/produits/modele-csv/` (Exemples types avec frigos Samsung, clim Haier).
- **Import CSV** : Directement depuis le bouton **"Importer CSV"** dans `/gestion/produits/` (mise à jour auto par SKU, création auto des marques et catégories).

### 3. Facture / Reçu PDF 1-Clic
- Accessible pour le client sur toutes les commandes validées (`/panier/mes-commandes/<order_number>/facture/`).
- Accessible pour la Direction (`/gestion/commandes/<order_id>/facture/`).
- Mise en page officielle A4, logo Onizouka Shop, mentions légales Grand Marché de Bamako, Dabanani, contact `+223 92 67 37 99`, bouton d'impression / export PDF direct (`window.print()`).

### 4. Commande et Suivi Direct via WhatsApp (+223 92 67 37 99)
- **Depuis le Panier (`/panier/`)** : Bouton *"Commander le Panier sur WhatsApp"* générant automatiquement la liste complète des articles, quantités, prix unitaires et montant total.
- **Depuis la Confirmation de Commande (`/panier/confirmation/<order_number>/`)** : Bannière prioritaire *"Transmettre sur WhatsApp"* avec récapitulatif complet (# de commande, date, articles, total, nom, téléphone, adresse à Bamako).
- **Depuis l'Espace Client (`/compte/commandes/` et `/panier/mes-commandes/<order_number>/`)** : Bouton *"Suivre sur WhatsApp"* pré-rempli pour échanger directement avec l'équipe de la boutique.
- **Format du message** : 100% professionnel, aucun émoji, mise en forme lisible avec sections claires.



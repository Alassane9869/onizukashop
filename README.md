# ONIZOUKA SHOP 🇲🇱
### Plateforme E-Commerce Ultra-Premium pour Électronique & Électroménager
**Grand Marché de Bamako (Dabanani, Bamako - Mali)** · **WhatsApp Officiel : +223 92 67 37 99**

---

## 🌟 Présentation du Projet

**Onizouka Shop** est une solution e-commerce et ERP d'entreprise sur-mesure conçue pour le marché malien et ouest-africain. Elle allie l'esthétique minimaliste et fluide des grandes plateformes internationales (calibre Apple Store) aux spécificités du commerce physique et numérique à Bamako.

- **Monnaie** : FCFA (XOF) sans décimale
- **Fuseau horaire** : Africa/Bamako (GMT+0)
- **Langue** : Français
- **Moyens de paiement** : Orange Money (#144#), Wave (QR/Transfert), Paiement à la livraison
- **Catalogue** : Climatiseurs Tropicalisés Inverter T3, Réfrigérateurs No Frost, Congélateurs Coffres, Smart TV 4K, Cuisinières & Gros Électroménager

---

## ⚡ Stack Technique

| Composant | Technologie / Librairie | Description |
|-----------|-------------------------|-------------|
| **Backend** | Python 3.12+ / Django 5.1 | Architecture robuste MVT |
| **Admin IT** | django-unfold 0.96+ | Interface d'administration moderne et personnalisée |
| **Auth** | django-allauth | Authentification email/identifiant |
| **Catégories** | django-mptt | Arborescence récursive performante |
| **Images** | django-imagekit + Pillow | Génération automatique WebP optimisée |
| **Frontend Dynamique** | HTMX + Alpine.js | Mises à jour instantanées sans rechargement lourd |
| **CSS & Design** | Tailwind CSS CDN + static/css/main.css | Charte dorée/ambre (#eab308 / #f59e0b) |
| **Base de données** | SQLite (Dev) / PostgreSQL (Prod) | Configurable via `.env` |
| **Fichiers statiques** | WhiteNoise | Compression et mise en cache des assets |

---

## 🚀 Fonctionnalités Majeures

### 1. Expérience Client (Boutique Publique)
- **Catalogue & Recherche en direct** : Filtrage par marque (Samsung, LG, Haier, Gree, TCL, etc.), catégories et prix en FCFA.
- **Commande 1-Clic sur WhatsApp (+223 92 67 37 99)** :
  - Depuis le Panier : récapitulatif détaillé des articles, prix et total.
  - Depuis la Confirmation de Commande : transmission immédiate de la commande au magasin.
- **Système de Codes Promo / Coupons** : Application de remises en pourcentage ou en montant fixe FCFA avec contrôle des dates et montants minimum.
- **Avis & Évaluations Clients** : Notation 1 à 5 étoiles, étoiles dorées, badge *"Achat vérifié à Bamako"* et avis modérés.
- **Liste de Favoris (Wishlist)** : Sauvegarde instantanée des coups de cœur via l'icône cœur interactif et page dédiée `/favoris/`.
- **Facture & Reçu PDF Officiel** : Génération et impression directe au format A4 (`window.print()`).

### 2. ERP & Portail Direction (`/gestion/`)
- **Tableau de Bord Exécutif** : CA global en FCFA, commandes en cours, alertes de stock critique.
- **Gestion des Commandes** : Pipeline de statuts interactif en HTMX (En attente, Confirmée, En préparation, Expédiée, Livrée).
- **Import / Export CSV en Masse** : Exportation Excel UTF-8 et import automatique du catalogue avec création auto des marques et catégories.
- **Gestion des Stocks** : Journal des mouvements d'entrées/sorties et fiches fournisseurs.
- **Gestion de l'Équipe & des Rôles** : Attribution des permissions (`Gestionnaire Direction` avec accès ERP vs `Client Acheteur`) et suspension de compte en 1 clic.
- **Sauvegarde Automatique Complète** : Commande `python manage.py backup_system` archivant la BDD et le dossier médias complet en ZIP horodaté.

---

## 🛠️ Installation & Démarrage Local

### 1. Cloner le projet
```bash
git clone https://github.com/Alassane9869/onizukashop.git
cd onizukashop
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
# Sur Windows :
.\venv\Scripts\activate
# Sur Linux / macOS :
source venv/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'environnement
Copiez `.env.example` en `.env` :
```bash
cp .env.example .env
```

### 5. Appliquer les migrations
```bash
python manage.py migrate
```

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```
Rendez-vous sur [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

---

## 🔐 Identifiants de Démonstration

- **Direction Onizouka (ERP /gestion/)** :
  - Identifiant : `admin_onizouka`
  - Mot de passe : `onizouka123`
- **Client de Test (Boutique)** :
  - Identifiant : `client`
  - Mot de passe : `client123`

---

## 📦 Sauvegarde du Système
```bash
python manage.py backup_system
```
Génère une archive dans `backups/backup_onizouka_YYYYMMDD_HHMMSS.zip`.

---

© 2026 Onizouka Shop · Grand Marché de Bamako, Mali. Tous droits réservés.

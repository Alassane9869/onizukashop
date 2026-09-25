"""
ONIZOUKA SHOP - Point d'entrée Phusion Passenger pour hébergement o2switch (cPanel)
"""
import os
import sys

# Répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Charger les variables d'environnement depuis le fichier .env
env_file = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_file):
    try:
        from decouple import RepositoryEnv
        repo = RepositoryEnv(env_file)
        for key, val in repo.data.items():
            os.environ[key] = val
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onizouka.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


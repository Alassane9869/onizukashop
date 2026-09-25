"""
ONIZOUKA SHOP - Point d'entrée Phusion Passenger pour hébergement o2switch (cPanel)
"""
import os
import sys

# 1. Forcer l'interpréteur Python 3.12 du virtualenv CloudLinux / cPanel o2switch
INTERP = "/home/vuxe8870/virtualenv/repositories/onizukashop/3.12/bin/python"
if os.path.exists(INTERP) and sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# 2. Ajout des paquets du virtualenv au PYTHONPATH
VENV_PACKAGES = "/home/vuxe8870/virtualenv/repositories/onizukashop/3.12/lib/python3.12/site-packages"
if os.path.exists(VENV_PACKAGES) and VENV_PACKAGES not in sys.path:
    sys.path.insert(0, VENV_PACKAGES)

# 3. Répertoire racine du projet
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 4. Charger les variables d'environnement depuis le fichier .env
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

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    with open(os.path.join(BASE_DIR, 'passenger_debug.log'), 'a') as f:
        f.write(f"\n--- Erreur démarrage Passenger ---\n{traceback.format_exc()}\n")
    raise

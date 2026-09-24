"""
ONIZOUKA SHOP - Script autonome de Sauvegarde Système
Usage : python scripts/backup_db.py
"""
import os
import sys

# Ajouter le dossier racine au sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onizouka.settings")

if __name__ == "__main__":
    import django
    django.setup()
    from django.core.management import call_command
    call_command("backup_system")

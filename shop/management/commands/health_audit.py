"""
ONIZOUKA SHOP - Commande Management : health_audit
Execution:
  python manage.py health_audit
  python manage.py health_audit --remote https://onizouka.danayaplus.com
"""

from django.core.management.base import BaseCommand
import subprocess
import sys
from pathlib import Path

class Command(BaseCommand):
    help = "Exécute la suite de tests de haut niveau et l'audit de santé du système Onizouka Shop"

    def add_arguments(self, parser):
        parser.add_argument('--remote', type=str, help="URL du serveur de production pour le scan HTTP distant")
        parser.add_argument('--all', action='store_true', help="Exécuter tests internes + scan de production")

    def handle(self, *args, **options):
        script_path = Path(__file__).resolve().parent.parent.parent.parent / 'scripts' / 'system_health_audit.py'
        cmd = [sys.executable, str(script_path)]

        if options.get('remote'):
            cmd.extend(['--remote', options['remote']])
        if options.get('all'):
            cmd.append('--all')

        subprocess.run(cmd)

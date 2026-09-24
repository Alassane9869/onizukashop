"""
ONIZOUKA SHOP - Commande de Sauvegarde Automatisée du Système
App: shop / Command: backup_system
Usage: python manage.py backup_system [--with-media] [--clean-old 30]
"""
import os
import shutil
import sqlite3
import zipfile
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Sauvegarde sécurisée de la base de données et des médias de Onizouka Shop."

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-media',
            action='store_true',
            help='Exclure le dossier media/ de la sauvegarde (base de données uniquement)',
        )
        parser.add_argument(
            '--clean-days',
            type=int,
            default=0,
            help='Supprimer automatiquement les sauvegardes de plus de X jours (0 = désactivé)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Demarrage de la sauvegarde securisee Onizouka Shop..."))

        base_dir = settings.BASE_DIR
        backups_dir = os.path.join(base_dir, 'backups')
        os.makedirs(backups_dir, exist_ok=True)

        now_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"backup_onizouka_{now_str}.zip"
        zip_filepath = os.path.join(backups_dir, zip_filename)

        db_settings = settings.DATABASES['default']
        db_engine = db_settings.get('ENGINE', '')
        temp_files = []

        try:
            with zipfile.ZipFile(zip_filepath, 'w') as zipf:
                # 1. Sauvegarde Base de Données
                if 'sqlite' in db_engine:
                    db_path = db_settings.get('NAME')
                    if db_path and os.path.exists(db_path):
                        temp_db_copy = os.path.join(backups_dir, f"temp_db_{now_str}.sqlite3")
                        temp_files.append(temp_db_copy)

                        # Hot-backup SQLite sécurisé (non bloquant)
                        src_conn = sqlite3.connect(db_path)
                        dst_conn = sqlite3.connect(temp_db_copy)
                        with dst_conn:
                            src_conn.backup(dst_conn)
                        src_conn.close()
                        dst_conn.close()

                        zipf.write(temp_db_copy, arcname="db.sqlite3", compress_type=zipfile.ZIP_DEFLATED)
                        self.stdout.write(self.style.SUCCESS("[OK] Base de donnees SQLite archivee"))
                else:
                    self.stdout.write(self.style.WARNING(f"Base de donnees externe ({db_engine}) : pensez a utiliser pg_dump pour PostgreSQL."))

                # 2. Sauvegarde des Fichiers Médias (images produits, etc.)
                include_media = not options['no_media']
                if include_media and os.path.exists(settings.MEDIA_ROOT):
                    media_count = 0
                    for root, _, files in os.walk(settings.MEDIA_ROOT):
                        for file in files:
                            abs_file = os.path.join(root, file)
                            rel_file = os.path.relpath(abs_file, base_dir)
                            zipf.write(abs_file, arcname=rel_file, compress_type=zipfile.ZIP_STORED)
                            media_count += 1
                    self.stdout.write(self.style.SUCCESS(f"[OK] Dossier media archive ({media_count} fichiers)"))

            # Calcul de la taille
            size_mb = os.path.getsize(zip_filepath) / (1024 * 1024)
            self.stdout.write(
                self.style.SUCCESS(
                    f"\nSUCCES : Sauvegarde terminee avec succes !\n"
                    f"Fichier : {zip_filename}\n"
                    f"Emplacement : {zip_filepath}\n"
                    f"Taille : {size_mb:.2f} Mo\n"
                )
            )

            # Nettoyage automatique des anciennes archives si demandé
            clean_days = options.get('clean_days', 0)
            if clean_days > 0:
                cutoff = datetime.now() - timedelta(days=clean_days)
                for f in os.listdir(backups_dir):
                    if f.startswith("backup_onizouka_") and f.endswith(".zip"):
                        f_path = os.path.join(backups_dir, f)
                        mtime = datetime.fromtimestamp(os.path.getmtime(f_path))
                        if mtime < cutoff:
                            os.remove(f_path)
                            self.stdout.write(self.style.NOTICE(f"Ancienne archive supprimee : {f}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la sauvegarde : {str(e)}"))
            if os.path.exists(zip_filepath):
                os.remove(zip_filepath)
        finally:
            for tf in temp_files:
                if os.path.exists(tf):
                    try:
                        os.remove(tf)
                    except OSError:
                        pass

"""
ONIZOUKA SHOP - Initialisation Django
Support automatique de PyMySQL pour les hébergements type o2switch (cPanel / MariaDB)
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Contournement de la vérification stricte de version PostgreSQL (o2switch PostgreSQL 9.6)
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None
except Exception:
    pass


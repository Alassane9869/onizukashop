"""
ONIZOUKA SHOP - Initialisation Django
Support automatique de PyMySQL pour les hébergements type o2switch (cPanel / MariaDB)
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

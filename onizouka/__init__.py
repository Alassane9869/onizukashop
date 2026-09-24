"""
ONIZOUKA SHOP - Initialisation Django
Support automatique de PyMySQL pour les hébergements type o2switch (cPanel / MariaDB)
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Rétrocompatibilité PostgreSQL 9.6 pour cPanel o2switch (relispartition + version check)
try:
    from django.db.backends.base.base import BaseDatabaseWrapper
    BaseDatabaseWrapper.check_database_version_supported = lambda self: None

    from django.db.backends.postgresql.introspection import DatabaseIntrospection, TableInfo
    def _patched_get_table_list(self, cursor):
        cursor.execute(
            """
            SELECT
                c.relname,
                CASE
                    WHEN c.relkind = 'm' THEN 'm'
                    WHEN c.relkind = 'v' THEN 'v'
                    ELSE 't'
                END
            FROM pg_catalog.pg_class c
            LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
            WHERE c.relkind IN ('r', 'v', 'm')
                AND n.nspname NOT IN ('pg_catalog', 'pg_toast')
                AND pg_catalog.pg_table_is_visible(c.oid)
            """
        )
        return [
            TableInfo(row[0], row[1])
            for row in cursor.fetchall()
            if row[0] not in self.ignored_tables
        ]
    from django.db.backends.postgresql.base import DatabaseWrapper as PGDatabaseWrapper
    PGDatabaseWrapper.data_types['AutoField'] = 'serial'
    PGDatabaseWrapper.data_types['BigAutoField'] = 'bigserial'
    PGDatabaseWrapper.data_types['SmallAutoField'] = 'smallserial'
    PGDatabaseWrapper.data_types_suffix = {}

    DatabaseIntrospection.get_table_list = _patched_get_table_list
except Exception:
    pass


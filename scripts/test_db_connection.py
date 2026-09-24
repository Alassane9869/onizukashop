"""
Script de diagnostic de connexion PostgreSQL sur o2switch / cPanel
"""
import os
import sys
import psycopg2
from decouple import config

def test_connections():
    db_name = config('DB_NAME', default='vuxe8870_onizouka')
    db_user = config('DB_USER', default='vuxe8870_onize')
    db_pass = config('DB_PASSWORD', default='Wj_nhcI8~.Ocl[Vg')
    
    print(f"=== TEST DE CONNEXION POSTGRESQL ===")
    print(f"Base : {db_name}")
    print(f"Utilisateur : {db_user}")
    print("-------------------------------------")
    
    # 1. Test via socket Unix par défaut (pas de host)
    print("1. Test via Socket Unix local (default libpq)...")
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass)
        print(" -> SUCCES ! Connexion par socket Unix établie.")
        conn.close()
        return
    except Exception as e:
        print(f" -> Echec : {e}")

    # 2. Test via socket /tmp
    print("\n2. Test via Socket Unix dans /tmp...")
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host='/tmp')
        print(" -> SUCCES ! Connexion via /tmp établie.")
        conn.close()
        return
    except Exception as e:
        print(f" -> Echec : {e}")

    # 3. Test via socket /var/run/postgresql
    print("\n3. Test via Socket Unix dans /var/run/postgresql...")
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host='/var/run/postgresql')
        print(" -> SUCCES ! Connexion via /var/run/postgresql établie.")
        conn.close()
        return
    except Exception as e:
        print(f" -> Echec : {e}")

    # 4. Test via 127.0.0.1 avec SSL
    print("\n4. Test via 127.0.0.1 avec sslmode=prefer...")
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host='127.0.0.1', port=5432, sslmode='prefer')
        print(" -> SUCCES ! Connexion TCP avec SSL établie.")
        conn.close()
        return
    except Exception as e:
        print(f" -> Echec : {e}")

    print("\n-------------------------------------")
    print("DIAGNOSTIC : Vérifiez dans cPanel > Bases de données PostgreSQL que :")
    print("1. L'utilisateur vuxe8870_onize est bien ajouté à la base vuxe8870_onizouka.")
    print("2. Tous les privilèges lui ont bien été accordés.")

if __name__ == '__main__':
    test_connections()

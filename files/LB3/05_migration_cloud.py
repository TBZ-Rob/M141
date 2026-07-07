"""
LB3: Automatisierte Migration lokal → Cloud (AWS RDS)
Robin Nydegger, PE24c

Dieses Script:
  1. Erstellt einen mysqldump der lokalen DB
  2. Verbindet sich mit der Cloud-DB (AWS RDS)
  3. Überträgt Schema + Daten + Berechtigungen
  4. Validiert die Migration

Voraussetzung:
  - pip install mysql-connector-python
  - mysqldump im PATH (XAMPP: C:\\xampp\\mysql\\bin)
  - AWS RDS Instanz läuft und ist erreichbar

Ausführen: python 05_migration_cloud.py
"""

import subprocess
import sys
import os

try:
    import mysql.connector
except ImportError:
    print("FEHLER: pip install mysql-connector-python")
    sys.exit(1)

# ============================================================
# KONFIGURATION – HIER ANPASSEN!
# ============================================================

# Lokale DB
LOCAL = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',                  # <-- Dein lokales root-PW
    'database': 'backpacker_robin',
}

# Cloud DB (AWS RDS)
CLOUD = {
    'host': 'backpacker-robin.cxyckcs2u3ce.eu-central-1.rds.amazonaws.com',
    'port': 3306,
    'user': 'admin',                                  # <-- RDS Master-User
    'password': 'LB3_Admin_2026!',                                  # <-- RDS Master-PW
    'database': 'backpacker_robin',
}

# Pfad zu mysqldump
MYSQLDUMP = r'C:\xampp\mysql\bin\mysqldump.exe'
MYSQL_CLI = r'C:\xampp\mysql\bin\mysql.exe'

# Dump-Datei
DUMP_FILE = os.path.join(os.path.dirname(__file__), 'backpacker_robin_dump.sql')

# ============================================================
# PHASE 1: Lokalen Dump erstellen
# ============================================================

def create_dump():
    """mysqldump der lokalen DB erstellen."""
    print("\n" + "=" * 60)
    print("PHASE 1: Lokalen Dump erstellen")
    print("=" * 60)

    cmd = [
        MYSQLDUMP,
        f'--host={LOCAL["host"]}',
        f'--port={LOCAL["port"]}',
        f'--user={LOCAL["user"]}',
        f'--password={LOCAL["password"]}',
        '--opt',
        '--routines',
        '--triggers',
        '--single-transaction',
        '--set-charset',
        '--default-character-set=utf8mb4',
        LOCAL['database'],
    ]

    print(f"  Dump: {LOCAL['database']} → {DUMP_FILE}")

    with open(DUMP_FILE, 'w', encoding='utf-8') as f:
        result = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"  [FEHLER] mysqldump: {result.stderr}")
        sys.exit(1)

    size_mb = os.path.getsize(DUMP_FILE) / (1024 * 1024)
    print(f"  [OK] Dump erstellt: {size_mb:.2f} MB")
    return DUMP_FILE


# ============================================================
# PHASE 2: Cloud-DB vorbereiten & Dump einspielen
# ============================================================

def import_to_cloud(dump_file):
    """Dump in die Cloud-DB importieren."""
    print("\n" + "=" * 60)
    print("PHASE 2: Dump in Cloud importieren")
    print("=" * 60)

    # Erst DB erstellen (falls nicht existiert)
    try:
        conn = mysql.connector.connect(
            host=CLOUD['host'],
            port=CLOUD['port'],
            user=CLOUD['user'],
            password=CLOUD['password'],
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{CLOUD['database']}` "
                       f"DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"  [OK] Datenbank '{CLOUD['database']}' auf Cloud erstellt/existiert")
    except mysql.connector.Error as e:
        print(f"  [FEHLER] Cloud-Verbindung: {e}")
        sys.exit(1)

    # Dump einspielen via mysql CLI
    cmd = [
        MYSQL_CLI,
        f'--host={CLOUD["host"]}',
        f'--port={CLOUD["port"]}',
        f'--user={CLOUD["user"]}',
        f'--password={CLOUD["password"]}',
        '--default-character-set=utf8mb4',
        CLOUD['database'],
    ]

    print(f"  Import: {dump_file} → {CLOUD['host']}")

    with open(dump_file, 'r', encoding='utf-8') as f:
        result = subprocess.run(cmd, stdin=f, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        print(f"  [FEHLER] mysql import: {result.stderr}")
        # Nicht abbrechen – Warnungen sind oft OK
        if 'ERROR' in result.stderr.upper():
            sys.exit(1)

    print(f"  [OK] Dump erfolgreich importiert")


# ============================================================
# PHASE 3: Berechtigungen auf Cloud übertragen
# ============================================================

def setup_cloud_dcl():
    """Rollen und Benutzer auf der Cloud-DB erstellen."""
    print("\n" + "=" * 60)
    print("PHASE 3: Berechtigungen auf Cloud einrichten")
    print("=" * 60)

    conn = mysql.connector.connect(
        host=CLOUD['host'],
        port=CLOUD['port'],
        user=CLOUD['user'],
        password=CLOUD['password'],
        database=CLOUD['database'],
    )
    cursor = conn.cursor()

    # DCL-Script einlesen und ausführen
    dcl_file = os.path.join(os.path.dirname(__file__), '03_dcl_rollen_benutzer.sql')

    if os.path.exists(dcl_file):
        print(f"  DCL-Script: {dcl_file}")
        with open(dcl_file, 'r', encoding='utf-8') as f:
            sql = f.read()

        # USE-Statement anpassen
        sql = sql.replace('USE backpacker_robin;', f'USE `{CLOUD["database"]}`;')

        # Statements einzeln ausführen
        statements = [s.strip() for s in sql.split(';') if s.strip()
                       and not s.strip().startswith('--')
                       and not s.strip().startswith('SELECT')]

        success = 0
        errors = 0
        for stmt in statements:
            try:
                cursor.execute(stmt)
                success += 1
            except mysql.connector.Error as e:
                # Einige Fehler sind OK (z.B. DROP IF NOT EXISTS)
                if 'already exists' not in str(e).lower():
                    print(f"  [WARNUNG] {e}")
                errors += 1

        conn.commit()
        print(f"  [OK] {success} Statements ausgeführt, {errors} Warnungen")
    else:
        print(f"  [WARNUNG] DCL-Script nicht gefunden: {dcl_file}")
        print(f"  Bitte manuell ausführen!")

    cursor.close()
    conn.close()


# ============================================================
# PHASE 4: Migration validieren
# ============================================================

def validate_migration():
    """Vergleich: Lokale DB vs Cloud DB."""
    print("\n" + "=" * 60)
    print("PHASE 4: Migration validieren")
    print("=" * 60)

    tables = ['tbl_land', 'tbl_leistung', 'tbl_personen',
              'tbl_benutzer', 'tbl_buchung', 'tbl_positionen']

    # Lokale Counts
    local_conn = mysql.connector.connect(**LOCAL)
    local_cursor = local_conn.cursor()

    # Cloud Counts
    cloud_conn = mysql.connector.connect(
        host=CLOUD['host'], port=CLOUD['port'],
        user=CLOUD['user'], password=CLOUD['password'],
        database=CLOUD['database'],
    )
    cloud_cursor = cloud_conn.cursor()

    print(f"\n  {'Tabelle':25s} {'Lokal':>8s} {'Cloud':>8s} {'Status':>8s}")
    print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")

    all_ok = True
    for t in tables:
        local_cursor.execute(f"SELECT COUNT(*) FROM {t}")
        local_count = local_cursor.fetchone()[0]

        cloud_cursor.execute(f"SELECT COUNT(*) FROM {t}")
        cloud_count = cloud_cursor.fetchone()[0]

        match = "✅" if local_count == cloud_count else "❌"
        if local_count != cloud_count:
            all_ok = False
        print(f"  {t:25s} {local_count:>8d} {cloud_count:>8d} {match:>8s}")

    # Engine-Check auf Cloud
    print(f"\n  Engine-Check (Cloud):")
    cloud_cursor.execute("""
        SELECT TABLE_NAME, ENGINE
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = %s ORDER BY TABLE_NAME
    """, (CLOUD['database'],))
    for row in cloud_cursor.fetchall():
        status = "✅" if row[1] == 'InnoDB' else "❌"
        print(f"    {status} {row[0]} → {row[1]}")

    # FK-Check auf Cloud
    print(f"\n  FK-Constraints (Cloud):")
    cloud_cursor.execute("""
        SELECT CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME
        FROM information_schema.KEY_COLUMN_USAGE
        WHERE TABLE_SCHEMA = %s AND REFERENCED_TABLE_NAME IS NOT NULL
    """, (CLOUD['database'],))
    fks = cloud_cursor.fetchall()
    for fk in fks:
        print(f"    ✅ {fk[0]}: {fk[1]} → {fk[2]}")
    if not fks:
        print(f"    ❌ Keine FK-Constraints gefunden!")
        all_ok = False

    # User-Check auf Cloud
    print(f"\n  Benutzer-Check (Cloud):")
    for user in ['bp_benutzer', 'bp_management', 'bp_admin']:
        try:
            cloud_cursor.execute(f"SHOW GRANTS FOR '{user}'@'%'")
            grants = cloud_cursor.fetchall()
            print(f"    ✅ {user}: {len(grants)} Grant(s)")
        except mysql.connector.Error:
            print(f"    ❌ {user}: Nicht gefunden!")
            all_ok = False

    local_cursor.close()
    local_conn.close()
    cloud_cursor.close()
    cloud_conn.close()

    print(f"\n  {'='*50}")
    if all_ok:
        print(f"  ✅ MIGRATION ERFOLGREICH – Alle Daten stimmen überein!")
    else:
        print(f"  ⚠️  MIGRATION MIT WARNUNGEN – Bitte prüfen!")
    print(f"  {'='*50}")


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("LB3: Automatisierte Migration lokal → Cloud")
    print("Robin Nydegger, PE24c")
    print("=" * 60)

    # Prüfe ob Tools vorhanden
    if not os.path.exists(MYSQLDUMP):
        print(f"[FEHLER] mysqldump nicht gefunden: {MYSQLDUMP}")
        print(f"Bitte Pfad in MYSQLDUMP anpassen!")
        sys.exit(1)

    if CLOUD['host'].startswith('DEIN-'):
        print("\n[HINWEIS] Cloud-Konfiguration noch nicht gesetzt!")
        print("Bitte in der Datei die CLOUD-Variable anpassen:")
        print("  - host: Dein RDS-Endpoint")
        print("  - password: Dein RDS Master-Passwort")
        print("\nDanach Script erneut ausführen.")
        sys.exit(0)

    # Phase 1: Dump
    dump = create_dump()

    # Phase 2: Import
    import_to_cloud(dump)

    # Phase 3: DCL
    setup_cloud_dcl()

    # Phase 4: Validierung
    validate_migration()

    print("\n[FERTIG] Migration abgeschlossen!")
    print(f"Cloud-DB erreichbar unter: {CLOUD['host']}:{CLOUD['port']}")


if __name__ == '__main__':
    main()

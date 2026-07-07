"""
LB3: Datenimport – Backpacker DB
Robin Nydegger, PE24c

Dieses Script:
  1. Entpackt backpacker_lb3.csv.zip
  2. Liest alle CSV-Dateien
  3. Importiert die Daten in die richtige Reihenfolge (Stammdaten zuerst)
  4. Bereinigt FK-Inkonsistenzen
  5. Gibt ein Testprotokoll aus

Voraussetzung: pip install mysql-connector-python
Ausführen:     python 02_import_daten.py
"""

import zipfile
import csv
import os
import sys

try:
    import mysql.connector
except ImportError:
    print("FEHLER: mysql-connector-python nicht installiert!")
    print("Bitte ausführen: pip install mysql-connector-python")
    sys.exit(1)

# ============================================================
# KONFIGURATION – hier anpassen!
# ============================================================
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',           # <-- Dein root-Passwort hier
    'database': 'backpacker_robin',
    'charset': 'utf8mb4',
    'allow_local_infile': True,
}

# Pfad zur ZIP-Datei (relativ oder absolut)
ZIP_PATH = r'C:\Users\robin\Claude\Projects\M141-Harald\LB3-Praxisarbeit\backpacker_lb3.csv.zip'
EXTRACT_DIR = r'C:\Users\robin\OneDrive\Dokumente\GitHub\M141\files\LB3\csv_data'

# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def connect_db():
    """Verbindung zur DB herstellen."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"[OK] Verbunden mit {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        return conn
    except mysql.connector.Error as e:
        print(f"[FEHLER] DB-Verbindung: {e}")
        sys.exit(1)


def extract_zip():
    """ZIP entpacken und CSV-Dateien auflisten."""
    os.makedirs(EXTRACT_DIR, exist_ok=True)
    print(f"\n--- ZIP entpacken: {ZIP_PATH}")
    with zipfile.ZipFile(ZIP_PATH, 'r') as z:
        z.extractall(EXTRACT_DIR)
        files = z.namelist()
        for f in files:
            print(f"  [ENTPACKT] {f}")
    return files


def read_csv(filename):
    """CSV-Datei lesen und als Liste von Dicts zurückgeben."""
    filepath = os.path.join(EXTRACT_DIR, filename)
    # Verschiedene Encodings probieren
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                # Sniffer für Delimiter
                sample = f.read(2048)
                f.seek(0)
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
                reader = csv.DictReader(f, dialect=dialect)
                rows = list(reader)
                print(f"  [OK] {filename}: {len(rows)} Zeilen gelesen (Encoding: {enc}, Delimiter: '{dialect.delimiter}')")
                return rows
        except (UnicodeDecodeError, csv.Error):
            continue
    print(f"  [FEHLER] {filename}: Konnte nicht gelesen werden!")
    return []


def clean_value(val):
    """Leere Strings und 'NULL' zu None konvertieren."""
    if val is None:
        return None
    val = val.strip()
    if val == '' or val.upper() == 'NULL':
        return None
    return val


def safe_int(val):
    """String zu Int konvertieren, None bei Fehler."""
    val = clean_value(val)
    if val is None:
        return None
    try:
        return int(float(val))
    except (ValueError, TypeError):
        return None


def safe_decimal(val):
    """String zu Decimal konvertieren, 0.00 bei Fehler."""
    val = clean_value(val)
    if val is None:
        return 0.00
    try:
        return float(val)
    except (ValueError, TypeError):
        return 0.00


# ============================================================
# IMPORT-FUNKTIONEN (pro Tabelle)
# ============================================================

def import_land(cursor, rows):
    """tbl_land importieren."""
    print("\n--- Import: tbl_land")
    sql = "INSERT IGNORE INTO tbl_land (Land_ID, Land) VALUES (%s, %s)"
    count = 0
    for row in rows:
        land_id = safe_int(row.get('Land_ID') or row.get('land_id') or row.get('LandID'))
        land = clean_value(row.get('Land') or row.get('land'))
        if land_id is not None and land is not None:
            cursor.execute(sql, (land_id, land))
            count += 1
    print(f"  [OK] {count} Länder importiert")
    return count


def import_leistung(cursor, rows):
    """tbl_leistung importieren."""
    print("\n--- Import: tbl_leistung")
    sql = "INSERT IGNORE INTO tbl_leistung (LeistungID, Beschreibung) VALUES (%s, %s)"
    count = 0
    for row in rows:
        lid = safe_int(row.get('LeistungID') or row.get('leistungid') or row.get('Leistung_ID'))
        beschr = clean_value(row.get('Beschreibung') or row.get('beschreibung'))
        if lid is not None:
            cursor.execute(sql, (lid, beschr))
            count += 1
    print(f"  [OK] {count} Leistungen importiert")
    return count


def import_personen(cursor, rows):
    """tbl_personen importieren."""
    print("\n--- Import: tbl_personen")
    sql = """INSERT IGNORE INTO tbl_personen 
             (Personen_ID, Titel, Vorname, Name, Strasse, PLZ, Ort, Anrede, Telefon, erfasst, Sprache)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    count = 0
    for row in rows:
        pid = safe_int(row.get('Personen_ID') or row.get('personen_id'))
        if pid is None:
            continue
        cursor.execute(sql, (
            pid,
            clean_value(row.get('Titel', '')),
            clean_value(row.get('Vorname', '')),
            clean_value(row.get('Name', '')),
            clean_value(row.get('Strasse', '')),
            clean_value(row.get('PLZ', '')),
            clean_value(row.get('Ort', '')),
            clean_value(row.get('Anrede', '')),
            clean_value(row.get('Telefon', '')),
            clean_value(row.get('erfasst', '')),
            clean_value(row.get('Sprache', '')),
        ))
        count += 1
    print(f"  [OK] {count} Personen importiert")
    return count


def import_benutzer(cursor, rows):
    """tbl_benutzer importieren."""
    print("\n--- Import: tbl_benutzer")
    sql = """INSERT IGNORE INTO tbl_benutzer 
             (Benutzer_ID, Benutzername, Password, Vorname, Name, Benutzergruppe, deaktiviert, aktiv)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    count = 0
    for row in rows:
        bid = safe_int(row.get('Benutzer_ID') or row.get('benutzer_id'))
        if bid is None:
            continue
        deaktiviert = clean_value(row.get('deaktiviert', ''))
        if deaktiviert is None:
            deaktiviert = '1000-01-01'
        cursor.execute(sql, (
            bid,
            clean_value(row.get('Benutzername', '')) or '',
            clean_value(row.get('Password', '')),
            clean_value(row.get('Vorname', '')),
            clean_value(row.get('Name', '')),
            safe_int(row.get('Benutzergruppe', '1')) or 1,
            deaktiviert,
            safe_int(row.get('aktiv', '1')) or 1,
        ))
        count += 1
    print(f"  [OK] {count} Benutzer importiert")
    return count


def import_buchung(cursor, rows):
    """tbl_buchung importieren – FK-Check gegen tbl_personen und tbl_land."""
    print("\n--- Import: tbl_buchung")
    
    # Bestehende IDs laden für FK-Check
    cursor.execute("SELECT Personen_ID FROM tbl_personen")
    valid_personen = {r[0] for r in cursor.fetchall()}
    cursor.execute("SELECT Land_ID FROM tbl_land")
    valid_land = {r[0] for r in cursor.fetchall()}
    
    sql = """INSERT IGNORE INTO tbl_buchung 
             (Buchungs_ID, Personen_FS, Ankunft, Abreise, Land_FS)
             VALUES (%s, %s, %s, %s, %s)"""
    count = 0
    skipped_person = 0
    skipped_land = 0
    for row in rows:
        bid = safe_int(row.get('Buchungs_ID') or row.get('buchungs_id'))
        if bid is None:
            continue
        
        personen_fs = safe_int(row.get('Personen_FS') or row.get('personen_fs'))
        land_fs = safe_int(row.get('Land_FS') or row.get('land_fs'))
        
        # FK-Bereinigung: ungültige FKs auf NULL setzen
        if personen_fs is not None and personen_fs not in valid_personen:
            skipped_person += 1
            personen_fs = None
        if land_fs is not None and land_fs not in valid_land:
            skipped_land += 1
            land_fs = None
        
        cursor.execute(sql, (
            bid,
            personen_fs,
            clean_value(row.get('Ankunft', '')),
            clean_value(row.get('Abreise', '')),
            land_fs,
        ))
        count += 1
    
    print(f"  [OK] {count} Buchungen importiert")
    if skipped_person > 0:
        print(f"  [WARNUNG] {skipped_person} ungültige Personen_FS → NULL gesetzt")
    if skipped_land > 0:
        print(f"  [WARNUNG] {skipped_land} ungültige Land_FS → NULL gesetzt")
    return count


def import_positionen(cursor, rows):
    """tbl_positionen importieren – FK-Check gegen tbl_buchung, tbl_benutzer, tbl_leistung."""
    print("\n--- Import: tbl_positionen")
    
    # Bestehende IDs laden für FK-Check
    cursor.execute("SELECT Buchungs_ID FROM tbl_buchung")
    valid_buchung = {r[0] for r in cursor.fetchall()}
    cursor.execute("SELECT Benutzer_ID FROM tbl_benutzer")
    valid_benutzer = {r[0] for r in cursor.fetchall()}
    cursor.execute("SELECT LeistungID FROM tbl_leistung")
    valid_leistung = {r[0] for r in cursor.fetchall()}
    
    sql = """INSERT IGNORE INTO tbl_positionen 
             (Positions_ID, Buchungs_FS, Konto, Anzahl, Preis, Rabatt, 
              Benutzer_FS, erfasst, Leistung_Text, Leistung_FS)
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    count = 0
    warn_buchung = 0
    warn_benutzer = 0
    warn_leistung = 0
    
    for row in rows:
        pid = safe_int(row.get('Positions_ID') or row.get('positions_id'))
        if pid is None:
            continue
        
        buchungs_fs = safe_int(row.get('Buchungs_FS') or row.get('buchungs_fs'))
        benutzer_fs = safe_int(row.get('Benutzer_FS') or row.get('benutzer_fs'))
        leistung_fs = safe_int(row.get('Leistung_FS') or row.get('leistung_fs'))
        
        # FK-Bereinigung
        if buchungs_fs is not None and buchungs_fs not in valid_buchung:
            warn_buchung += 1
            buchungs_fs = None
        if benutzer_fs is not None and benutzer_fs not in valid_benutzer:
            warn_benutzer += 1
            benutzer_fs = 0  # Default 0, da NOT NULL
        if leistung_fs is not None and leistung_fs not in valid_leistung:
            warn_leistung += 1
            leistung_fs = None
        
        erfasst = clean_value(row.get('erfasst', ''))
        if erfasst is None:
            erfasst = '2000-01-01 00:00:00'
        
        cursor.execute(sql, (
            pid,
            buchungs_fs,
            safe_int(row.get('Konto', '0')) or 0,
            safe_int(row.get('Anzahl', '0')) or 0,
            safe_decimal(row.get('Preis', '0')),
            safe_decimal(row.get('Rabatt', '0')),
            benutzer_fs if benutzer_fs is not None else 0,
            erfasst,
            clean_value(row.get('Leistung_Text', '')) or '',
            leistung_fs,
        ))
        count += 1
    
    print(f"  [OK] {count} Positionen importiert")
    if warn_buchung > 0:
        print(f"  [WARNUNG] {warn_buchung} ungültige Buchungs_FS → NULL gesetzt")
    if warn_benutzer > 0:
        print(f"  [WARNUNG] {warn_benutzer} ungültige Benutzer_FS → 0 gesetzt")
    if warn_leistung > 0:
        print(f"  [WARNUNG] {warn_leistung} ungültige Leistung_FS → NULL gesetzt")
    return count


# ============================================================
# VALIDIERUNG
# ============================================================

def validate(cursor):
    """Datenkonsistenz prüfen und Testprotokoll ausgeben."""
    print("\n" + "=" * 60)
    print("TESTPROTOKOLL – Datenkonsistenz")
    print("=" * 60)
    
    # Zeilenzählung
    tables = ['tbl_land', 'tbl_leistung', 'tbl_personen', 'tbl_benutzer', 'tbl_buchung', 'tbl_positionen']
    print("\n--- Zeilenzählung:")
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        count = cursor.fetchone()[0]
        print(f"  {t:25s} → {count:>6} Datensätze")
    
    # Engine-Check
    print("\n--- Engine-Check (alle InnoDB?):")
    cursor.execute("""
        SELECT TABLE_NAME, ENGINE 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME
    """, (DB_CONFIG['database'],))
    for row in cursor.fetchall():
        status = "✅" if row[1] == 'InnoDB' else "❌"
        print(f"  {status} {row[0]:25s} → {row[1]}")
    
    # Duplikate-Check
    print("\n--- Duplikate-Check (PK):")
    for t, pk in [('tbl_land', 'Land_ID'), ('tbl_personen', 'Personen_ID'), 
                   ('tbl_benutzer', 'Benutzer_ID'), ('tbl_buchung', 'Buchungs_ID'),
                   ('tbl_positionen', 'Positions_ID'), ('tbl_leistung', 'LeistungID')]:
        cursor.execute(f"SELECT {pk}, COUNT(*) c FROM {t} GROUP BY {pk} HAVING c > 1")
        dupes = cursor.fetchall()
        if dupes:
            print(f"  ❌ {t}: {len(dupes)} Duplikate!")
        else:
            print(f"  ✅ {t}: Keine Duplikate")
    
    # FK-Konsistenz
    print("\n--- FK-Konsistenz:")
    checks = [
        ("tbl_buchung.Personen_FS → tbl_personen", 
         "SELECT COUNT(*) FROM tbl_buchung b LEFT JOIN tbl_personen p ON b.Personen_FS = p.Personen_ID WHERE b.Personen_FS IS NOT NULL AND p.Personen_ID IS NULL"),
        ("tbl_buchung.Land_FS → tbl_land",
         "SELECT COUNT(*) FROM tbl_buchung b LEFT JOIN tbl_land l ON b.Land_FS = l.Land_ID WHERE b.Land_FS IS NOT NULL AND l.Land_ID IS NULL"),
        ("tbl_positionen.Buchungs_FS → tbl_buchung",
         "SELECT COUNT(*) FROM tbl_positionen p LEFT JOIN tbl_buchung b ON p.Buchungs_FS = b.Buchungs_ID WHERE p.Buchungs_FS IS NOT NULL AND b.Buchungs_ID IS NULL"),
        ("tbl_positionen.Leistung_FS → tbl_leistung",
         "SELECT COUNT(*) FROM tbl_positionen p LEFT JOIN tbl_leistung l ON p.Leistung_FS = l.LeistungID WHERE p.Leistung_FS IS NOT NULL AND l.LeistungID IS NULL"),
    ]
    for label, sql in checks:
        cursor.execute(sql)
        orphans = cursor.fetchone()[0]
        status = "✅" if orphans == 0 else f"⚠️  {orphans} verwaiste"
        print(f"  {status} {label}")
    
    print("\n" + "=" * 60)
    print("Import & Validierung abgeschlossen!")
    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():
    print("=" * 60)
    print("LB3: Backpacker DB – Datenimport")
    print("Robin Nydegger, PE24c")
    print("=" * 60)
    
    # 1. ZIP entpacken
    csv_files = extract_zip()
    
    # 2. CSV-Dateien einlesen
    print("\n--- CSV-Dateien lesen:")
    data = {}
    for f in csv_files:
        if f.endswith('.csv'):
            name = os.path.splitext(os.path.basename(f))[0].lower()
            # Versuche den Tabellennamen zu erkennen
            rows = read_csv(f)
            if rows:
                data[name] = rows
                # Spalten anzeigen
                print(f"    Spalten: {list(rows[0].keys())}")
    
    if not data:
        print("[FEHLER] Keine CSV-Dateien gefunden!")
        sys.exit(1)
    
    # 3. DB-Verbindung
    conn = connect_db()
    cursor = conn.cursor()
    
    # FK-Checks temporär deaktivieren für sauberen Import
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    
    try:
        # 4. Import in der richtigen Reihenfolge (Stammdaten zuerst)
        # Die CSV-Dateinamen müssen zum Tabellennamen passen
        # Flexibel: suche nach Teilstrings
        
        for key, rows in data.items():
            if 'land' in key and 'leistung' not in key:
                import_land(cursor, rows)
            elif 'leistung' in key:
                import_leistung(cursor, rows)
            elif 'personen' in key or 'person' in key and 'benutzer' not in key:
                import_personen(cursor, rows)
            elif 'benutzer' in key:
                import_benutzer(cursor, rows)
        
        # Dann abhängige Tabellen
        for key, rows in data.items():
            if 'buchung' in key and 'position' not in key:
                import_buchung(cursor, rows)
        
        for key, rows in data.items():
            if 'position' in key:
                import_positionen(cursor, rows)
        
        # FK-Checks wieder aktivieren
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        conn.commit()
        print("\n[OK] Alle Daten committed!")
        
        # 5. Validierung
        validate(cursor)
        
    except Exception as e:
        conn.rollback()
        print(f"\n[FEHLER] Import fehlgeschlagen: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    main()

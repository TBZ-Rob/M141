# M141 – Prüfungsvorbereitung LB2
**Tag 1–6 | Theorie & Praxis**

---

## TAG 1 – Grundlagen, DB-Modelle, XAMPP

### Begriffe

| Begriff | Bedeutung |
|---|---|
| **DBS** (Datenbanksystem) | Logische Einheit zur Verwaltung strukturierter Daten |
| **DBMS** | Database Management System – die Software/Engine (z.B. mysqld) |
| **Datenbasis** | Die eigentlichen Daten (Schema + Daten) |
| **DB-Server** | Rechner/Prozess, der Datenbankdienste bereitstellt |
| **DB-Client** | Programm, das auf den Server zugreift (mysql.exe, phpMyAdmin, Workbench) |

### DB-Modelle

| Typ | Beispiel |
|---|---|
| **Relational (RDBMS)** | MySQL, MariaDB, PostgreSQL, Oracle, MS Access |
| **Dokumentenorientiert** | MongoDB, CouchDB, Cassandra |
| **Key-Value** | Redis, DynamoDB |
| **Graphdatenbank** | Neo4j |
| **Wide Column** | HBase, Cassandra |

**Heute am häufigsten:** Relationale Datenbank (RDBMS)

### MySQL vs MariaDB

- **MySQL**: Entwickelt ~1994, seit 2010 bei Oracle
- **MariaDB**: Fork von MySQL 5.5 durch Michael Widenius, unter GPL, wird von Wikipedia verwendet
- Für dieses Modul: Unterschied unwesentlich – beide benutzen SQL, gleiche Clients

### Serverkomponenten

| Komponente | Beschreibung |
|---|---|
| `mysqld.exe` | **Server-Daemon** – muss laufen für alle Verbindungen |
| `mysql.exe` | Kommandozeilen-**Client** |
| `phpMyAdmin` | Web-basierter **Client** |
| MySQL Workbench | GUI-**Client** |
| `my.ini` | Konfigurationsdatei (kein Client/Server, sondern Konfiguration) |

### Client/Server-Modell

- **Client** (Frontend): Dialog- und Präsentationsaufgaben beim Benutzer
- **Server** (Backend): Zentrale Dienste, Datenspeicherung, Zugriffskontrolle
- Vorteil ggü. Desktop-DB: Mehrbenutzer, Sicherheit, Skalierbarkeit, zentrale Verwaltung

### Wichtige Befehle

```sql
-- Server-Status anzeigen
STATUS;

-- Datenbanken anzeigen
SHOW DATABASES;

-- Server starten ohne Passwortprüfung (Notfall!)
c:\xampp\mysql\bin\mysqld --skip-grant-tables
```

---

## TAG 2 – Konfiguration (my.ini), Zeichensätze, SQL-Grundlagen

### Optionsdatei my.ini / my.cnf

- Windows: `my.ini`, Linux: `my.cnf`
- Wird beim Start gesucht in (Reihenfolge): `C:\Windows\my.ini` → `C:\my.ini` → `INSTALLDIR\my.ini` → ...
- **Zuletzt gelesener Wert gilt** – Kommandozeilenparameter haben Vorrang

```ini
[mysqld]          # Server-Einstellungen
language=german

[mysql]           # Client-Einstellungen
user=meier
```

Alle Parameter anzeigen:
```cmd
mysqld --verbose --help
```

### Zeichensätze

| Kodierung | Merkmale |
|---|---|
| **ASCII** | 7-Bit, nur Englisch, veraltet |
| **Latin1 (ISO-8859-1)** | Westeuropäisch, kein Emoji |
| **UTF-8** | Unicode, 1–4 Bytes pro Zeichen, >98% aller Websites |
| **UTF-16** | 2 Bytes Minimum (Java) |

**Empfehlung:** Immer `utf8mb4` verwenden (unterstützt auch Emojis)

### Kollation (Sortierfolge)

| Kollation | Eigenschaft |
|---|---|
| `utf8mb4_general_ci` | Schnell, nicht 100% Unicode-konform, case-insensitive |
| `utf8mb4_unicode_ci` | Exakt nach Unicode-Standard, etwas langsamer |
| `utf8mb4_german2_ci` | Telefonbuch-Sortierung (ä=ae, ö=oe, ü=ue) |
| `latin1_german1_ci` | Wörterbuch-Sortierung (ä=a, ö=o, ü=u) |
| `latin1_general_cs` | Case-sensitive (A ≠ a) |

**Suffix:** `_ci` = case-insensitive | `_cs` = case-sensitive

Kollation anzeigen: `SHOW COLLATION;`

### SQL-Befehlsgruppen

| Gruppe | Befehle |
|---|---|
| **DDL** (Data Definition) | `CREATE`, `ALTER`, `DROP`, `RENAME` |
| **DML** (Data Manipulation) | `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` |
| **DQL/DRL** (Data Query) | `SELECT`, `SHOW`, `DESCRIBE` |
| **DCL** (Data Control) | `GRANT`, `REVOKE` |
| **TCL** (Transaction Control) | `BEGIN`, `COMMIT`, `ROLLBACK` |

### Datenimport

```cmd
-- SQL-Skript ausführen (CMD):
mysql -u root -p db < pfad\script.sql

-- CSV importieren:
LOAD DATA INFILE 'datei.csv' INTO TABLE tabelle
FIELDS TERMINATED BY ';';

-- Backup erstellen:
mysqldump -u root -p firma > backup.sql

-- Im MySQL-Client:
mysql> source pfad\script.sql
```

### Tabellenstruktur prüfen

```sql
DESCRIBE tabellenname;
SHOW CREATE TABLE tabellenname;
```

---

## TAG 3 – Tabellentypen & Transaktionen (ACID)

### Tabellentypen im Vergleich

| Eigenschaft | ARIA (früher MyISAM) | InnoDB |
|---|---|---|
| Transaktionen | ❌ (MyISAM) / einfach (ARIA) | ✅ voll |
| Referentielle Integrität | ❌ | ✅ |
| Locking | **Table-Level** | **Row-Level** |
| Speicherplatz | weniger | mehr |
| Speicherdateien | `.FRM` + `.MAD/.MYD` + `.MAI/.MYI` | `.FRM` + `.ibd` + Tablespace |
| Einsatz | Viele Daten, Geschwindigkeit | Sicherheit, viele gleichzeitige Schreibzugriffe |

> **Standard heute:** InnoDB (seit MySQL/MariaDB-Standard)

> ⚠️ Tabellen der `mysql`-Datenbank (Benutzerverwaltung) dürfen **nicht** auf InnoDB umgestellt werden!

### Tablespace (InnoDB)

- Zentrale Datei `ibdata1` – virtueller Speicher für alle InnoDB-Tabellen
- Startet mit 10 MB, wächst in 8-MB-Schritten (`autoextend`)
- **Kann nicht verkleinert werden** (nur via Dump → neu aufsetzen)

```sql
-- Tabellentyp ändern:
ALTER TABLE tabellenname ENGINE = InnoDB;

-- Tablespace-Belegung anzeigen:
SELECT SPACE, NAME, ROUND((ALLOCATED_SIZE/1024/1024), 2) AS "MB"
FROM information_schema.INNODB_SYS_TABLESPACES ORDER BY 3 DESC;
```

### Transaktionen

**Zweck:** Mehrere SQL-Befehle werden als **unteilbare Einheit** ausgeführt – *ganz oder gar nicht*.

```sql
BEGIN;  -- oder START TRANSACTION

  UPDATE tbl_konto SET Saldo = Saldo - 1000 WHERE name = 'Von';
  UPDATE tbl_konto SET Saldo = Saldo + 1000 WHERE name = 'Nach';

COMMIT;   -- Änderungen speichern
-- oder
ROLLBACK; -- Alles widerrufen
```

### Autocommit

```sql
-- Autocommit ausschalten (alle Befehle gelten als Transaktion):
SET AUTOCOMMIT = 0;

-- Standard:
SET AUTOCOMMIT = 1;  -- jeder Befehl wird sofort ausgeführt
```

### Locking-Mechanismen

| Mechanismus | Beschreibung |
|---|---|
| **Table-Level-Locking** (ARIA) | Ganze Tabelle gesperrt |
| **Page-Level-Locking** (BDB) | Ganze Speicherseiten gesperrt |
| **Row-Level-Locking** (InnoDB) | Nur betroffene Zeilen gesperrt → effizient |

```sql
-- Exclusive Lock (für UPDATE):
BEGIN;
SELECT * FROM tabelle WHERE x > 10 FOR UPDATE;
COMMIT;

-- Shared Lock (nur lesen, andere dürfen auch lesen):
BEGIN;
SELECT * FROM tabelle WHERE x > 10 LOCK IN SHARE MODE;
COMMIT;

-- Deadlock diagnostizieren:
SHOW ENGINE INNODB STATUS;
```

### ACID-Prinzipien

| Buchstabe | Eigenschaft | Bedeutung |
|---|---|---|
| **A** | **Atomarität** | Alles oder nichts – keine halben Transaktionen |
| **C** | **Konsistenz** | Datenbank ist vor und nach der Transaktion konsistent |
| **I** | **Isoliertheit** | Transaktionen beeinflussen sich nicht gegenseitig |
| **D** | **Dauerhaftigkeit** | Abgeschlossene Transaktionen bleiben dauerhaft gespeichert |

---

## TAG 4 – Datenbanksicherheit & Netzwerkzugriff

### Authentifizierung (Wer darf rein?)

MySQL prüft **3 Informationen** beim Login:

| Info | Bedeutung |
|---|---|
| `Benutzername` | DB-Login-Name (≠ OS-Benutzer) |
| `Passwort` | Verschlüsselt als Hash gespeichert |
| `Hostname / IP` | Von wo darf der User zugreifen |

**Hostname-Optionen:**

| Hostname | Bedeutung |
|---|---|
| `localhost` | Nur lokal vom Server selbst |
| `%` | Von überall (extern, aber **nicht** lokal) |
| `172.16.17.111` | Nur von dieser IP |
| `172.16.17.%` | Aus diesem Subnetz |

### Benutzer verwalten

```sql
-- User erstellen:
CREATE USER 'username'@'localhost' IDENTIFIED BY 'Passw0rt';
CREATE USER 'user_rem'@'%' IDENTIFIED BY 'Passw0rt';

-- Passwort setzen:
SET PASSWORD FOR 'user'@'%' = PASSWORD('neuesPasswort');
FLUSH PRIVILEGES;  -- ⚠️ Nie vergessen!

-- User löschen:
DROP USER 'username'@'localhost';

-- Passwort als Hash anzeigen:
SELECT PASSWORD('TBZforever');
```

### Server absichern (nach Installation)

```sql
-- root-Passwort setzen:
SET PASSWORD FOR root@localhost = PASSWORD('superpasswort');
FLUSH PRIVILEGES;

-- root-Zugang von extern verhindern:
DROP USER 'root'@'%';
FLUSH PRIVILEGES;

-- Lokalen Zugang ohne Passwort erlauben (nur einloggen, keine Rechte):
GRANT USAGE ON *.* TO ''@localhost;
FLUSH PRIVILEGES;
```

> ⚠️ XAMPP hat per Default **kein Passwort** auf root – sofort ändern!

### Netzwerkzugriff (DB-Server im LAN)

```cmd
-- Verbindung testen:
ping 172.16.17.4
mysqladmin -h 172.16.17.4 -u remote -p ping

-- Als Remote-Client verbinden:
mysql -h 172.16.17.4 -u remote -p

-- Backup über Netz:
mysqldump -h 172.16.17.4 -u remote -p firma > backup.sql

-- Restore über Netz:
mysql -h 172.16.17.4 -u remote -p firma < backup.sql
```

```ini
-- Netzwerkzugriff verbieten (in my.ini):
[mysqld]
skip-networking
```

> Port 3306 muss in Firewall offen sein für externen Zugriff.

### Benutzerverwaltung prüfen

```sql
-- User-Tabelle anzeigen:
SELECT * FROM mysql.user;
SELECT * FROM mysql.global_priv;  -- echte Rohdaten (JSON) seit MariaDB 10.4
```

---

## TAG 5 – Zugriffsrechte (GRANT / REVOKE / Rollen)

### WAS – Privilegien

| Privileg | Beschreibung |
|---|---|
| `SELECT` | Daten lesen |
| `INSERT` | Daten einfügen |
| `UPDATE` | Daten ändern |
| `DELETE` | Daten löschen |
| `ALL PRIVILEGES` | Alle Rechte (außer GRANT OPTION) |
| `GRANT OPTION` | Eigene Rechte weitergeben |
| `USAGE` | Nur einloggen, keine Daten |
| `FILE` | Dateioperationen auf Server (`LOAD DATA INFILE`) |

### WO – Geltungsbereich (Ebenen)

| Ebene | Syntax | Bedeutung |
|---|---|---|
| **Global** | `ON *.*` | Ganzer Server, alle DBs |
| **Datenbank** | `ON mydb.*` | Alle Tabellen einer DB |
| **Tabelle** | `ON mydb.tabelle` | Nur diese Tabelle |
| **Spalte** | `(col1, col2) ON db.tb` | Nur diese Spalten |

### Wo werden Rechte gespeichert?

| Tabelle | Ebene |
|---|---|
| `mysql.global_priv` | Global (`*.*`) – auch Passwörter/User |
| `mysql.db` | Datenbank-Ebene |
| `mysql.tables_priv` | Tabellen-Ebene |
| `mysql.columns_priv` | Spalten-Ebene |

> `mysql.user` ist seit MariaDB 10.4 nur noch eine **View** auf `mysql.global_priv`

### GRANT und REVOKE

```sql
-- Syntax:
GRANT privileg ON wo TO user@host [WITH GRANT OPTION];
REVOKE privileg ON wo FROM user@host;

-- Beispiele:
GRANT ALL ON hotel.* TO hotel_admin@localhost WITH GRANT OPTION;
GRANT SELECT, INSERT, UPDATE, DELETE ON hotel.* TO hotel_user@localhost;
GRANT FILE ON *.* TO username@'%';

-- Rechte entziehen:
REVOKE SELECT ON hotel.* FROM hotel_user@localhost;

-- Rechte anzeigen:
SHOW GRANTS FOR hotel_admin@localhost;

-- Aktivieren (immer nötig!):
FLUSH PRIVILEGES;
```

### Rollen (ab MariaDB 10.x)

```sql
-- Rolle erstellen und Rechte zuweisen:
CREATE ROLE verkauf;
GRANT SELECT ON kunden.* TO verkauf;

-- User erstellen und Rolle zuweisen:
CREATE USER 'max'@'localhost' IDENTIFIED BY 'Passw0rt';
GRANT verkauf TO 'max'@'localhost';
FLUSH PRIVILEGES;

-- Rolle aktivieren (als eingeloggter User):
SET ROLE verkauf;
SELECT CURRENT_ROLE;

-- Standard-Rolle setzen (automatisch beim Login):
SET DEFAULT ROLE verkauf;
```

### Zugriffsmatrix (Beispiel)

| Tabelle | Verkauf (S/I/U/D) | Management (S/I/U/D) |
|---|---|---|
| `produkte` | S | S/I/U/D |
| `personal.lohn` | – | S/U |
| `rechnungen` | S | S/I/U/D |
| `kunden` | S/I/U | S/I/U/D |

*S=Select, I=Insert, U=Update, D=Delete*

### pma-User (phpMyAdmin)

```sql
-- Passwort setzen (nach Installation!):
SET PASSWORD FOR pma@localhost = PASSWORD('irgendwas');
FLUSH PRIVILEGES;
```

> Der `pma`-User darf nicht gelöscht werden – sonst funktioniert phpMyAdmin nicht mehr.

---

## TAG 6 – Server-Administration, Logging, Backup, Optimierung

### Die 4 Phasen im Produktivbetrieb

```
1. KONFIGURATION  →  2. ÜBERWACHUNG (Logging)  →  3. BACKUP & RECOVERY  →  4. OPTIMIERUNG
```

---

### 1. Konfiguration

**3 Wege zur Konfiguration:**

**A) my.ini / my.cnf bearbeiten** (Standard im Produktivbetrieb):
```ini
[mysqld]
language=german
log-error=C:/log/mysql_error.log
log-bin=mysql-bin
```

**B) Kommandozeilenparameter** beim Start:
```cmd
mysqld --language=german
```

**C) Systemvariablen** im laufenden Betrieb:
```sql
SHOW VARIABLES LIKE '%log%';
SET GLOBAL general_log = 1;
```

> ⚠️ Änderungen in my.ini werden erst nach **Server-Neustart** wirksam!

**Konfiguration prüfen (Syntax-Check):**
```cmd
mysqld.exe --validate-config
```

---

### 2. Logging (Überwachung)

| Log-Typ | Datei | Zweck | Aktiv? |
|---|---|---|---|
| **Error Log** | `mysql_error.log` | Start/Stop/Fehler | ✅ immer |
| **Binary Log** | `mysql-bin.000001` | Alle Datenänderungen → Recovery, Replikation | 🔧 manuell aktivieren |
| **General Query Log** | `<host>.log` | Alle Befehle (sehr groß!) | ⚠️ nur Debugging |
| **Slow Query Log** | `<host>-slow.log` | Langsame Abfragen → Optimierung | 🔍 für Performance |
| **Transaction Log** | `ib_logfile*` | InnoDB-Crash-Recovery | 📊 automatisch |

**Binary Log aktivieren (my.ini):**
```ini
[mysqld]
log-bin=mysql-bin
```

**Neue Log-Datei erzeugen:**
```sql
FLUSH LOGS;
```

**Binary Log lesen:**
```cmd
mysqlbinlog C:\...\mysql\data\mysql-bin.000001
```

**General Query Log aktivieren:**
```sql
SET GLOBAL general_log = 1;
```

---

### 3. Backup & Recovery

**Backup erstellen mit mysqldump:**
```cmd
-- Einfaches Backup:
mysqldump -u root -p firma > backup.sql

-- Optimiertes Backup (--opt empfohlen):
mysqldump --user=root --password=pwd --opt firma > backup.sql

-- Mit Read-Lock (Datenintegrität während Backup):
mysqldump --lock-tables firma > backup.sql

-- Alle Datenbanken:
mysqldump -u root -p --all-databases > alles.sql
```

**Wichtige mysqldump-Optionen:**

| Option | Bedeutung |
|---|---|
| `--opt` | Kombiniert: quick, add-drop-table, add-locks, extended-insert, lock-tables |
| `--lock-tables` | Tabellen für Backup sperren (READ LOCK) |
| `--single-transaction` | Konsistentes Backup ohne Locking (nur InnoDB) |
| `-F, --flush-logs` | Logs vor Dump leeren (sauberer Schnitt mit Binary Log) |
| `--add-drop-table` | `DROP TABLE IF EXISTS` vor jedem CREATE |
| `--compact` | Weniger Ausgabetext |

**Restore:**
```cmd
mysql -u root -p firma < backup.sql
```

**Recovery aus Binary Log** (nach dem Backup-Restore):
```cmd
-- Älteste zuerst!
mysqlbinlog mysql-bin.000001 | mysql -u root -p
mysqlbinlog mysql-bin.000002 | mysql -u root -p
```

> 🔁 **Zusammenspiel:** Backup = letzter Stand | Binary Log = Brücke zum Absturzzeitpunkt

---

### 4. Optimierung

**Was wird optimiert?**

| Bereich | Maßnahme |
|---|---|
| Datenbankstruktur | Minimaler Speicherplatz, Index-Verwendung |
| Abfragen | Mit `EXPLAIN` analysieren |
| Locks | Geschwindigkeit durch gezieltes Sperren |
| Server | Parameter in my.ini optimieren |

**Indizes:**
- Beschleunigen `SELECT`, `ORDER BY`, `JOIN`
- Verlangsamen `INSERT`, `UPDATE`, `DELETE` (Index muss mitgepflegt werden)
- Sinnvoll ab ~10.000 Datensätzen oder wenn DB > RAM

```sql
-- Index erstellen:
CREATE INDEX idx_name ON tabelle (spalte);

-- Index löschen:
DROP INDEX idx_name ON tabelle;

-- Abfrage analysieren (Ausführungsplan):
EXPLAIN SELECT COUNT(*) FROM buchung, person WHERE buchung.PersID = person.PersID;
```

**EXPLAIN-Ausgabe lesen:**
- `key` = verwendeter Index (`NULL` = kein Index → Problem!)
- `rows` = Anzahl untersuchter Zeilen (möglichst klein)

**Index-Tipps:**

| ✅ Gut für Index | ❌ Nicht optimierbar |
|---|---|
| Primär- und Fremdschlüssel | `NOT`, `<>` |
| Häufig sortierte Spalten | `LIKE '%muster'` (% am Anfang) |
| JOIN-Spalten | Funktionen in WHERE-Klausel |

**Tabelle optimieren (Speicher defragmentieren):**
```sql
OPTIMIZE TABLE person;
```

**Wichtige Speicherparameter (my.ini):**
```ini
key_buffer_size = 16M       -- Speicher für Indizes
table_cache = 64            -- Max. geöffnete Tabellen
sort_buffer = 2M            -- Sortier-Buffer
read_buffer_size = 128K     -- Sequentielles Lesen
```

**Query Cache:**
```ini
query_cache_size = 32M
query_cache_type = 1        -- 0=Off, 1=On, 2=Demand
query_cache_limit = 50K     -- Max. Größe pro Query
```

```sql
-- Cache leeren:
RESET QUERY CACHE;

-- Status anzeigen:
SHOW STATUS;
```

---

## SCHNELLREFERENZ: Wichtigste SQL-Befehle

```sql
-- === BENUTZERVERWALTUNG ===
CREATE USER 'name'@'host' IDENTIFIED BY 'passwort';
DROP USER 'name'@'host';
SET PASSWORD FOR 'name'@'host' = PASSWORD('neu');
FLUSH PRIVILEGES;  -- immer nach Änderungen!

-- === RECHTE ===
GRANT SELECT, INSERT ON db.* TO 'name'@'host';
GRANT ALL ON *.* TO 'admin'@'localhost';
REVOKE SELECT ON db.* FROM 'name'@'host';
SHOW GRANTS FOR 'name'@'host';

-- === ROLLEN ===
CREATE ROLE rolle;
GRANT SELECT ON db.* TO rolle;
GRANT rolle TO 'user'@'host';
SET ROLE rolle;

-- === TRANSAKTIONEN ===
BEGIN;
  -- SQL-Befehle
COMMIT;   -- oder ROLLBACK;
SET AUTOCOMMIT = 0;

-- === TABELLENTYPEN ===
ALTER TABLE tabelle ENGINE = InnoDB;
SHOW TABLE STATUS;

-- === LOGGING ===
SHOW VARIABLES LIKE '%log%';
SET GLOBAL general_log = 1;
FLUSH LOGS;

-- === STATUS ===
STATUS;
SHOW VARIABLES;
SHOW STATUS;
SHOW ENGINE INNODB STATUS;
```

---

## PRÜFUNGSTIPPS

### Theorie-Teil (20–30 min, Spick erlaubt)

Folgende Konzepte gut kennen:
1. **ACID** – alle 4 Eigenschaften erklären können
2. **ARIA vs InnoDB** – Unterschiede, wann welcher Typ?
3. **Authentifizierung vs Autorisierung** – was prüft was?
4. **GRANT/REVOKE Syntax** – auswendig können
5. **Logging-Typen** – welches Log wozu?
6. **Backup + Binary Log** – Zusammenspiel erklären

### Praxis-Teil (40–60 min, Openbook)

Typische Aufgaben:
- User erstellen, Rechte vergeben, testen
- Rollen erstellen und zuweisen
- Backup erstellen und wiederherstellen
- Logging aktivieren und auslesen
- EXPLAIN auf eine Abfrage anwenden
- Konfiguration in my.ini anpassen

### Häufige Fehler vermeiden

| ❌ Fehler | ✅ Richtig |
|---|---|
| `FLUSH PRIVILEGES` vergessen | Nach jeder Rechteänderung ausführen |
| Falscher Hostname beim User | `localhost` ≠ `%` |
| Binary Log nicht aktiv | Vor Recovery prüfen: `SHOW VARIABLES LIKE 'log_bin';` |
| Tabellentyp-Tabellen (mysql.*) umstellen | `mysql`-DB-Tabellen immer MyISAM/ARIA lassen |
| Passwort im Klartext in Script | `mysql_config_editor` oder `--defaults-extra-file` verwenden |

---

*M141 – DB-Systeme in Betrieb nehmen | TBZ 2025/2026*

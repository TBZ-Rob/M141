# 7. Tag – Datenbank mit Testdaten testen

![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)
![Datum](https://img.shields.io/badge/Datum-23.06.26-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ 6. Tag](../6.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [8. Tag ➡️](../8.Tag/README.md)

Am letzten inhaltlichen Tag vor LB2 geht es darum, eine Datenbank **systematisch zu testen**: Benutzer anlegen, Testdaten laden, Berechtigungen prüfen, Datenintegrität sicherstellen und Performance mit und ohne Indizes vergleichen.

## 🎯 Lernziele

| | Lernziel |
|---|----------|
| 👥 | Test-User mit Rollen erstellen und Berechtigungen prüfen |
| 📦 | Grosse Datenmengen per Bulk-Import laden (LOAD DATA INFILE) |
| 🔍 | Datenintegrität sicherstellen (PK, FK, Eindeutigkeit, Constraints) |
| ⚡ | Performance mit und ohne Indizes vergleichen (EXPLAIN) |
| 🧪 | Weitere Tests: Negativ-/Grenztests, Transaktionen, Backup/Restore, Nebenläufigkeit |
| 📊 | Benchmark-Test mit `mysqlslap` durchführen |

---

## 🗂️ Vorgehen im Überblick

Das Testprotokoll folgt einem **strukturierten Ablauf** von 15 Schritten:

| Schritt | Aktion |
|---------|--------|
| 1 | Login mit Test-User (scheitert – User existiert noch nicht) |
| 2 | User erstellen und Login testen |
| 3 | Schema und Tabellen erstellen (ohne PK/Index) |
| 4 | Bulk-Import: je 400'000 Datensätze laden |
| 5 | Berechtigungen über Rollen konfigurieren (RBAC) |
| 6 | Berechtigungen mit Test-Usern prüfen |
| 7 | Datenintegrität sicherstellen |
| 8–12 | Performance-Tests (ohne Index → mit Index → Vergleich) |
| 13 | Weitere Tests (Negativ, Transaktionen, Backup, Locking) |
| 14 | Benchmark mit `mysqlslap` |
| 15 | Schlussbilanz |

---

## 👥 User erstellen & Login testen

Zwei Test-User werden angelegt:

```sql
CREATE USER 'Reader' IDENTIFIED BY '123!';
CREATE USER 'Contributor' IDENTIFIED BY '123!';
```

> ⚠️ Einige MariaDB-Versionen erstellen hierbei **4 User** – je einen mit Hostname `%` (mit Passwort) und einen mit `localhost` (ohne Passwort). Im produktiven Betrieb die `localhost`-User ohne Passwort wieder löschen!

---

## 📦 Schema, Tabellen & Bulk-Import

Die Tabellen werden **bewusst ohne Primary Key und Indizes** erstellt – um später den Performance-Unterschied zu demonstrieren:

```sql
CREATE SCHEMA IF NOT EXISTS myTestDb DEFAULT CHARACTER SET utf8mb4;
USE myTestDb;

CREATE TABLE Person (
    Id INT,
    Vorname VARCHAR(255),
    Nachname VARCHAR(255),
    Email VARCHAR(255),
    AdresseId INT
);

CREATE TABLE Adresse (
    Id INT,
    Strasse VARCHAR(255),
    Hausnummer VARCHAR(10),
    PLZ VARCHAR(10),
    Stadt VARCHAR(255),
    Bundesstaat VARCHAR(10)
);
```

**Bulk-Import** mit je 400'000 Datensätzen aus CSV-Dateien:

```sql
LOAD DATA INFILE './person.csv'
INTO TABLE Person
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
-- Query OK, 400000 rows affected (3.7 sec)

LOAD DATA INFILE './adresse.csv'
INTO TABLE Adresse
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;
-- Query OK, 400003 rows affected (3.5 sec)
```

---

## 🔐 Berechtigungen über Rollen (RBAC)

| Zugriffsmatrix | Reader: S | I | U | D | Contributor: S | I | U | D |
|---------------|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| Person | ✅ | | | | ✅ | ✅ | ✅ | ✅ |
| Adresse | ✅ | | | | ✅ | ✅ | ✅ | ✅ |

*S = Select, I = Insert, U = Update, D = Delete*

```sql
-- Rollen erstellen
CREATE ROLE 'RoleReader', 'RoleContributor';
GRANT SELECT ON myTestDb.* TO 'RoleReader';
GRANT SELECT, INSERT, UPDATE, DELETE ON myTestDb.* TO 'RoleContributor';

-- Rollen zuweisen
GRANT 'RoleReader' TO 'Reader'@'localhost';
GRANT 'RoleContributor' TO 'Contributor'@'localhost';

-- Default-Rollen setzen (automatisch aktiv beim Login)
SET DEFAULT ROLE 'RoleReader' TO 'Reader'@'localhost';
SET DEFAULT ROLE 'RoleContributor' TO 'Contributor'@'localhost';

FLUSH PRIVILEGES;
```

**Test:** Reader kann `SELECT` ausführen, aber `UPDATE` wird abgelehnt (`ERROR 1142`). Contributor kann alle CRUD-Operationen durchführen.

---

## 🔍 Datenintegrität sicherstellen

Mehrere Aspekte der Datenqualität müssen geprüft werden:

| Aspekt | Prüfung |
|--------|---------|
| **Eindeutigkeit** | Doppelte IDs finden mit `GROUP BY ... HAVING COUNT > 1` |
| **Referenzielle Integrität** | FK-Constraints setzen: `FOREIGN KEY (AdresseId) REFERENCES Adresse(Id)` |
| **Datentypen** | Stichproben prüfen (z.B. PLZ als String, nicht Integer) |
| **Datenbeschränkungen** | CHECK-Constraints einsetzen: `CHECK (Age >= 0)` |

**Duplikate finden und bereinigen:**

```sql
-- Doppelte Adressen finden
SELECT Id FROM Adresse
GROUP BY Id
HAVING COUNT(Id) > 1;
-- Ergebnis: 3 doppelte IDs (44738, 133344, 234426)

-- Duplikate löschen (je einen behalten)
DELETE FROM Adresse WHERE Id=44738 LIMIT 1;
DELETE FROM Adresse WHERE Id=133344 LIMIT 1;
DELETE FROM Adresse WHERE Id=234426 LIMIT 1;

-- Primary Keys setzen (nach Bereinigung)
ALTER TABLE Adresse ADD PRIMARY KEY (Id);
ALTER TABLE Person ADD PRIMARY KEY (Id);
```

---

## ⚡ Performance-Tests: Index-Vergleich

Die gleiche JOIN-Abfrage wird **drei Mal** gemessen – ohne Index, mit einem Index und mit zwei Indizes:

```sql
SELECT * FROM Person p
INNER JOIN Adresse a ON a.Id = p.AdresseId
WHERE p.Id = 2569;
```

| Test | Index auf | Dauer | Faktor |
|------|----------|-------|--------|
| **Ohne Index** | – | ~9.5 s | 1× (Baseline) |
| **1 Index** | `Person.AdresseId` | ~1.2 s | **~8× schneller** |
| **2 Indizes** | `Person.AdresseId` + `Adresse.Id` | ~0.16 s | **~60× schneller** |

```sql
-- Indizes erstellen
CREATE INDEX idx_AdresseId ON Person (AdresseId);
CREATE INDEX idx_Id ON Adresse (Id);
```

Mit `EXPLAIN` lässt sich der Unterschied im Ausführungsplan sehen: Ohne Index wird ein **Table Scan** durchgeführt (alle Zeilen gelesen), mit Index ein effizienter **Key Lookup**.

---

## 🧪 Weitere Tests

### Negativ- und Grenztests

```sql
-- NOT NULL Test: NULL in Pflichtfeld → Fehler erwartet
INSERT INTO Person VALUES (999999, 'Max', 'Muster', NULL, 1);

-- Feldlänge überschreiten → Fehler erwartet
INSERT INTO Adresse VALUES (999999, 'Test', '1a', '12345678901', 'Zürich', 'ZH');
```

### Transaktionstest (ROLLBACK)

```sql
START TRANSACTION;
UPDATE Person SET Nachname = 'Geändert' WHERE Id = 1;
SELECT * FROM Person WHERE Id = 1;  -- Sieht 'Geändert'
ROLLBACK;
SELECT * FROM Person WHERE Id = 1;  -- Alter Wert wieder da
```

### Backup- und Restore-Test

```cmd
mysqldump -u root -p myTestDb > myTestDb_backup.sql
-- Datenbank löschen (Ausfall simulieren):
DROP DATABASE myTestDb;
-- Wiederherstellen:
mysql -u root -p < myTestDb_backup.sql
-- Prüfen: SELECT COUNT(*) → alle 400'000 Datensätze vorhanden
```

### Nebenläufigkeit und Locking

Zwei Sessions ändern gleichzeitig denselben Datensatz:
- **Session 1** startet Transaktion und ändert Person Id=1, kein COMMIT
- **Session 2** versucht ebenfalls Person Id=1 zu ändern → wird **blockiert** (Lock)
- Nach COMMIT/ROLLBACK von Session 1 wird Session 2 freigegeben

---

## 📊 Benchmark mit mysqlslap

```powershell
cd C:\xampp\mysql\bin
.\mysqlslap.exe --user=root --password `
  --concurrency=30 --iterations=5 --number-of-queries=3000 `
  --query="SELECT * FROM Orders WHERE Freight > 100 ORDER BY Freight DESC;" `
  --create-schema=northwind
```

**Optimierungspotenzial messen** durch Anpassen der `my.ini`:

| Parameter | Empfehlung | Effekt |
|-----------|-----------|--------|
| `innodb_buffer_pool_size` | 512M–1G | Mehr Daten im RAM statt auf Disk |
| `innodb_log_file_size` | 128M | Weniger Schreiblast bei vielen Transaktionen |
| `max_connections` | > 30 | Vermeidet "Too many connections"-Fehler |

---

## 💡 Schlussbilanz

Die wichtigsten Erkenntnisse aus dem Testprotokoll:

| Erkenntnis | Details |
|-----------|---------|
| **Indizes sind entscheidend** | 60× schnellere Abfragen mit korrekten Indizes auf PK und FK |
| **Datenbereinigung vor PK** | Duplikate müssen entfernt werden, bevor ein PRIMARY KEY gesetzt werden kann |
| **RBAC funktioniert** | Rollen ermöglichen saubere Berechtigungsverwaltung |
| **Checkliste/Drehbuch** | Bei einer Migration ist ein strukturiertes Vorgehen mit Testprotokoll entscheidend |
| **Backup prüfen** | Ein Backup ist nur nützlich, wenn das Restore auch funktioniert |

---

## ✅ Checkpoint

Die Aufgaben sind gelöst unter: [Checkpoint 7. Tag](./Checkpoint.md)

- ✅ Test-User mit Rollen erstellt und Berechtigungen geprüft
- ✅ 400'000 Datensätze per Bulk-Import geladen
- ✅ Datenintegrität geprüft (Duplikate, PK, FK)
- ✅ Performance ohne/mit Index verglichen (9.5s → 0.16s)
- ✅ Benchmark mit `mysqlslap` durchgeführt

---

[⬅️ 6. Tag](../6.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [8. Tag ➡️](../8.Tag/README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

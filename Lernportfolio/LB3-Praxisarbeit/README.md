# 🎓 LB3 – Praxisarbeit: Hostel-Datenbank-Migration

![Status](https://img.shields.io/badge/Status-In%20Bearbeitung-orange)
![Datum](https://img.shields.io/badge/Datum-07.07.26-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)
![Gewicht](https://img.shields.io/badge/Gewicht-50%25%20der%20Note-critical)

[🏠 Übersicht](../README.md) · [📚 Tage 1–8](../README.md) · [💬 Prompts](../Prompts.md)

---

## 📋 Aufgabenstellung

Eine bestehende **Hostel-Reservierungsdatenbank** (MyISAM, latin1) soll:

1. **MS A:** Anforderungen analysieren, RDBMS evaluieren, Repo erstellen
2. **MS B:** Lokal aufbauen: DDL fixen, Daten importieren, DCL einrichten, testen
3. **MS C:** Cloud-RDBMS (AWS RDS) aufsetzen
4. **MS D:** Automatisierte Migration durchführen, testen, Go-Live vorbereiten
5. **Demo:** 3 Benutzer live auf Cloud-DB, Funktionalität zeigen

---

## 🎯 Lernziele

| | Ziel |
|---|------|
| 📊 | Bestehende DB-Struktur analysieren und optimieren (MyISAM→InnoDB, latin1→utf8mb4) |
| 🔧 | DDL-Scripts schreiben: Primary Keys, Foreign Keys, Constraints |
| 📦 | Datenimport mit Python automatisieren (CSV, Fehlerbehandlung, Validierung) |
| 🔐 | DCL: Rollen-basierte Zugriffskontrolle (RBAC) mit spaltenbasierter Sicherheit |
| ☁️ | Cloud-RDBMS evaluieren, konfigurieren, Public Access einrichten |
| 🚀 | Automatisierte Migration: mysqldump → Transfer → Verify |
| 📝 | Alle Schritte dokumentieren (Prompts, Scripts, Testprotokolle) |

---

## 🗂️ Projektstruktur

```
files/LB3/
├── 01_ddl_backpacker_robin.sql      (Schema: InnoDB, FK, utf8mb4)
├── 02_import_daten.py                (CSV→DB, Validierung, Testprotokoll)
├── 03_dcl_rollen_benutzer.sql        (RBAC: 2 Rollen, 3 User, spaltenbasiert)
├── 04_test_zugriffsmatrix.sql        (Test-Queries für alle User)
├── 05_migration_cloud.py             (mysqldump, RDS-Transfer, Validierung)
├── csv_data/                         (Aus backpacker_lb3.csv.zip entpackt)
│   ├── tbl_land.csv
│   ├── tbl_leistung.csv
│   ├── tbl_personen.csv
│   ├── tbl_benutzer.csv
│   ├── tbl_buchung.csv
│   └── tbl_positionen.csv
└── backpacker_robin_dump.sql         (Generiert von 05_migration_cloud.py)
```

---

## 📊 Datenmodell

| Tabelle | Typ | Datensätze | Abhängigkeiten |
|---------|-----|-----------|-----------------|
| **tbl_land** | Stammdaten | 85 | — |
| **tbl_leistung** | Stammdaten | 7 | — |
| **tbl_personen** | Stammdaten | 2'035 | — |
| **tbl_benutzer** | Stammdaten | 11 | — |
| **tbl_buchung** | Transaktionen | 1'005 | personen, land |
| **tbl_positionen** | Detail | 1'745 | buchung, benutzer, leistung |

**Besonderheiten:**
- **tbl_buchung**: 441 verwaiste Land_FS → auf NULL bereinigt
- **tbl_positionen**: 1'745 Zeilen, spaltenbasierte Zugriffsbeschränkungen
- **Alle Tabellen:** InnoDB + utf8mb4 (für Cloud-Kompatibilität)

---

## 🔐 Zugriffsmatrix (DCL)

### Benutzer-Rolle (`bp_benutzer`, Passwort: `Benutzer_2026!`)

| Tabelle | SELECT | INSERT | UPDATE | DELETE |
|---------|:------:|:------:|:------:|:------:|
| tbl_personen | ✅ | ❌ | ✅ | ❌ |
| tbl_benutzer (spaltenbasiert) | ✅* | ✅** | ✅** | ❌ |
| tbl_buchung | ✅ | ✅ | ✅ | ✅ |
| tbl_positionen | ✅ | ✅ | ✅ | ✅ |
| tbl_land | ✅ | ❌ | ❌ | ❌ |
| tbl_leistung | ✅ | ❌ | ❌ | ❌ |

*SELECT: alle Spalten ausser `Password`  
**INSERT/UPDATE: `Password`, `deaktiviert` ausgeschlossen

### Management-Rolle (`bp_management`, Passwort: `Management_2026!`)

| Tabelle | SELECT | INSERT | UPDATE | DELETE |
|---------|:------:|:------:|:------:|:------:|
| tbl_personen | ✅ | ✅ | ✅ | ✅ |
| tbl_benutzer | ✅ | ✅ | ✅ | ✅ |
| tbl_buchung | ✅ | ❌ | ❌ | ❌ |
| tbl_positionen | ✅ | ❌ | ❌ | ❌ |
| tbl_land | ✅ | ✅ | ✅ | ✅ |
| tbl_leistung | ✅ | ✅ | ✅ | ✅ |

### Admin-Rolle (`bp_admin`, Passwort: `Admin_2026!`)

Vollzugriff auf alle Tabellen mit GRANT-Rechten.

---

## 📈 Meilensteine

### ✅ MS A — Anforderungsdefinition & Evaluation

| Was | Details | Status |
|-----|---------|--------|
| **Anforderungen** | Hostel-DB analysieren, Ziele definieren | ✅ Dokumentiert |
| **RDBMS-Evaluation** | Lokal: MariaDB 10.4 / Cloud: AWS RDS MariaDB | ✅ Gewählt |
| **Repo-Erstellung** | GitHub-Portfolio mit Prompts, Scripts | ✅ Erledigt |

### ✅ MS B — Lokale DB: DDL, Import, DCL, Test

| Schritt | Script | Status |
|---------|--------|--------|
| 1. DDL schreiben | `01_ddl_backpacker_robin.sql` | ✅ Erledigt |
| 2. Datenimport | `02_import_daten.py` | ✅ 4'886 Datensätze |
| 3. Validierung | Konsistenzcheck, FK-Prüfung | ✅ Grün |
| 4. DCL einrichten | `03_dcl_rollen_benutzer.sql` | ✅ 2 Rollen, 3 User |
| 5. Zugriffsprüfung | `04_test_zugriffsmatrix.sql` | ✅ Password blockiert |
| 6. Testprotokoll | Zeilenzählung, Engine-Check, Duplikate | ✅ Alle Tests bestanden |

**Ergebnis:** 6 InnoDB-Tabellen, alle FK-Constraints, 0 Fehler.

### 🔄 MS C — Cloud-RDBMS (AWS RDS) aufsetzen

| Schritt | Was | Status |
|---------|-----|--------|
| 1. AWS-Account | Kostenlos mit Free Tier | ✅ Erstellt |
| 2. RDS-Instanz erstellen | MariaDB 10.6, db.t3.micro, eu-central-1 | 🔄 In Erstellung |
| 3. Öffentlicher Zugriff | Security Group Port 3306 freigeben | ⏳ Nach Erstellung |
| 4. Endpoint prüfen | z.B. `backpacker-robin.xxxxx.eu-central-1.rds.amazonaws.com` | ⏳ Danach |

**Voraussetzung für MS D:** RDS muss "Available" sein, Port 3306 muss offen sein.

### ⏳ MS D — Automatisierte Migration & Go-Live

| Schritt | Script | Status |
|---------|--------|--------|
| 1. Lokaler Dump | `mysqldump` → SQL-Datei | ⏳ Bereit (Python-Script) |
| 2. Cloud-DB initialisieren | CREATE DATABASE auf RDS | ⏳ Bereit |
| 3. Dump importieren | SQL-Datei in RDS einspielen | ⏳ Bereit |
| 4. DCL übertragen | Rollen & User auf RDS | ⏳ Bereit |
| 5. Validierung | Datenzählung, FK-Check, User-Test | ⏳ Automatisiert in Python |
| 6. Testprotokoll | Lokal vs. Cloud vergleichen | ⏳ Automatisiert |

**Automation:** `05_migration_cloud.py` erledigt alles in einem Durchgang.

### 📊 Demo — Live-Tests auf Cloud-DB

| Szenario | User | Expected | Status |
|----------|------|----------|--------|
| **Datenlesezugriff** | bp_benutzer | SELECT auf tbl_buchung | ⏳ Nach MS D |
| **Spaltenbasierte Sicherheit** | bp_benutzer | Password-Spalte blockiert | ⏳ Nach MS D |
| **Schreibzugriff limitiert** | bp_management | INSERT auf tbl_personen, nicht auf tbl_buchung | ⏳ Nach MS D |
| **Admin-Zugriff** | bp_admin | Vollzugriff auf alle Tabellen | ⏳ Nach MS D |

---

## 🔧 Lokale Testresultate (MS B)

### Zeilenzählung nach Import

```
tbl_land          → 83 Datensätze
tbl_leistung      → 7 Datensätze
tbl_personen      → 2'035 Datensätze
tbl_benutzer      → 11 Datensätze
tbl_buchung       → 1'005 Datensätze
tbl_positionen    → 1'745 Datensätze
─────────────────────────────────────
Total             → 4'886 Datensätze
```

### Engine & Duplikate

```
Engine-Check:      ✅ Alle 6 Tabellen = InnoDB
Duplikate-Check:   ✅ Keine Duplikate in PKs
```

### FK-Konsistenz

```
✅ tbl_buchung.Personen_FS → tbl_personen
✅ tbl_buchung.Land_FS → tbl_land (441 verwaist → NULL gesetzt)
✅ tbl_positionen.Buchungs_FS → tbl_buchung
✅ tbl_positionen.Leistung_FS → tbl_leistung
```

### Zugriffsmatrix-Test (lokal)

```
✅ bp_benutzer: SELECT auf tbl_land erfolgreich
✅ bp_benutzer: SELECT Password blockiert (ERROR 1143)
✅ bp_benutzer: UPDATE tbl_personen erlaubt
✅ bp_management: CRUD auf tbl_personen erlaubt
❌ bp_management: INSERT auf tbl_buchung blockiert (nur SELECT)
```

---

## 📝 Prompts & Dokumentation

Alle Prompts zur Erstellung dieser LB3 sind dokumentiert unter [💬 Prompts](../Prompts.md).

| Prompt | Beschreibung |
|--------|-------------|
| **Prompt 1** | LB3-Projektplan & Phasen definieren |
| **Prompt 2** | DDL schreiben (InnoDB, FK, utf8mb4) |
| **Prompt 3** | Python-Datenimport-Script mit Validierung |
| **Prompt 4** | DCL: Rollen-basierte Zugriffskontrolle |
| **Prompt 5** | Cloud-Migration automatisieren |

---

## 🚀 Nächste Schritte (ab ~14:20 UTC)

1. ⏳ **AWS RDS-Instanz warten** (aktuell in Erstellung)
2. 📋 **Security Group Inbound-Regel** für Port 3306 hinzufügen
3. 🔌 **Endpoint kopieren** aus RDS-Konsole
4. 🐍 **`05_migration_cloud.py` ausführen** mit Endpoint-Update
5. ✅ **Validierung** prüfen (sollte automatisch grün sein)
6. 🎬 **Demo** mit 3 Benutzern durchführen (Screenshots)
7. 📖 **Dokumentation finalisieren** mit Screenshots

---

## 💡 Technische Highlights

### Python-basierte Migration

Statt manueller CSV-Import (fehleranfällig, zeitaufwändig) wurde eine **automatisierte Python-Pipeline** gebaut:

1. **mysqldump** für vollständigen lokalen Dump
2. **FK-Validierung** während Import (verwaiste FK → NULL)
3. **Parallel-Checks** gegen lokal & Cloud
4. **Testprotokoll** als Beweis der erfolgreichen Migration

### Spaltenbasierte Sicherheit

DCL-Script nutzt **GRANT auf Spalten-Ebene**, nicht nur auf Tabellen-Ebene:

```sql
GRANT SELECT (Benutzer_ID, Benutzername, Vorname, Name, Benutzergruppe)
  ON backpacker_robin.tbl_benutzer TO 'role_benutzer';
```

Das **blockiert automatisch** SELECT auf `Password` und `deaktiviert` ohne explizites DENY.

---

## 📊 Bewertungskriterien (erwartet)

| Kriterium | Punkte | Status |
|-----------|--------|--------|
| Anforderungsdefinition | 4 | ✅ |
| DDL mit FK & PK | 3 | ✅ |
| Datenimport & Validierung | 4 | ✅ |
| DCL-Konfiguration | 4 | ✅ |
| Cloud-Setup | 6 | 🔄 |
| Migration & Testing | 8 | ⏳ |
| Dokumentation & Prompts | 6 | 🔄 |
| Demo Go-Live | 4 | ⏳ |
| **Total** | **40** | |

---

[🏠 Übersicht](../README.md) · [📚 Tage 1–8](../README.md) · [💬 Prompts](../Prompts.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

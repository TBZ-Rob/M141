# 🗄️ Tag 2 – Konfiguration & Datenimport

![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)
![Datum](https://img.shields.io/badge/Datum-19.05.2025-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

> 💬 **Claude Prompt für dieses File:**
> *„Analysiere das ganze Repo, aktualisiere jedes Diagramm oder Darstellung auf den neusten Stand und füge bei neuen Seiten hinzu."*

---

### 🔧 Durchgeführte Schritte

- `my.ini` mit `mysqld --verbose --help` untersucht
- Datenbank `firma` mit Kollation `utf8mb4_unicode_ci` angelegt
- `tbl_plz_ort.sql` importiert, Index `plz_ort_ID` gelöscht, Tabellentyp MyISAM → InnoDB
- `tbl_mitarbeiter.sql` importiert und Tabellenstruktur mit `DESCRIBE` / `SHOW CREATE TABLE` untersucht
- Eigene Tabelle `personen` erstellt und Daten via `LOAD DATA INFILE` geladen
- Tabelle `kunden` erstellt und Daten via JSON importiert
- Dump der Datenbank `firma` mit `mysqldump` erstellt

---

### 💡 Erkenntnisse

Da ich längere Zeit kein SQL mehr geschrieben hatte, musste ich mich erst wieder ins Thema einarbeiten und einzelne Befehle nachschlagen. Trotzdem verlief alles reibungslos.

**Probleme & Lösungen:**

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `ALTER TABLE` für `FS_Wohnort` schlug fehl | Spalte war bereits im importierten SQL-Script enthalten | Schritt übersprungen |
| `JSON_TABLE` Syntax-Fehler | Funktion erst ab MariaDB 10.6 verfügbar, installiert ist 10.4.32 | Daten direkt via `INSERT INTO VALUES` eingefügt |

---

### 📸 Screenshots

**my.ini untersuchen:**
![my.ini](./screenshots/myini-untersuchen.png)

**DESCRIBE tbl_mitarbeiter:**
![DESCRIBE](./screenshots/2t_describe_tbl_mitarbeiter.png)

**SHOW CREATE TABLE:**
![SHOW CREATE TABLE](./screenshots/2t_show_create_table_mitarbeiter.png)

**LOAD DATA INFILE:**
![LOAD DATA INFILE](./screenshots/2t_load_data_infile_personen.png)

**JSON Import:**
![JSON Import](./screenshots/2t_json_import_kunden.png)

---

### 🔗 Weitere Seiten

- [✅ Checkpoint](./Checkpoint.md)
- [📋 Repetition SQL](./Repetition_SQL.md)
- [📋 Repetition Kap. 2 & 3](./Repetition_Kap2_3.md)

---

### ✅ [Checkpoint](./Checkpoint.md)

| Ziel | Status |
|------|--------|
| my.ini untersucht | ✅ |
| Datenbank `firma` angelegt | ✅ |
| SQL-Dump importiert | ✅ |
| Index gelöscht, InnoDB gesetzt | ✅ |
| Tabellenstruktur untersucht | ✅ |
| LOAD DATA INFILE ausgeführt | ✅ |
| JSON Import durchgeführt | ✅ |
| Dump erstellt | ✅ |

---

| [🏠 Übersicht](../README.md) | [⬅️ Tag 1](../1.Tag/README.md) | [➡️ Tag 3](../3.Tag/README.md) |
|---|---|---|

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

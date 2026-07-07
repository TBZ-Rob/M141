# ✅ Checkpoint – 2. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-2-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 2](./README.md) · [🏠 Übersicht](../README.md)

Konfiguration & Datenimport — Lösungen zum Checkpoint.

---

## 🔘 Multiple Choice – my.ini Konfiguration

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Wo befindet sich die MySQL-Konfigurationsdatei? | `C:\xampp\mysql\bin\my.ini` oder `my.cnf` auf Linux |
| 2 | Welcher Parameter stellt den Port ein? | `port=3306` im Bereich `[mysqld]` |
| 3 | Was ist der Standard-Datenverzeichnis-Pfad? | `datadir=C:/xampp/mysql/data` |
| 4 | Welcher Parameter setzt den Zeichensatz? | `character_set_server=utf8mb4` |
| 5 | Wie werden Änderungen in my.ini wirksam? | Nach Neustart des MySQL-Servers |

---

## ✏️ Offene Fragen – Datenimport

**1. Beschreiben Sie 3 verschiedene Methoden zum Datenimport in MySQL:**

- **CSV-Import**: `LOAD DATA INFILE 'datei.csv' INTO TABLE tabelle`
- **SQL-Dump**: `mysql -u root -p datenbank < dump.sql`
- **PHP/GUI**: Mit phpMyAdmin oder Workbench hochladen

**2. Welche Vorteile hat der Datenimport per SQL-Dump?**

- Struktur UND Daten werden zusammen importiert
- Einfaches Backup/Restore
- Portabel zwischen verschiedenen Systemen
- Revisionierbar (Text-Format)

**3. Was muss beim CSV-Import beachtet werden?**

- Delimiter (`,` oder `;`)
- Zeichencodierung (UTF-8, Latin1)
- Spaltenreihenfolge muss stimmen
- Fehlende oder zu viele Werte führen zu Fehlern

**4. Wie prüft man den Erfolg eines Imports?**

```sql
SELECT COUNT(*) FROM importierte_tabelle;
SELECT * FROM importierte_tabelle LIMIT 5;
```

**5. Was ist die Collation und warum ist sie wichtig?**

Die Collation definiert Sortierregeln und Zeichenvergleiche. Wichtig für: Suchvorgänge, Sortierung, Eindeutigkeit von Feldern.

---

## 🛠️ Praktische Aufgaben

### Aufgabe 1: my.ini modifizieren

- [ ] my.ini in Texteditor öffnen
- [ ] Port von 3306 zu 3307 ändern
- [ ] MySQL neu starten
- [ ] Mit `mysql -P 3307` verbinden

### Aufgabe 2: CSV importieren

- [ ] CSV-Datei vorbereiten (mit Header-Zeile)
- [ ] Tabelle mit passenden Spalten erstellen
- [ ] `LOAD DATA INFILE` ausführen
- [ ] Daten mit SELECT prüfen

### Aufgabe 3: SQL-Dump erstellen und einlesen

- [ ] `mysqldump -u root -p testdb > backup.sql`
- [ ] Dump-Datei in phpMyAdmin/Workbench einlesen
- [ ] Datensätze zählen (sollte gleich sein)

---

[⬅️ Tag 2](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

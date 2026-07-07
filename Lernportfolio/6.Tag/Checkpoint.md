# ✅ Checkpoint – 6. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-6-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 6](./README.md) · [🏠 Übersicht](../README.md)

Lösungen zum Checkpoint **Server-Administration: Konfiguration, Logging, Backup/Recovery und Optimierung**.

---

## 🔘 Multiple Choice – Server konfigurieren

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Auf welche Arten können Konfigurationsparameter definiert werden? | ✅ Durch Eintrag auf der **Kommandozeile** · ✅ Durch Eintrag in einer **Konfigurationsdatei** |
| 2 | Welcher Parameter legt fest, wo die Log-Dateien abgelegt werden? | ✅ `basedir` · ✅ `datadir` · ✅ `log-bin` |
| 3 | Mit welchem Eintrag beginnen die Server-Parameter in der Konfigurationsdatei? | ✅ `[mysqld]` |
| 4 | Wozu kann der DB-Client `mysqlshow` verwendet werden? | ✅ **DB-Schema anzeigen** |
| 5 | Mit welchem Log-File bestimmen Sie den letzten Start des MySQL-Servers? | ✅ **Error Log** |
| 6 | Welcher Eintrag schaltet die Protokollierung aller User-Login ein? | ✅ `log` (General Query Log) |
| 7 | Wie restaurieren Sie nach einem Server-Ausfall eine DB vollständig? | ✅ Einlesen des letzten **Backup** · ✅ Einlesen aller **Update-Logs** in der richtigen Reihenfolge (mit `mysqlbinlog`) |

---

## ✏️ Offene Fragen – Server konfigurieren

**8. Wie erreichen Sie, dass Änderungen in der Konfigurationsdatei wirksam werden?**

Konfigurationsdatei abspeichern und den Server (`mysqld.exe`) **neu starten**. Änderungen in der `my.ini` werden erst beim Neustart eingelesen.

**9. Durch welche Daten wird der von einer DB benötigte Speicherplatz bestimmt?**

Drei Komponenten: **Nutzdaten** (die eigentlichen Datensätze), **Indizes** (Hilfstabellen für schnellen Zugriff) und **Systemdaten** (DB- und Tabellenbeschreibungen, Systemkatalog, User-Verwaltung).

**10. Wozu wird das Logging (Protokollierung) verwendet?**

Fünf Hauptzwecke: **Monitoring** (Fehler, Start/Stop), **Sicherheit** (Backup/Recovery), **Optimierung** (langsame Abfragen finden), **Replikation** (Synchronisierung mehrerer Server) und **Transaktionen** (Wiederherstellung nach DB-Absturz).

**11. In welcher Log-Datei finden Sie den Anwender, der bestimmte Daten löschte?**

Im **General Query Log** – dieses zeichnet jeden User und dessen Aktivitäten (alle SQL-Befehle) auf.

**12. Welche Informationen finden Sie im Slow Query Log?**

DB-Abfragen, die den grössten Aufwand verursachen (länger als der konfigurierte Schwellenwert). Die Analyse gibt direkte Hinweise zur Verbesserung der **Server-Performance** (z.B. fehlende Indizes).

**13. Geben Sie für jede Protokolldatei an, wie Sie deren Inhalt kontrollieren.**

- **Error Log, Query Log, Slow Query Log:** Mit einem **Texteditor** öffnen (Klartextdateien)
- **Binary Log (Update Log):** Mit dem Tool `mysqlbinlog.exe` anzeigen (binär codiert)
- **Transaction Logs:** Nur für den Server selbst relevant, nicht manuell auswertbar

**14. Wie beeinflusst der Parameter `--opt` beim Erstellen eines Backup das Tabellenlocking?**

`--opt` enthält u.a. `--lock-tables` und `--add-locks`. Die Tabellen werden beim Backup fürs Lesen gesperrt (READ LOCK) und die INSERT-Befehle im Backup-Script werden mit LOCK/UNLOCK-Befehlen umschlossen für schnelleres Einlesen.

**15. Beschreiben Sie das Vorgehen, um Daten von MySQL nach ORACLE zu migrieren.**

Tabellen aus MySQL exportieren mit `SELECT * INTO OUTFILE` oder `mysqldump` und in Oracle importieren. Dabei auf **Delimiter**, **Datumsformate** und **Kollation** (Zeichenformate/Encoding) achten.

**16. Beschreiben Sie eine praktische Anwendung für den READ-Lock.**

Der READ-Lock gewährleistet die **Integrität der Datenbank beim Erstellen eines Backups** – während des Dumps dürfen keine Daten verändert werden, sonst wäre das Backup inkonsistent.

---

## 🔘 Multiple Choice – Optimierung

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Welche Möglichkeiten verbessern die Geschwindigkeit eines DB-Servers? | ✅ **Serverparameter einstellen** · ✅ **Locks verwenden** |
| 2 | Wie werden Daten schneller in eine DB-Tabelle geladen? | ✅ Durch Verwenden des Parameters `--opt` · ✅ Durch **Importieren** der Daten aus einer Textdatei |
| 3 | Was trifft auf `OPTIMIZE TABLE` zu? | ✅ Entfernt nicht genutzten Speicherplatz aus MyISAM-Tabellendateien · ✅ Wird angewendet bei Tabellen mit häufigen Mutationen · ✅ Defragmentiert DB-Dateien |
| 4 | Wie finden Sie langsame DB-Abfragen? | ✅ Mit **EXPLAIN SELECT** · ✅ Im **Slow Query Log** |
| 5 | Welche Aussagen betreffend DB-Optimierung sind korrekt? | ✅ Indexe **beschleunigen** Abfragen · ✅ Indexe werden allgemein auf **Schlüsselattribute** gelegt |
| 6 | Wann verwenden Sie den Befehl EXPLAIN? | ✅ Um **langsame Abfragen** zu finden · ✅ Um zu erkennen, wie sich ein **Index** auf die Geschwindigkeit auswirkt |
| 7 | Welches sind Gründe für die Verwendung eines Index? | ✅ Um DB-Abfragen zu **beschleunigen** · ✅ Um **einmalige Werte** zu gewährleisten (UNIQUE) · ✅ Um das Eintragen bei Unique-Attributen zu beschleunigen |

---

## ✏️ Offene Fragen – Optimierung

**8. Nennen Sie Ziele der DB-Optimierung?**

Drei Ziele: **Performance verbessern** (schnellere SQL-Ausführung), **Speicherplatz einsparen** (schnellere Übertragung) und **Portabilität ermöglichen** (Übertragen auf anderen Server).

**9. Was wird optimiert, um die Geschwindigkeit eines DB-Servers zu verbessern?**

Such-, Schreib- und Lesevorgänge: Daten auf mehrere Festplatten verteilen, SQL-Scripts optimieren, Speicherplatz bereinigen, Indizes setzen.

**10. Mit welchen 2 prinzipiellen Massnahmen werden DB-Abfragen beschleunigt?**

1. **`--opt` und `LOAD DATA INFILE`**: Schnelleres Ausführen von SQL-Scripts
2. **`OPTIMIZE TABLE` und Indizes**: Entfernt ungenutzten Speicherplatz und beschleunigt Suchvorgänge

**11. Beschreiben Sie kurz, wie Sie den Befehl EXPLAIN verwenden.**

`EXPLAIN` wird einem `SELECT`-Statement vorangestellt. Es erklärt, wie MySQL die Abfrage ausführen würde: welche Tabellen in welcher Reihenfolge verknüpft werden, welche Indizes genutzt werden und wie viele Zeilen untersucht werden müssen. So erkennt man, wo Indizes fehlen.

**12. Wozu wird der Befehl `OPTIMIZE TABLE` angewendet?**

Entfernt nicht genutzten Speicherplatz, der durch DELETE- und UPDATE-Operationen entstanden ist, und defragmentiert die Tabellendatei für schnelleren Zugriff.

**13. Wie werden SELECT-Befehle optimiert?**

Indem Indizes auf häufig verwendete Attribute und auf Schlüssel (PK, FK) erstellt werden. Mit `EXPLAIN` prüfen, ob Indizes genutzt werden.

**14. Wie viele DB-Tabellen können standardmässig gleichzeitig geöffnet sein?**

`table_cache = 64` (Standard). Kann in der `my.ini` erhöht werden.

**15. Wie schalten Sie den Query Cache ein bzw. aus?**

In der Konfigurationsdatei: `query_cache_size = 32M` und `query_cache_type = 1` (ein) bzw. `query_cache_type = 0` (aus). Zur Laufzeit: `SET query_cache_type = 0;`

**16. CLI-Tools im Verzeichnis `mysql\bin`**

| Tool | Beschreibung |
|------|-------------|
| `mysql.exe` | DB-Befehlszeilenclient – SQL-Anfragen interaktiv oder per Script ausführen |
| `mysqladmin.exe` | Administrationstool – Prozessliste, Statistiken, DBs erstellen/löschen, Flush, Shutdown |
| `mysqlbinlog.exe` | Binärlog-Dateien in Klartext anzeigen |
| `mysqlcheck.exe` | Tabellen prüfen, reparieren, analysieren und optimieren |
| `mysqld.exe` | Der MariaDB-Server selbst (Daemon) |
| `mysqldump.exe` | Backup-Programm für Datenbanken |
| `mysqlimport.exe` | Tabellen aus Textdateien laden |
| `mysqlshow.exe` | Datenbanken, Tabellen, Spalten und Indizes anzeigen |
| `mysqlslap.exe` | Benchmark-Tool – simuliert Client-Last und misst Performance |
| `mysql_install_db.exe` | Initialisiert das Datenverzeichnis und erstellt Systemtabellen |
| `mysql_plugin.exe` | Plugins aktivieren oder deaktivieren |
| `mariabackup.exe` | Physische Online-Backups für InnoDB, Aria und MyISAM |

---

[⬅️ Tag 6](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

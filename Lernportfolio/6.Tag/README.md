# 6. Tag – Server-Administration

![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)
![Datum](https://img.shields.io/badge/Datum-16.06.26-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ 5. Tag](../5.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [7. Tag ➡️](../7.Tag/README.md)

Ein DB-Server im Produktivbetrieb erfordert mehr als eine Standardinstallation. Dieser Tag behandelt die vier zusammenhängenden Phasen für einen zuverlässigen, sicheren und performanten Betrieb: Konfiguration → Überwachung → Sicherung → Optimierung.

## 🎯 Lernziele

| | Lernziel |
|---|----------|
| ⚙️ | Server-Konfiguration über `my.ini`, Kommandozeile und Systemvariablen verstehen |
| 📋 | Logging-Typen kennen (Error, Binary, General Query, Slow Query, Transaction) |
| 💾 | Backup & Recovery mit `mysqldump` und Binary Logs durchführen |
| 🚀 | Optimierungsmöglichkeiten: Indizes, EXPLAIN, Query Cache, Server-Tuning |

---

## ⚙️ 1. Konfiguration

**Was:** Die Konfiguration bildet die Basis – hier wird eingestellt, wie der Server arbeitet, welche Logs geschrieben werden und wie viel Arbeitsspeicher zur Verfügung steht.

Der DB-Server kann auf **drei Arten** konfiguriert werden:

| Art | Beschreibung | Beispiel |
|-----|-------------|---------|
| **Konfigurationsdatei** | Parameter in `my.ini` / `my.cnf` eintragen | `[mysqld]` → `language=german` |
| **Kommandozeile** | Beim Start des Servers Optionen mitgeben | `mysqld --language=german` |
| **Systemvariablen** | Zur Laufzeit abfragen/ändern | `SHOW VARIABLES LIKE '%log%';` |

Es gilt: Werte auf der Kommandozeile haben **Vorrang** vor Einträgen in Konfigurationsdateien. Änderungen in `my.ini` werden erst nach einem **Neustart** wirksam.

**Konfiguration vorab prüfen:**

```sql
-- Syntax-Check vor Neustart (verhindert Startfehler)
mysqld.exe --validate-config
```

> ⚠️ Ein Tippfehler in der `my.ini` (z.B. `-` statt `_`) kann dazu führen, dass der Server nicht mehr startet.

**Client-Parameter** können ebenfalls in der Konfigurationsdatei hinterlegt werden:

```ini
[mysql]
user=meier
silent
```

---

## 📋 2. Überwachung (Logging)

**Was:** Logging protokolliert, was im System passiert – von Fehlern über Datenänderungen bis hin zu langsamen Abfragen.

**Warum:** Ohne Überwachung ist keine Fehlersuche, kein Recovery und keine Performance-Analyse möglich.

| Ziel | Nutzen |
|------|--------|
| **Monitoring** | Wer hat wann welche Daten verändert? |
| **Sicherheit** | Datenwiederherstellung zwischen Backups |
| **Optimierung** | Aufzeichnung aufwendiger Abfragen |
| **Replikation** | Synchronisierung mehrerer DB-Server |
| **Transaktionen** | Wiederherstellung nach DB-Absturz |

### Log-Typen im Überblick

| Log-Typ | Zweck | Standardmässig aktiv? |
|---------|-------|----------------------|
| **Error Log** | Server-Fehler, Start/Stop | ✅ Immer aktiv (kann nicht deaktiviert werden) |
| **Binary Log** | Alle Datenänderungen (INSERT/UPDATE/DELETE) – für Recovery & Replikation | ❌ Muss aktiviert werden (`log-bin=mysql-bin`) |
| **General Query Log** | Alle Befehle aller Clients | ❌ Nur für Debugging (wird sehr gross!) |
| **Slow Query Log** | Langsame Abfragen | ❌ Für Optimierung wichtig |
| **Transaction Log** | InnoDB-Transaktionen | ✅ Automatisch (für Crash-Recovery) |

> ⚠️ In der **Standardeinstellung** sind ausser dem Error Log alle Protokolle ausgeschaltet, da Logging den Server verlangsamt und Speicherplatz verbraucht.

### Error Log

Protokolliert jeden Start, Shutdown und alle Fehlermeldungen des Servers in Textform.

```ini
# Error Log-Datei festlegen (in my.ini)
log-error=C:/log/mysql_error.log
```

### Binary Log (Update Log)

Essentiell für **Backup & Recovery**. Zeichnet alle datenverändernden Befehle auf. Eine neue Log-Datei wird erstellt bei: Neustart, Erreichen der Maximalgrösse, oder `FLUSH LOGS`.

```ini
# Binary Logging aktivieren (in my.ini)
log-bin=mysql-bin
```

Binär-Logs lesen:

```cmd
mysqlbinlog C:\...\mysql\data\mysql-bin.000001
```

### Slow Query Log

Zeichnet Abfragen auf, die den grössten Aufwand verursachen – direkter Startpunkt für die **Optimierung**.

> 💡 Für maximale Geschwindigkeit und Sicherheit sollten Log-Dateien auf einer **anderen Festplatte** als die DB-Dateien liegen.

---

## 💾 3. Sicherung (Backup & Recovery)

**Was:** Regelmässige Backups schützen vor Datenverlust. Das Binary Log schliesst die Lücke zwischen dem letzten Backup und dem Crash-Zeitpunkt.

### Backup mit mysqldump

```cmd
mysqldump --user=root --password=pwd --opt firma > backup.sql
```

**Wichtige Optionen:**

| Option | Beschreibung |
|--------|-------------|
| `--opt` | Optimale Einstellung (fasst mehrere Optionen zusammen) |
| `--lock-tables` | READ LOCK für Datenintegrität während des Backups |
| `--single-transaction` | Konsistenter Snapshot (nur bei transaktionsfähigen Tabellen) |
| `--add-locks` | LOCK/UNLOCK um INSERT-Befehle für schnelleres Einlesen |
| `-F, --flush-logs` | Logs vor dem Dump auf Disk schreiben (sauberer Schnittpunkt) |
| `--compact` | Weniger Ausgabetext |

### Restore (Wiederherstellung)

**Schritt 1:** Letztes Backup einlesen:

```cmd
mysql -u root -p firma < backup.sql
```

**Schritt 2:** Binary Logs seit dem letzten Backup einspielen:

```cmd
mysqlbinlog mysql-bin.000001 | mysql -u root -p
mysqlbinlog mysql-bin.000002 | mysql -u root -p
```

> ⚠️ Die älteste Log-Datei wird **zuerst** ausgeführt. Binary Logs dürfen nie mehrfach eingespielt werden, sonst entstehen doppelte Daten.

### Speicherbedarf abschätzen

| Komponente | Formel (MyISAM) |
|-----------|----------------|
| Nutzdaten (`.MYD`) | Anzahl_Datensätze × [SUM(Bytes_pro_Attribut) + 5] |
| Indizes (`.MYI`) | Anzahl_Schlüssel × [(Schlüssellänge + 4) / 0.67] |
| Systemdaten (`.FRM`) | 8500 + (Anzahl_Attribute × 40) |

---

## 🚀 4. Optimierung

**Was:** Mit den Erkenntnissen aus dem Logging (Slow Query Log) und der richtigen Konfiguration (Speicherparameter) wird das System beschleunigt.

| Ziel | Beschreibung |
|------|-------------|
| **Performance** | Schnellere Ausführung von SQL-Befehlen |
| **Speicherplatz** | Schnellere Übertragung von/auf die Festplatte |
| **Portabilität** | Übertragen der DB auf einen anderen Server |

### Tabellenspeicherplatz optimieren

```sql
-- Entfernt ungenutzten Speicherplatz und defragmentiert (nur MyISAM/Aria)
OPTIMIZE TABLE person;
```

### Indizes

Eine Suche ist nur effizient in einem **sortierten Suchraum**. Indizes erstellen sortierte Hilfstabellen für schnelleren Zugriff:

- **Ohne Index:** Lineare/sequentielle Suche → bei N Elementen bis zu N Zugriffe
- **Mit Index:** Binäre Suche → bei N Elementen nur log₂(N) Zugriffe

**Nachteile:** Die Datenbank wird etwas grösser, INSERT/UPDATE-Operationen werden langsamer (Indextabellen müssen aktualisiert werden). In der Praxis ist die Abfragegeschwindigkeit aber wichtiger.

```sql
-- Index erstellen
CREATE INDEX idx_name ON tabelle (spalte);

-- Index löschen
DROP INDEX idx_name ON tabelle;
```

### EXPLAIN – Abfragen analysieren

```sql
EXPLAIN SELECT COUNT(*)
FROM buchung, person
WHERE buchung.PersID = person.PersID;
```

Die `key`-Spalte zeigt den verwendeten Index (NULL = kein Index). Die `rows`-Spalte zeigt die Anzahl zu untersuchender Zeilen. Anhaltspunkt: Alle `rows`-Werte multiplizieren → Ergebnis sollte möglichst klein sein.

| Optimierungstipp | Details |
|-----------------|---------|
| Index auf PK und FK | Beschleunigt JOINs massiv |
| Index auf häufig sortierte Attribute | Verbessert ORDER BY |
| `NOT` und `<>` | Können nicht optimiert werden |
| `LIKE` mit `%` am Anfang | Nicht optimierbar |
| Funktionen in WHERE | Verhindern Index-Nutzung |

### Query Cache

Speichert Ergebnisse von SQL-Abfragen. Bei identischer Abfrage wird das fertige Ergebnis wiederverwendet:

```ini
# Query Cache konfigurieren (in my.ini)
query_cache_size = 32M
query_cache_type = 1
query_cache_limit = 50K
```

### Server-Tuning

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `key_buffer_size` | Für Indizes reservierter Speicher | 8M |
| `table_cache` | Max. Anzahl geöffneter Tabellen | 64 |
| `sort_buffer` | Buffergrösse zum Sortieren/Gruppieren | 2M |
| `read_buffer_size` | Speicher für sequentielles Lesen | 128K |

> 💡 Server-Tuning lohnt sich im Allgemeinen nur bei sehr grossen Datenmengen (GByte) und vielen DB-Zugriffen pro Sekunde.

---

## ✅ Checkpoint

Die Aufgaben sind gelöst unter: [Checkpoint 6. Tag](./Checkpoint.md)

- ✅ Konfigurationsarten verstanden (my.ini, Kommandozeile, Systemvariablen)
- ✅ Logging-Typen und deren Zweck kennen
- ✅ Backup mit `mysqldump` und Recovery mit Binary Logs verstanden
- ✅ Indizes, EXPLAIN und Query Cache angewendet

---

[⬅️ 5. Tag](../5.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [7. Tag ➡️](../7.Tag/README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

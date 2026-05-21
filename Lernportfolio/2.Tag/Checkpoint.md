# ✅ Checkpoint 2. Tag

![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)

---

## DB-Server und XAMPP

**1. Wie kann der MySQL-Server gestartet werden?**
- ❌ Start von `mysql.exe` im CMD-Fenster *(das ist der Client, nicht der Server)*
- ✅ Start von `mysqld.exe` im CMD-Fenster
- ❌ über MySQL-Workbench
- ❌ Eingabe von localhost als URL im Browser
- ✅ `NET START mysql` im CMD-Fenster
- ✅ mit dem Dienstmanager von Windows

**2. Informationen bei `status`-Befehl?**
- ✅ Version des Konsolenprogramms
- ✅ Betriebszeit des Servers
- ✅ Version des Servers
- ❌ Betriebszeit des DB-Klienten mysql

**3. Daten im Verzeichnis datadir?**
- ✅ Protokoll-Dateien (Log-Files)
- ✅ Fehlerprotokolle
- ❌ ausführbare MySQL-Programme *(diese liegen in /bin)*
- ✅ Datenbanken

**4. Wie prüfen ob MySQL-Server läuft?**
- ✅ mit dem Dienst-Manager von Windows
- ❌ mit dem GUI-Tool Administrator
- ❌ durch Eingabe des Befehls `status` im CMD-Fenster *(nur wenn bereits verbunden)*
- ✅ mit dem Task-Manager von Windows (Prozess)

---

**5. Wie testen Sie die Installation?**
Verbindung mit `mysql -u root -p` herstellen – wenn erfolgreich, ist die Installation korrekt.

**6. Wie überprüfen Sie die Laufzeit?**
Mit dem Befehl `status` im mysql-Monitor → zeigt `Uptime` des Servers.

**7. Wozu mysql.exe? Wie starten?**
`mysql.exe` ist der Kommandozeilen-Client für SQL-Befehle.
Start: `mysql -u root -p` im CMD unter `C:\xampp\mysql\bin`

**8. 3 Informationen des status-Befehls:**

| Information | Bedeutung |
|-------------|-----------|
| Server version | Zeigt die installierte MariaDB/MySQL Version |
| Uptime | Wie lange der Server bereits läuft |
| Character set | Aktuelle Zeichencodierung der Verbindung |

**9. 2 wichtige Verzeichnisse:**

| Verzeichnis | Inhalt |
|-------------|--------|
| `C:\xampp\mysql\bin` | Ausführbare Programme (mysql.exe, mysqld.exe, mysqldump.exe) |
| `C:\xampp\mysql\data` | Datenbanken, Log-Dateien, my.ini |

**10. Inhalt der my.ini:**
Konfigurationseinstellungen für Server (`[mysqld]`) und Client (`[client]`), z.B. Port, Zeichensatz, Datenpfade.

---

## Codierung und Kollation

**1. Aussagen zur Codierung:**
- ❌ Datenbankserver erkennt Codierung automatisch
- ✅ Codierung ist eine Vereinbarung zwischen Nutzer und System
- ✅ Legt fest, welche binäre Bitkombination zu welchem Zeichen gehört
- ❌ ANSI und ASCII ist dasselbe *(ANSI ist eine Erweiterung von ASCII)*
- ❌ Unicode hat 32 Bit Codelänge *(UTF-32 hat 32 Bit, Unicode selbst ist variabel)*
- ✅ UTF bedeutet Unicode Transformation Format
- ❌ UTF-8 hat nur 8 Bit *(UTF-8 ist variabel: 1–4 Bytes)*

**2. Aussagen zur Kollation:**
- ❌ utf8_general_cs ist Standard *(Standard ist utf8_general_ci)*
- ✅ DIN-Normierung bietet zwei Varianten zur Umlauthandhabung
- ❌ Endung `_ci` unterscheidet Gross-/Kleinschreibung *(ci = case insensitive = NICHT unterschieden)*
- ✅ Seit MySQL 5.5.3 sollte utf8mb4 verwendet werden
- ✅ In my.ini kann UTF8-Codierung als Standard angegeben werden
- ❌ Kollationseinstellung gilt für ganze Tabelle *(kann auch pro Spalte gesetzt werden)*
- ✅ Binärsortierung = Sortierung anhand des binären Codes

**3. Beobachtung bei DB-Kollation:**
Die importierte Tabelle `tbl_plz_ort` hatte die Kollation `latin1_swedish_ci` – Umlaute wurden falsch dargestellt. Nach Umstellung auf `utf8mb4_unicode_ci` wurden Sonderzeichen (ä, ö, ü, é, à) korrekt angezeigt.

---

## Daten importieren

**Mit welchem Befehl die Tabellenstruktur kontrollieren?**
- ❌ SHOW DATABASES
- ✅ SHOW CREATE TABLE *tabellenname*
- ✅ DESC *tabellenname*
- ✅ DESCRIBE *tabellenname*
- ❌ SELECT * FROM *tabellenname* *(zeigt Daten, nicht Struktur)*
- ❌ SHOW TABLE *tabellenname* *(kein gültiger Befehl)*

---

| [🏠 Übersicht](../../README.md) | [⬅️ Tag 2](../README.md) |
|---|---|

# 5. Tag – Zugriffssystem & Autorisierung

![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)
![Datum](https://img.shields.io/badge/Datum-09.06.26-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ 4. Tag](../4.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [6. Tag ➡️](../6.Tag/README.md)

An Tag 4 wurde die **Authentifizierung** (Wer darf sich verbinden?) behandelt. Heute geht es um die zweite Phase: **Autorisierung** – also was ein Benutzer nach dem Login tun darf. Dazu gehören Privilegien, Geltungsbereiche, Rollen (RBAC) und der Schutz des `pma`-Users.

## 🎯 Lernziele

| | Lernziel |
|---|----------|
| 🔑 | Unterschied Authentifizierung vs. Autorisierung verstehen |
| 📋 | Privilegien (SELECT, INSERT, UPDATE, DELETE, ALL, USAGE) kennen |
| 🌐 | Geltungsbereiche (Global → DB → Tabelle → Spalte) verstehen |
| 🛠️ | GRANT / REVOKE korrekt anwenden |
| 👥 | Rollen (RBAC) erstellen und Benutzern zuweisen |
| 🔒 | pma-User absichern |

---

## 🔐 Authentifizierung vs. Autorisierung

MySQL kontrolliert den Zugang in zwei Phasen:

| Phase | Frage | Zeitpunkt |
|-------|-------|-----------|
| **Authentifizierung** (Tag 4) | Wer darf sich verbinden? | Beim Verbindungsaufbau |
| **Autorisierung** (Tag 5) | Was darf der Benutzer tun? | Bei jedem SQL-Befehl |

Die Autorisierung kann **global** oder **lokal** auf bestimmte Datenbanken, Tabellen und sogar Spalten vergeben werden. Über Views lässt sich der Zugriff sogar auf einzelne Zeilen einschränken.

---

## 📋 Privilegien – „WAS" darf der Benutzer?

| Privileg | Beschreibung |
|:---|:---|
| **SELECT** | Daten lesen |
| **INSERT** | Neue Daten einfügen |
| **UPDATE** | Bestehende Daten ändern |
| **DELETE** | Daten löschen |
| **FILE** | Datei-Operationen auf dem Server (`LOAD DATA INFILE`) – globales Recht |
| **GRANT OPTION** | Eigene Rechte an andere weitergeben |
| **ALL PRIVILEGES** | Alle verfügbaren Rechte (ausser GRANT OPTION) |
| **USAGE** | Keine Rechte – nur Connect erlaubt |

---

## 🌐 Geltungsbereiche – „WO" gelten die Rechte?

| Ebene | Syntax | Beschreibung |
|:---|:---|:---|
| **Global** | `ON *.*` | Ganzer Server – alle DBs, Tabellen, Spalten |
| **Datenbank** | `ON mydb.*` | Eine spezifische Datenbank |
| **Tabelle** | `ON mydb.tabelle1` | Einzelne Tabelle |
| **Spalte** | `(att1, att2) ON db.tbl` | Einzelne Spalten – selten genutzt, besser Views verwenden |
| **Stored Routine** | `ON PROCEDURE ...` | Gespeicherte Prozedur oder Funktion |

**Wo werden Privilegien gespeichert?**

Die Rechte landen je nach Ebene in verschiedenen Systemtabellen der `mysql`-Datenbank:

| Systemtabelle | Speichert Rechte für |
|:---|:---|
| `mysql.global_priv` | Globale Rechte (`*.*`) – seit MariaDB 10.4 die eigentliche Tabelle |
| `mysql.db` | Datenbank-Rechte (`db.*`) |
| `mysql.tables_priv` | Tabellen-Rechte (`db.tabelle`) |
| `mysql.columns_priv` | Spalten-Rechte (`db.tabelle.spalte`) |
| `mysql.procs_priv` | Rechte für Stored Procedures/Functions |

> ⚠️ Die alte `mysql.user`-Tabelle existiert seit MariaDB 10.4 nur noch als **View** auf `mysql.global_priv` – für Kompatibilität mit älteren Tools.

---

## 🛠️ GRANT und REVOKE – Rechte vergeben und entziehen

Die DCL-Befehle (Data Control Language) im Überblick:

```sql
-- Rechte vergeben
GRANT privileg1 [, privileg2, ...]
ON [datenbank.]tabelle
TO user@host [IDENTIFIED BY 'passwort'] [WITH GRANT OPTION];

-- Rechte entziehen
REVOKE privileg1 [, privileg2, ...]
ON [datenbank.]tabelle
FROM user@host;
```

**Beispiele:**

```sql
-- Alle Rechte auf hotel-DB inkl. Weitergabe
GRANT ALL ON hotel.* TO hotel_admin@localhost WITH GRANT OPTION;

-- Nur CRUD-Rechte
GRANT SELECT, INSERT, UPDATE, DELETE ON hotel.* TO hotel_user@localhost;

-- Datei-Zugriff (global)
GRANT FILE ON *.* TO username@'%';

-- Rechte prüfen
SHOW GRANTS FOR hotel_admin@localhost;
```

> 🔑 `FLUSH PRIVILEGES;` nach Änderungen nie vergessen!

---

## 👥 Rollen (RBAC) – Rollenbasierte Zugriffsverwaltung

Statt jedem Benutzer einzeln Rechte zu geben, werden **Rollen** definiert und den Benutzern zugewiesen (ab MariaDB 10.x):

```sql
-- Rollen erstellen
CREATE ROLE verkauf, management;

-- Rechte an Rollen vergeben
GRANT SELECT ON kunden.produkte TO verkauf;
GRANT SELECT, INSERT, UPDATE, DELETE ON kunden.* TO management;

-- Rollen an Benutzer zuweisen
GRANT verkauf TO user@localhost;

-- Rolle aktivieren (als eingeloggter User)
SET ROLE verkauf;

-- Default-Rolle setzen (automatisch beim Login aktiv)
SET DEFAULT ROLE verkauf FOR user@localhost;
```

**Zugriffsmatrix – Beispiel:**

| Tabelle | Verkauf: S | I | U | D | Management: S | I | U | D |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| produkte | ✅ | | | | ✅ | ✅ | ✅ | ✅ |
| personal.lohn | | | | | ✅ | | ✅ | |
| rechnungen | ✅ | | | | ✅ | ✅ | ✅ | ✅ |
| kunden | ✅ | ✅ | ✅ | | ✅ | ✅ | ✅ | ✅ |

*S = Select, I = Insert, U = Update, D = Delete*

---

## 🔒 Der pma-User für phpMyAdmin

Nach der Installation existiert ein Benutzer `pma` mit eingeschränkten Rechten auf die `phpmyadmin`-Datenbank:

```sql
SHOW GRANTS FOR pma@localhost;
-- GRANT USAGE ON *.* TO `pma`@`localhost`
-- GRANT SELECT, INSERT, UPDATE, DELETE ON `phpmyadmin`.* TO `pma`@`localhost`
```

Auch der pma-User **muss** ein Passwort bekommen:

```sql
SET PASSWORD FOR pma@localhost = PASSWORD('sicheresPasswort');
```

Das Passwort muss zusätzlich in der Datei `config.inc.php` eingetragen werden, sonst startet phpMyAdmin nicht mehr.

> ⚠️ Wer den `pma`-User löscht, kann phpMyAdmin nicht mehr verwenden. Bei versehentlichem Löschen kann er jedoch neu angelegt werden.

> 💡 Nach dem Setzen des pma-Passworts lässt sich MySQL evtl. nicht mehr über das XAMPP-Control-Panel stoppen. Workaround: `mysqladmin --user=pma --password=... shutdown`

---

## ✅ Checkpoint

Die Aufgaben sind gelöst unter: [Checkpoint 5. Tag](./Checkpoint.md)

- ✅ Privilegien und Geltungsbereiche verstanden
- ✅ GRANT / REVOKE korrekt angewendet
- ✅ Rollen (RBAC) erstellt und zugewiesen
- ✅ pma-User abgesichert

---

[⬅️ 4. Tag](../4.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [6. Tag ➡️](../6.Tag/README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

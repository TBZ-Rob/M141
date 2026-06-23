# 4. Tag – Datenbanksicherheit

![Status](https://img.shields.io/badge/Status-Abgeschlossen-brightgreen)
![Datum](https://img.shields.io/badge/Datum-02.06.26-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ 3. Tag](../3.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [5. Tag ➡️](../5.Tag/README.md)

An diesem Tag geht es darum, einen DB-Server **sicher zu betreiben**: Wie kontrolliert MySQL den Zugang, wie werden Benutzer und Passwörter verwaltet, wie greift man übers LAN auf einen Server zu – und wie härtet man die unsicheren Default-Einstellungen.

## 🎯 Lernziele

| | Lernziel |
|---|----------|
| 🛡️ | Verstehen, warum DB-Sicherheit zentral ist (reale Angriffe) |
| 🔐 | Authentifizierung erklären: Benutzername, Passwort, Hostname |
| 👤 | Benutzer anlegen, Passwörter setzen/verschlüsseln, löschen |
| 🌐 | Über das Netzwerk auf einen DB-Server zugreifen (Backup/Restore) |
| 🔒 | Default-Einstellungen absichern (root, externe Zugriffe) |

---

## 🛡️ Warum Datenbank-Sicherheit?

**Was:** Cybersicherheit ist für die Verfügbarkeit von Onlineangeboten zentral – ein unsicherer DB-Server ist ein beliebtes Angriffsziel.

**Warum:** Die häufigsten Angriffsarten zeigen, wie breit die Bedrohung ist.

![Häufigste Angriffe](./screenshots/Angriffe.png)

| Anteil | Angriffsart |
|--------|-------------|
| 29 % | Ransomware |
| 28 % | DDoS |
| 25 % | Ausnutzung von Schwachstellen in Open-Source-Software |
| 22 % | Social Engineering |
| 20 % | Angriffe auf APIs / Webanwendungen |

**Wie real das ist:** Ein öffentlicher TBZ-Raspi mit MySQL-Server wurde 2023 angegriffen – es existierte ein Benutzer `'admin'@'%'` **ohne Passwort**.

![Admin ohne Passwort](./screenshots/XAMPP-Admin-noPW.png)

Die Folge: Die Datenbanken wurden verschlüsselt und gegen ein Bitcoin-Lösegeld „angeboten" (klassische Ransomware).

![Ransomware-Forderung](./screenshots/XAMPP-RansomeWare.png)

> ⚠️ XAMPP ist eine **Entwicklungsumgebung** – Sicherheitsvorkehrungen sind bewusst deaktiviert (z.B. `root` ohne Passwort). Für den produktiven Betrieb muss zwingend nachgehärtet werden.

---

## 🔐 Zugangskontrolle – Authentifizierung

MySQL kontrolliert den Zugang in **zwei Phasen**:

| Phase | Frage | Wann |
|-------|-------|------|
| **Authentifizierung** | Wer darf sich verbinden? | Beim Verbindungsaufbau |
| **Autorisierung** | Was darf der Benutzer? | Bei jedem Request (→ [Tag 5](../5.Tag/README.md)) |

Die Authentifizierung prüft drei Angaben aus der View `mysql.user`:

![mysql.user View](./screenshots/mysql_user_view.png)

| Information | Bedeutung |
|-------------|-----------|
| **Benutzername** | Name für die DB-Anmeldung (unabhängig vom Betriebssystem-User) |
| **Passwort** | Wird **verschlüsselt** gespeichert (Default: leer) |
| **Hostname** | Von wo aus zugegriffen werden darf |

Mögliche Hostname-Angaben:

| Wert | Bedeutung |
|------|-----------|
| `localhost` | nur lokal auf dem Server |
| `%` | von **überall extern** (nicht lokal) |
| `172.16.17.111` | nur von dieser **einen IP** |
| `172.16.17.%` | von dieser **IP-Range** |
| `name.local` | von diesem **Hostnamen** |

---

## 👤 Benutzer erstellen & Passwörter

**Externen Benutzer (`%`) mit Passwort anlegen:**

```sql
DROP USER IF EXISTS 'user_rem'@'%';
CREATE USER 'user_rem'@'%' IDENTIFIED BY 'Passw0rt';
```

**Lokalen Benutzer (`localhost`) ohne Passwort anlegen** (nur über die Konsole möglich – phpMyAdmin verlangt ein Passwort):

```sql
CREATE USER 'user_local'@localhost;
```

**Passwort setzen / ändern:** Passwörter werden mit einer Hashfunktion verschlüsselt (41-Byte-Hash, beginnt mit `*`).

```sql
SET PASSWORD FOR 'user'@'%' = PASSWORD('TBZforever');
FLUSH PRIVILEGES;   -- Aktivierung – nie vergessen!
```

> 🔑 `FLUSH PRIVILEGES` macht Änderungen sofort wirksam.
> ⚠️ Passwörter dürfen **nie im Klartext** in einem Skript stehen.

---

## 🌐 DB-Server im LAN

**Warum Dezentralisierung?**

| Grund | Nutzen |
|-------|--------|
| Datenverfügbarkeit | sicherer bei mehreren Servern |
| Datensicherheit | Zugriffssteuerung bei kleineren Beständen einfacher |
| Flexibilität | Teilsysteme leichter änderbar |
| Performance | besser verteilt auf mehrere Rechner |
| Kosten | günstiger als ein Grosscomputer |

**Wie:** Der Zugriff funktioniert wie lokal, nur wird zusätzlich die **IP/Hostname** des Servers über `-h` angegeben. Eine Firewall muss **Port 3306** offen haben.

| Befehl | Testet … |
|--------|----------|
| `ping 172.16.17.4` | ob der **Rechner** erreichbar ist |
| `mysqladmin -h 172.16.17.4 -u remote -p ping` | ob der **DB-Dienst** läuft (`mysqld is alive`) |
| `mysql -h 172.16.17.4 -u remote -p` | **Login** auf den DB-Server |

**Backup/Restore über das Netz** – der Remote-User braucht globale Lese-Rechte inkl. `LOCK TABLES`:

![Globale Rechte für Remote-User](./screenshots/Remote_Rechte.png)

```sql
mysqldump -h 172.16.17.4 -u remote -p firma > H:\backup.sql
mysql     -h 172.16.17.4 -u remote -p firma < H:\backup.sql
```

**Netzzugriff temporär sperren:** Eintrag `skip-networking` in der `my.ini` unter `[mysqld]` verbietet jeden TCP/IP-Zugriff (auch lokal).

---

## 🚫 phpMyAdmin extern & Fehler 403

Beim externen Aufruf von `IP-Hostname/phpmyadmin` kann folgender Fehler auftreten:

![403 Forbidden](./screenshots/Forbidden.png)

**Lösung:** In der Datei `httpd-xampp.conf` (Abschnitt `phpmyadmin`) den Eintrag `Require local` durch `Require all granted` ersetzen.

![Require all granted](./screenshots/require_all_granted.png)

> Tipp: Zuerst grundsätzlich den Apache-Zugriff über `IP-Hostname/Dashboard` testen. Es könnte auch eine Firewall-Regel für HTTP greifen.

---

## 🔒 Default-Einstellungen härten

Direkt nach der Installation sollten diese Schritte erfolgen:

| Massnahme | Befehl / Vorgehen |
|-----------|-------------------|
| `root`-Passwort lokal setzen | `SET PASSWORD FOR root@localhost = PASSWORD('…'); FLUSH PRIVILEGES;` |
| `root`-Zugang von extern sperren | `DROP USER 'root'@'%';` (oder Rechte entziehen) |
| Kein Login ohne PW von extern | jedem `%`-User ein Passwort geben |
| Lokalen Zugang ohne PW erlauben (optional) | `GRANT USAGE ON *.* TO ''@localhost;` |

> ⚠️ Aufpassen, dass man `root` nicht versehentlich die nötigen Rechte entzieht – sonst sperrt man sich selbst aus.
> 📘 Für professionelles Hardening: die kostenlosen **CIS Benchmarks** sind ein guter Einstieg.

---

## ⚠️ Stolperstein (Reflexion)

Beim Untersuchen der Tabellen habe ich `aria_chk` **auf aktive System-Tabellen** angewendet – das hat den MariaDB-Server zum Absturz gebracht. **Learning:** `aria_chk` nur auf gestopptem Server bzw. nie auf den laufenden System-Tabellen ausführen, sonst wird die `mysql`-Datenbasis beschädigt und der Server startet nicht mehr.

---

## ✅ Checkpoint

Die Aufgaben sind gelöst unter: [Checkpoint 4. Tag](./Checkpoint.md)

- ✅ MySQL-Server mit Passwörtern (root, pma, remote) geschützt
- ✅ Zugriff auf den DB-Server eines/r Lernenden inkl. Backup/Restore verstanden
- ✅ Zugriff auf den DB-Server der LP inkl. Backup/Restore verstanden

---

[⬅️ 3. Tag](../3.Tag/README.md) · [🏠 Übersicht](../README.md) · [✅ Checkpoint](./Checkpoint.md) · [5. Tag ➡️](../5.Tag/README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

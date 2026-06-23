# ✅ Checkpoint – 4. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-4-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 4](./README.md) · [🏠 Übersicht](../README.md)

Lösungen zum Checkpoint **DB-Server im LAN / Datenbank-Sicherheit**.

---

## 🔘 Multiple Choice

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Befehl, der die Verbindung zum **Server-Rechner** `139.79.124.97` testet | ✅ `ping 139.79.124.97` |
| 2 | Wozu dient der Parameter `-h` bei MySQL? | ✅ Angabe der **Adresse des Server-Rechners** (`h` = host) |
| 3 | Was bewirkt `mysqldump -h 139.79.124.97 hotel > datei.txt`? | ✅ **Backup** der DB `hotel` vom Server `139.79.124.97` – die Datei `datei.txt` wird dabei **lokal** geschrieben |
| 4 | Aufgabe des ODBC-Drivers | ✅ Ermöglicht den **einheitlichen Zugriff** einer Applikation auf **verschiedene** Datenbanken |
| 5 | Zugriff vom Konsolenfenster auf den DB-Server `139.79.124.97` | ✅ `mysql -h 139.79.124.97 -u root -p` |

> 💡 Zu Frage 1: `ping` testet nur, ob der **Rechner** erreichbar ist. Ob der **DB-Dienst** läuft, prüft man mit `mysqladmin -h 139.79.124.97 -u <user> -p ping` → Antwort `mysqld is alive`.

---

## ✏️ Offene Fragen

**1. Welche Aufgaben hat der DB-Server im Gegensatz zum DB-Client?**

Der **Server** speichert und verwaltet die Daten, führt die SQL-Abfragen aus, regelt Zugriffsrechte sowie Transaktionen und liefert die Resultate zurück. Der **Client** baut die Verbindung auf, schickt die Anfragen und stellt die Ergebnisse dar (Benutzeroberfläche). Kurz: Server = Datenhaltung + Logik, Client = Bedienung + Anzeige.

**2. Weshalb benutzt man MS Access z.B. zusammen mit einem MySQL-Server?**

Access dient als **Frontend** (Formulare, Berichte, komfortable GUI), MySQL als robustes, mehrbenutzerfähiges **Backend** für die eigentliche Datenhaltung. Verbunden werden beide über **ODBC**. Vorteile gegenüber einer reinen Access-Datei: zentrale Datenhaltung, echter Mehrbenutzerbetrieb, höhere Datensicherheit und bessere Performance.

**3. Wie bestimmen Sie die IP-Adresse des Server-Rechners?**

Auf dem Server-Rechner selbst mit `ipconfig` (Windows) bzw. `ip a` / `ifconfig` (Linux). Im fremden Netz alternativ über einen Netzwerkscanner (z.B. Advanced IP Scanner).

**4. Wie prüfen Sie, ob der DB-Server auf Adresse `139.79.124.97` läuft?**

```batch
mysqladmin -h 139.79.124.97 -u <user> -p ping
```

Antwortet der Server mit `mysqld is alive`, läuft der Dienst. (Ein blosses `ping` sagt nur etwas über den Rechner aus, nicht über den DB-Dienst.)

**5. Welcher Befehl führt das SQL-Skript `xy.sql` auf die DB `hotel` auf Adresse `139.79.124.97` aus?**

```batch
mysql -h 139.79.124.97 -u <user> -p hotel < xy.sql
```

---

[⬅️ Tag 4](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

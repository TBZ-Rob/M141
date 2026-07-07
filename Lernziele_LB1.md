# 🎓 Lernziele LB1

![Status](https://img.shields.io/badge/LB-1-blue)
![Gewicht](https://img.shields.io/badge/Gewicht-20%25-orange)
![Datum](https://img.shields.io/badge/Datum-09.06.26-brightgreen)

**LB1** (Tag 1–5, ca. 60 Minuten): DBMS, Konfiguration & Datenimport, Tabellentypen & Transaktionen, Authentifizierung

- 20–30 min **Theorie** mit Spick (max. 3 × A4)
- 20–30 min **Praxis** Openbook mit DBMS & KI

---

## Tag 1: Grundlagen & Installation

### Lernziele

- **Begriffe:** Datenbank, DBMS, Datenbank-Klient, Datenbank-Server verstehen
- **DB-Modelle:** Relationale, hierarchische, NoSQL-Datenbanken kennen
- **MySQL/MariaDB:** Unterschiede und Einsatzgebiete
- **Installation:** XAMPP, Workbench, phpMyAdmin funktionsfähig installieren

### Checkpoints

- ✅ Komponenten eines DB-Systems benennen
- ✅ Client/Server-Architektur erklären
- ✅ MySQL-Server starten (via XAMPP, CMD, Workbench)
- ✅ Mit 3 Klienten verbinden (mysql.exe, Workbench, phpMyAdmin)

---

## Tag 2: Konfiguration & Datenimport

### Lernziele

- **my.ini:** Struktur, wichtige Parameter, Änderungen anwenden
- **Startparameter:** Wie Optionen beim Server-Start wirken
- **Datenimport:** CSV, SQL-Dumps, JSON in die DB laden
- **Zeichensätze:** Kodierung, Collation verstehen

### Checkpoints

- ✅ my.ini-Einträge erklären (port, datadir, character_set)
- ✅ Server mit Parametern neu starten
- ✅ CSV-Datei in Tabelle importieren
- ✅ SQL-Dump einlesen (mysqldump, Workbench)

---

## Tag 3: Tabellentypen & Transaktionen

### Lernziele

- **Storage Engines:** MyISAM vs. InnoDB verstehen
- **Transaktionen:** ACID-Prinzipien, BEGIN/COMMIT/ROLLBACK
- **Locking:** Sperrmechanismen und Konflikte
- **Referenzielle Integrität:** Foreign Keys und Constraints

### Checkpoints

- ✅ MyISAM und InnoDB vergleichen
- ✅ Transaktionen durchführen (COMMIT/ROLLBACK)
- ✅ Locks testen (2 Sessions, ein Datensatz)
- ✅ Foreign Keys erstellen und testen

---

## Tag 4: Datenbanksicherheit

### Lernziele

- **Authentifizierung:** Benutzer, Passwörter, Host-Beschränkung
- **Härtung:** Standard-Passwörter entfernen, anonyme User löschen
- **Netzwerk:** Remote-Zugriff konfigurieren (Host, Port)
- **Häufige Angriffe:** Injection, Default-Credentials, fehlende Logs

### Checkpoints

- ✅ Hacker-Angriffsvektoren identifizieren
- ✅ Anonyme User und Test-DB löschen
- ✅ MySQL-User mit Passwort anlegen
- ✅ Remote-Zugriff testen (von anderem Host)

---

## Tag 5: Zugriffssystem & Autorisierung **(LB1 Praxisteil)**

### Lernziele

- **Autorisierung:** GRANT/REVOKE, Privilegien (SELECT, INSERT, UPDATE, DELETE)
- **Berechtigungsebenen:** Global, Datenbank, Tabelle, Spalte
- **Rollen:** Benutzergruppen, Standard-Rollen
- **Best Practices:** Least-Privilege-Prinzip

### Checkpoints

- ✅ User mit spezifischen Rechten erstellen
- ✅ GRANT/REVOKE korrekt anwenden
- ✅ Rechtevergabe testen (verschiedene User, verschiedene Operationen)
- ✅ Rollen implementieren und zuweisen

---

## 📊 Bewertungskriterien LB1

| Kriterium | Punkte |
|-----------|--------|
| Theorie (Spick + Prüfung) | 10 |
| Praxis (DBMS-Übungen) | 10 |
| **Total** | **20** |

---

## 📚 Ressourcen

- [Tag 1 – README](../Lernportfolio/1.Tag/README.md)
- [Tag 2 – README](../Lernportfolio/2.Tag/README.md)
- [Tag 3 – README](../Lernportfolio/3.Tag/README.md)
- [Tag 4 – README](../Lernportfolio/4.Tag/README.md)
- [Tag 5 – README](../Lernportfolio/5.Tag/README.md)
- [Literatur & Links](./Literatur.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

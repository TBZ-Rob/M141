# ✅ Checkpoint 1. Tag

![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)

---

## Einführung, DB-Engines, XAMPP

**1. Häufigste Datenbank-Art?**
- ✅ Relationale Datenbank

**2. Komponenten in einem DB-Server?**
- ✅ 1 oder mehrere Datenbanken
- ✅ Datenbank-Management-System (DBMS)

**3. Relationale Datenbanken?**
- ✅ Oracle
- ✅ MySQL
- ✅ MariaDB
- ✅ MS Access
- ✅ PostgreSQL

**4. Aufgaben eines DB-Clients?**
- ✅ Stellt dem Benutzer ein User-Interface für den Datenzugriff zur Verfügung
- ✅ Leitet die Befehle des Benutzers an den DB-Server weiter

**5. Client-Komponenten von MySQL?**
- ✅ mysql
- ✅ phpMyAdmin

**6. Server-Komponente von MySQL?**
- ✅ mysqld

---

## Offene Fragen

**7. Client/Server-Modell:**
Der Server stellt Dienste (z.B. Datenbankzugriff) zentral bereit. Clients verbinden sich über ein Netzwerk und senden Anfragen, die der Server verarbeitet und beantwortet.

**8. Vorteile Client/Server gegenüber Desktop-DB:**
- Mehrere Clients können gleichzeitig auf dieselben Daten zugreifen
- Zentrale Datenverwaltung und Sicherheit
- Keine lokale Installation der DB auf jedem Client nötig

**9. Datenspeicherung in relationaler DB:**
Daten werden in Tabellen (Relationen) gespeichert – strukturiert in Zeilen (Datensätze) und Spalten (Attribute).

**10. Vorteile referentielle Datenintegrität:**
Verhindert verwaiste Datensätze (z.B. kein Mitarbeiter ohne gültige Abteilung). Stellt Konsistenz zwischen verknüpften Tabellen sicher.

**11. 4 NoSQL-Gruppen:**
- Key-Value Stores (z.B. Redis)
- Document Stores (z.B. MongoDB)
- Column-Family Stores (z.B. Cassandra)
- Graph-Datenbanken (z.B. Neo4j)

**12. DBaaS (Database as a Service):**
Datenbank wird als Cloud-Dienst bereitgestellt. Kein eigener Server nötig. Beispiel: AWS RDS – man mietet eine MySQL-Datenbank bei Amazon und greift über das Internet darauf zu.

**13. Vorteile RDBMS gegenüber anderen DB-Modellen:**
- Standardisierte Abfragesprache (SQL)
- ACID-Transaktionen (Atomicity, Consistency, Isolation, Durability)
- Hohe Datenkonsistenz durch referentielle Integrität
- Weit verbreitet und gut dokumentiert

---

## Praktische Aufgaben

**14. DB-Server starten/stoppen:**

| Methode | Befehl / Weg |
|---------|-------------|
| XAMPP Control Panel | Apache + MySQL → Start/Stop |
| CMD | `net start mysql` / `net stop mysql` |
| Workbench | Nur wenn MySQL als Windows-Dienst läuft |

**15. DB-Server prüfen:**

| Tool | Was prüfen |
|------|------------|
| Task-Manager | Prozess `mysqld.exe` läuft |
| Dienst-Manager | Dienst `MySQL` hat Status „Gestartet" |
| mysql / phpMyAdmin | Verbindung erfolgreich |

---

| [🏠 Übersicht](../../README.md) | [⬅️ Tag 1](../README.md) |
|---|---|

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

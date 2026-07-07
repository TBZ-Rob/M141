# ✅ Checkpoint – 7. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-7-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 7](./README.md) · [🏠 Übersicht](../README.md)

Nachweis zum **Testprotokoll: Datenbank mit Testdaten testen**.

---

## ✅ Checkliste Testprotokoll

| # | Schritt | Status |
|---|---------|--------|
| 1 | Login mit Test-User (scheitert erwartungsgemäss) | ✅ |
| 2 | User `Reader` und `Contributor` erstellt, Login getestet | ✅ |
| 3 | Schema `myTestDb` mit Tabellen `Person` und `Adresse` erstellt (ohne PK/Index) | ✅ |
| 4 | Bulk-Import: je 400'000 Datensätze via `LOAD DATA INFILE` geladen | ✅ |
| 5 | Rollen `RoleReader` / `RoleContributor` erstellt und Benutzern zugewiesen | ✅ |
| 6 | Berechtigungen geprüft: Reader nur SELECT, Contributor CRUD | ✅ |
| 7 | Datenintegrität: 3 Duplikate gefunden und bereinigt, PK gesetzt | ✅ |
| 8 | Performance ohne Index: ~9.5 s (Table Scan) | ✅ |
| 9 | Index auf `Person.AdresseId` erstellt | ✅ |
| 10 | Performance mit 1 Index: ~1.2 s (~8× schneller) | ✅ |
| 11 | Index auf `Adresse.Id` erstellt | ✅ |
| 12 | Performance mit 2 Indizes: ~0.16 s (~60× schneller) | ✅ |
| 13 | Weitere Tests: Negativ-/Grenztests, ROLLBACK, Backup/Restore, Locking | ✅ |
| 14 | Benchmark mit `mysqlslap` (30 Clients, 3000 Queries) | ✅ |
| 15 | Schlussbilanz erstellt | ✅ |

---

## 💡 Kernerkenntnisse

**Indizes sind der grösste Performance-Hebel.** Ohne Index durchsucht MariaDB bei einem JOIN alle 400'000 Datensätze beider Tabellen (Table Scan). Mit Indizes auf den Join-Spalten reduziert sich die Suchzeit um den Faktor 60.

**Datenbereinigung ist Pflicht vor Constraints.** Duplikate in der Adress-Tabelle mussten entfernt werden, bevor ein PRIMARY KEY gesetzt werden konnte. In der Praxis ist dieser Schritt oft der aufwändigste.

**RBAC macht die Berechtigungsverwaltung sauber.** Statt jedem User einzeln Rechte zu geben, definiert man Rollen und weist diese zu. Beim Testen wurde verifiziert, dass Reader kein UPDATE ausführen kann und Contributor alle CRUD-Operationen hat.

---

[⬅️ Tag 7](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

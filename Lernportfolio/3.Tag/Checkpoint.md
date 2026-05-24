# ✅ Checkpoint 3. Tag

![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)
![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)

---

## Tabellentypen und Transaktionen

**1. Mehrere DB-Operationen in einem Schritt?**
- ✅ Transaktion

**2. Warum Locks schnell freigeben?**
- ✅ damit andere DB-Anwender nicht lange warten müssen
- ✅ damit möglichst viele Benutzer gleichzeitig zugreifen können

**3. Standard-Tabellenformat MySQL/MariaDB?**
- ✅ InnoDB

**4. Wann InnoDB verwenden?**
- ✅ wenn auf gar keinen Fall ein Datenverlust vorkommen darf
- ✅ wenn viele Benutzer gleichzeitig Daten ändern

**5. Tablespace?**
- ✅ Datei, welche alle InnoDB-Tabellen enthält (virtueller Speicher)
- ✅ wird nach Erreichen von x MB automatisch vergrössert

**6. Transaktionen steuern?**
- ✅ COMMIT; oder ROLLBACK;
- ✅ BEGIN; oder START TRANSACTION;

**7. Locking bei InnoDB-Transaktionen?**
- ✅ Row locking
- ✅ nur die gerade bearbeiteten Datensätze werden gesperrt

---

## Offene Fragen

**8. Vorteile InnoDB gegenüber MyISAM?**
Row-Level-Locking, Transaktionsunterstützung, referentielle Integrität, Crash-Recovery nach Stromausfall.

**9. MyISAM-Tabelle KUNDEN gespeichert in?**
- `KUNDEN.FRM` – Tabellenbeschreibung
- `KUNDEN.MYD` – Daten
- `KUNDEN.MYI` – Indexe

**10. SQL für InnoDB-Tabelle BESTELLUNGEN?**
```sql
CREATE TABLE BESTELLUNGEN (
  id INT AUTO_INCREMENT PRIMARY KEY,
  Datum DATE,
  Betrag DECIMAL(10,2)
) ENGINE=InnoDB;
```

**11. Locking-Art:**
- MyISAM → **Table-Level-Locking** – ganze Tabelle wird gesperrt
- InnoDB → **Row-Level-Locking** – nur betroffene Datensätze werden gesperrt

**12. Datenbank-Transaktion?**
Eine Gruppe von SQL-Befehlen, die entweder ganz oder gar nicht ausgeführt wird. Eingeleitet mit `BEGIN`, abgeschlossen mit `COMMIT` oder `ROLLBACK`.

**13. I in ACID = Isolation?**
Transaktionen beeinflussen sich nicht gegenseitig. Laufende Änderungen einer Transaktion sind für andere Clients nicht sichtbar bis zum COMMIT.

**14. Datenkonsistenz nach Crash?**
InnoDB schreibt alle Transaktionen in Log-Dateien (`ib_logfile0`, `ib_logfile1`). Beim nächsten Start werden vollständig abgeschlossene Transaktionen wiederhergestellt, unvollständige automatisch zurückgerollt (Crash-Recovery).

**15. SELECT wartet auf Entsperrung?**
`SELECT ... LOCK IN SHARE MODE` – wartet bis alle Exclusive Locks aufgelöst sind.

**16. Autocommit für explizites COMMIT?**
```sql
SET AUTOCOMMIT=0;
```
→ Jeder SQL-Befehl gehört automatisch zu einer Transaktion und muss explizit mit `COMMIT` bestätigt werden.

---

| [🏠 Übersicht](../../README.md) | [⬅️ Tag 3](../README.md) |
|---|---|

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

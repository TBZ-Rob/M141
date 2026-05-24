# 🗄️ Tag 3 – Transaktionen & Tabellentypen

![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)
![Geplant](https://img.shields.io/badge/Geplant-26.05.2025-lightgrey)
![Durchgeführt](https://img.shields.io/badge/Durchgeführt-22.%26%2024.04.2026-blue)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

> ⚠️ Dieser Tag wurde nicht am geplanten Datum (26.05.2025) durchgeführt, sondern aufgeteilt auf den **22. und 24. April 2026**.

> 💬 **Claude Prompt für dieses File:**
> *„Analysiere das ganze Repo, aktualisiere jedes Diagramm oder Darstellung auf den neusten Stand und füge bei neuen Seiten hinzu."*

---

### 🗄️ Tabellentypen

InnoDB, MyISAM und Aria wurden verglichen. Der wichtigste Unterschied: MyISAM verwendet Table-Level-Locking und unterstützt keine Transaktionen, InnoDB hingegen Row-Level-Locking und volle ACID-Transaktionen.

Die Engine kann nachträglich geändert werden:
```sql
ALTER TABLE tabellenname ENGINE=InnoDB;
```

**Verzeichnisstruktur nach Engine-Wechsel:**
Jede MyISAM-Tabelle erzeugt 3 Dateien (`.FRM`, `.MYD`, `.MYI`), eine InnoDB-Tabelle nur `.FRM` + `.ibd` (Tablespace).

![Engine Wechsel](./screenshots/3t_engine_wechsel.png)

---

### 🏨 Hotel-Datenbank

Die `hotel`-Datenbank wurde importiert und die Tabelle `benutzer` auf InnoDB umgestellt. Anschliessend wurden alle Tabellentypen abgefragt und die Dateistruktur im `data`-Verzeichnis kontrolliert.

![Hotel Engines](./screenshots/3t_hotel_tabellen_engines.png)

![data Verzeichnis](./screenshots/3t_hotel_data_verzeichnis.png)

---

### 💾 Tablespace & my.ini

Der Tablespace wurde mit `INNODB_SYS_TABLESPACES` abgefragt. In der `my.ini` wurde überprüft, dass `skip-innodb` auskommentiert und `innodb_lock_wait_timeout=50` gesetzt ist.

![Tablespace](./screenshots/3t_tablespace.png)

![my.ini InnoDB](./screenshots/3t_myini_innodb.png)

---

### 🔄 Transaktionen

**Konto-Transaktion:** Ein Betrag von CHF 1000 wurde mit `BEGIN`, `UPDATE` und `COMMIT` von Konto "Von" auf "Nach" überwiesen.

```sql
BEGIN;
UPDATE tbl_konto SET Saldo = Saldo - 1000 WHERE name = 'Von';
UPDATE tbl_konto SET Saldo = Saldo + 1000 WHERE name = 'Nach';
COMMIT;
```

![Konto Transaktion](./screenshots/3t_transaktion_konto.png)

**ROLLBACK:** Änderungen können mit `ROLLBACK` rückgängig gemacht werden – nach dem ROLLBACK war der ursprüngliche Saldo wiederhergestellt.

![ROLLBACK](./screenshots/3t_rollback.png)

**AUTOCOMMIT=0:** Ohne `BEGIN` wird durch `AUTOCOMMIT=0` trotzdem eine Transaktion gestartet.

![Autocommit](./screenshots/3t_autocommit.png)

---

### 🔒 Locking-Demo

Die drei Locking-Mechanismen wurden mit zwei CMD-Fenstern (Client A & B) getestet:

**1. MyISAM Table-Lock:** Client B musste warten bis Client A die Tabelle freigab. Nach ENGINE=InnoDB-Wechsel funktionierte das Row-Locking korrekt.

![Locking Demo](./screenshots/3t_locking_demo.png)

**2. SELECT FOR UPDATE:** Client B wartete 25 Sekunden bis Client A committete.

![SELECT FOR UPDATE](./screenshots/3t_select_for_update.png)

**3. LOCK IN SHARE MODE:** Interessant: Ein **Deadlock** trat auf – MariaDB erkannte ihn automatisch und brach eine Transaktion ab.

![LOCK IN SHARE MODE](./screenshots/3t_lock_in_share_mode.png)

---

### 🧪 Transaktions-Demo (Zeitpunkte 1–5)

Mit zwei Clients wurde die Isolation von Transaktionen demonstriert:

| Zeitpunkt | Client A | Client B |
|-----------|----------|----------|
| 1 | Sieht colB=11 (eigene Transaktion) | Sieht noch colB=10 (Isolation) |
| 2 | Transaktion läuft | Wartet auf Lock |
| 3 | COMMIT | Läuft weiter |
| 4 | Sieht colB=11 | Sieht colB=14, macht ROLLBACK |
| 5 | Beide sehen colB=11 | |

![Zeitpunkt 1 Client A](./screenshots/3t_zeitpunkt1_clientA.png)
![Zeitpunkt 1 Client B](./screenshots/3t_zeitpunkt1_clientB.png)
![Zeitpunkt 4 Client B](./screenshots/3t_zeitpunkt4_clientB.png)

---

### 💡 Erkenntnisse

Heute wurden neue SQL-Befehle kennengelernt:

**`BEGIN`** – Startet eine Transaktion. Alle nachfolgenden Befehle werden erst mit `COMMIT` gespeichert oder mit `ROLLBACK` rückgängig gemacht.

**`UPDATE`** – Ändert bestehende Datensätze. Wichtig: Immer mit `WHERE` verwenden, sonst werden alle Zeilen geändert.

Besonders eindrücklich war der automatisch erkannte **Deadlock** und die **Isolation** – Client B sah die Änderungen von Client A erst nach dem `COMMIT`.

---

### 🔗 Weitere Seiten

- [✅ Checkpoint](./Checkpoint.md)

---

### ✅ [Checkpoint](./Checkpoint.md)

| Ziel | Status |
|------|--------|
| Tabellentypen verglichen | ✅ |
| Engine-Wechsel durchgeführt | ✅ |
| hotel DB importiert | ✅ |
| Tablespace abgefragt | ✅ |
| my.ini geprüft | ✅ |
| Transaktionen mit BEGIN/COMMIT/ROLLBACK | ✅ |
| AUTOCOMMIT getestet | ✅ |
| Locking-Demos (3 Arten) | ✅ |
| Transaktions-Demo Zeitpunkte 1–5 | ✅ |
| SHOW ENGINE INNODB STATUS | ✅ |
| LOCK TABLES | ✅ |

---

| [🏠 Übersicht](../README.md) | [⬅️ Tag 2](../2.Tag/README.md) | [✅ Checkpoints](../Checkpoints/README.md) | [➡️ Tag 4](../4.Tag/README.md) |
|---|---|---|---|

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

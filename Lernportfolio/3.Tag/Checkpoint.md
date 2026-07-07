# ✅ Checkpoint – 3. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-3-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 3](./README.md) · [🏠 Übersicht](../README.md)

Tabellentypen & Transaktionen — Lösungen zum Checkpoint.

---

## 🔘 Multiple Choice – Storage Engines

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Welche Storage Engine unterstützt Transaktionen? | ✅ **InnoDB** (MyISAM nicht) |
| 2 | Welche Engine ist für hohes Aufkommen optimiert? | ✅ **InnoDB** (mit ACID) |
| 3 | Kann MyISAM Transaktionen durchführen? | ❌ **Nein** (nur Tabellen-Lock) |
| 4 | Welche Engine erlaubt Fremdschlüssel? | ✅ **InnoDB** (MyISAM unterstützt keine FK) |
| 5 | Performance: MyISAM vs InnoDB bei Writes? | InnoDB ist sicherer, MyISAM schneller (ohne ACID) |

---

## ✏️ Offene Fragen – Transaktionen

**1. Was ist eine Transaktion?**

Eine logische Einheit von SQL-Befehlen, die ganz ausgeführt oder ganz zurückgerollt wird (Alles-oder-Nichts-Prinzip). Sorgt für Datenkonsistenz.

**2. Erklären Sie die ACID-Prinzipien:**

- **A (Atomicity):** Transaktion ganz oder gar nicht
- **C (Consistency):** Vor/nach: konsistenter Zustand
- **I (Isolation):** Transaktionen beeinflussen sich nicht
- **D (Durability):** Nach Commit: Daten auf Disk gespeichert

**3. Was ist der Unterschied zwischen COMMIT und ROLLBACK?**

- **COMMIT:** Transaktionsänderungen werden permanent
- **ROLLBACK:** Transaktionsänderungen werden rückgängig gemacht

**4. Was sind Locks und wann entstehen Konflikte?**

Locks sperren Ressourcen während Änderungen. Konflikte entstehen, wenn 2 Transaktionen denselben Datensatz ändern wollen → Deadlock oder Warten.

**5. Wie kann man Deadlocks vermeiden?**

- Immer in **gleicher Reihenfolge** auf Tabellen zugreifen
- **Transaktionen kurz** halten
- **Isolationslevel** richtig wählen
- **Timeouts** setzen

---

## 🧪 Praktische Aufgaben

### Aufgabe 1: InnoDB vs MyISAM vergleichen

```sql
-- Tabelle mit MyISAM erstellen
CREATE TABLE test_myisam (
  id INT PRIMARY KEY
) ENGINE=MyISAM;

-- Tabelle mit InnoDB erstellen
CREATE TABLE test_innodb (
  id INT PRIMARY KEY
) ENGINE=InnoDB;

-- Engines abfragen
SHOW TABLE STATUS WHERE Name IN ('test_myisam', 'test_innodb');
```

### Aufgabe 2: Transaktion durchführen

```sql
-- Transaktion starten
START TRANSACTION;

UPDATE konten SET saldo = saldo - 100 WHERE account_id = 1;
UPDATE konten SET saldo = saldo + 100 WHERE account_id = 2;

-- Überprüfen
SELECT * FROM konten WHERE account_id IN (1, 2);

-- Entweder:
COMMIT;   -- Änderungen speichern
-- ODER:
ROLLBACK; -- Änderungen rückgängig
```

### Aufgabe 3: Locking testen

**Session 1:**
```sql
START TRANSACTION;
UPDATE person SET name = 'Test1' WHERE id = 1;
-- Kein COMMIT - Lock bleibt aktiv
```

**Session 2:**
```sql
UPDATE person SET name = 'Test2' WHERE id = 1;
-- ⏳ Wartet auf Session 1
```

**Session 1:**
```sql
COMMIT; -- Lock freigeben → Session 2 kann jetzt aktualisieren
```

---

## 📊 Vergleichstabelle

| Aspekt | MyISAM | InnoDB |
|--------|--------|--------|
| **Transaktionen** | ❌ Nein | ✅ Ja (ACID) |
| **Foreign Keys** | ❌ Nein | ✅ Ja |
| **Locking** | Table-Level | Row-Level |
| **Crash-Recovery** | ❌ Schwierig | ✅ Robust |
| **Performance (Read)** | ⚡ Schnell | 🟡 Mittel |
| **Performance (Write)** | 🟡 Mittel | ⚡ Optimiert |
| **Best für** | Read-heavy | Production |

---

[⬅️ Tag 3](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

# 🎓 Lernziele LB2

![Status](https://img.shields.io/badge/LB-2-blue)
![Gewicht](https://img.shields.io/badge/Gewicht-30%25-orange)
![Datum](https://img.shields.io/badge/Datum-23.06.26-brightgreen)

**LB2** (Tag 4–7, ca. 60–90 Minuten): Server-Administration, Logging, Testen, Performance

- 20–30 min **Theorie** mit Spick (max. 3 × A4)
- 40–60 min **Praxis** Openbook mit DBMS & KI

---

## Tag 4–5: Sicherheit & Zugriff (Wiederholung)

Siehe [Lernziele LB1](./Lernziele_LB1.md)

---

## Tag 6: Server-Administration im Produktivbetrieb

### Lernziele

- **Konfiguration:** my.ini für Produktion, Logging, Speicher-Parameter
- **Logging:** Error Log, Binary Log, General Query Log, Slow Query Log
- **Backup & Recovery:** mysqldump, Binary Logs für Point-in-Time-Recovery
- **Optimierung:** Indizes, Query Cache, Server-Tuning
- **Überwachung:** Status-Informationen, Performance-Metriken

### Checkpoints

- ✅ my.ini für Produktion konfigurieren
- ✅ Verschiedene Log-Typen aktivieren und interpretieren
- ✅ mysqldump durchführen und Restore testen
- ✅ Indizes erstellen und mit EXPLAIN analysieren
- ✅ Query Cache konfigurieren und testen
- ✅ Server-Parameter (key_buffer_size, table_cache) anpassen

---

## Tag 7: Datenbank mit Testdaten testen

### Lernziele

- **Testplanung:** Systematisches Testvorgehen
- **Test-Benutzer:** Rollen mit unterschiedlichen Rechten erstellen
- **Bulk-Import:** Grosse Datenmengen laden und validieren
- **Datenintegrität:** Primary Keys, Foreign Keys, Duplikate prüfen
- **Performance-Test:** Mit und ohne Indizes vergleichen (EXPLAIN)
- **Nebenläufigkeit:** Concurrent Access, Locking testen

### Checkpoints

- ✅ Test-Benutzer mit Rollen erstellen (Reader, Contributor, Admin)
- ✅ 400'000+ Datensätze importieren (LOAD DATA INFILE)
- ✅ Datenintegrität prüfen (Duplikate, verwaiste FKs)
- ✅ Performance ohne Index vs. mit Index vergleichen (>50× Unterschied!)
- ✅ Backup & Restore funktioniert
- ✅ Concurrent Locks testen

---

## 📊 Bewertungskriterien LB2

| Kriterium | Punkte |
|-----------|--------|
| Theorie (Spick + Prüfung) | 15 |
| Praxis (Admin-Übungen + Testing) | 15 |
| **Total** | **30** |

---

## 📚 Ressourcen

- [Tag 6 – README](../Lernportfolio/6.Tag/README.md)
- [Tag 7 – README](../Lernportfolio/7.Tag/README.md)
- [Literatur & Links](./Literatur.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

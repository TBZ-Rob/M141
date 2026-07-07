# 📚 M141 – Datenbanksystem in Betrieb nehmen

![Status](https://img.shields.io/badge/Klasse-PE24c-blue)
![Modul](https://img.shields.io/badge/Modul-M141-orange)
![Portfolio](https://img.shields.io/badge/Portfolio-GitHub-brightgreen)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

Installiert und konfiguriert ein Datenbanksystem und führt eine Dateninitialisierung durch. Stellt die Funktionalität sicher und führt die Übergabe in den produktiven Betrieb durch.

---

## 📋 Lektionenplan mit Links

| Tag | Thema | Lernziele | Status |
|:---:|:------|-----------|:------:|
| **1** | [Intro & Installation](./Lernportfolio/1.Tag/README.md) | RDBMS-Überblick, Installation XAMPP, Workbench, phpMyAdmin | ✅ |
| **2** | [Konfiguration & Datenimport](./Lernportfolio/2.Tag/README.md) | my.ini, Schema/Dump/CSV-Import | ✅ |
| **3** | [Tabellentypen & Transaktionen](./Lernportfolio/3.Tag/README.md) | MyISAM, InnoDB, Locking, Transaktionen | ✅ |
| **4** | [Datenbanksicherheit](./Lernportfolio/4.Tag/README.md) | Authentifizierung, Zugriffskontrolle, Härtung | ✅ |
| **5** | [Zugriffssystem (LB1)](./Lernportfolio/5.Tag/README.md) | **LB1 (20%)**: Autorisierung, DCL, Rollen | ✅ |
| **6** | [Server-Administration](./Lernportfolio/6.Tag/README.md) | Admin-Tools, Logging, Optimierung, Backup | ✅ |
| **7** | [Datenbank testen](./Lernportfolio/7.Tag/README.md) | Testing, Performance, Bulk-Import | ✅ |
| **8** | [Weiterarbeit LB3](./Lernportfolio/8.Tag/README.md) | **LB2 (30%)**: Praxisarbeit Vorbereitung | ✅ |
| **9** | [LB3: Praxisarbeit MS B](./Lernportfolio/LB3-Praxisarbeit/README.md) | **LB3 (50%)**: Lokale DB-Migration | 🔄 |
| **10** | [LB3: Praxisarbeit MS C/D](./Lernportfolio/LB3-Praxisarbeit/README.md) | Cloud-Migration, Testing, Go-Live | 🔄 |

---

## 📖 Detaillierte Lernziele

- **[Lernziele LB1](./Lernziele_LB1.md)** — Tag 1–5 (Installation, Konfiguration, Sicherheit)
- **[Lernziele LB2](./Lernziele_LB2.md)** — Tag 4–7 (Administration, Testing, Betrieb)

---

## 🎓 Beurteilungen

| LB | Gewicht | Datum | Themen |
|----|---------|-------|--------|
| **LB1** | 20% | 09.06.26 | Tag 1–5: Installation, Konfiguration, Sicherheit |
| **LB2** | 30% | 23.06.26 | Tag 4–7: Administration, Testing |
| **[LB3](./Lernportfolio/LB3-Praxisarbeit/README.md)** | 50% | 07.07.26 | Praxisarbeit: Hostel-DB-Migration (lokal + Cloud) |

---

## 📚 Weitere Ressourcen

- **[Checkpoints](./Lernportfolio/Checkpoints/README.md)** — Selbstkontrolle pro Tag
- **[Literatur & Links](./Literatur.md)** — Referenzen und Dokumentationen
- **[Prompts](./Lernportfolio/Prompts.md)** — KI-Prompts für Lernunterstützung

---

## 🛠️ Technologie-Stack

| Komponente | Werkzeug | Version |
|-----------|----------|---------|
| **RDBMS (lokal)** | MariaDB / MySQL | 10.4.x |
| **RDBMS (Cloud)** | AWS RDS | MariaDB 10.6 |
| **GUI-Client** | MySQL Workbench | 8.x |
| **Web-Client** | phpMyAdmin | 5.x |
| **Server-Stack** | XAMPP | 7.4+ |

---

## 📊 Portfolio-Struktur

```
M141/
├── README.md                           (Diese Datei)
├── Lernziele_LB1.md
├── Lernziele_LB2.md
├── Literatur.md
├── LICENSE.md
└── Lernportfolio/
    ├── README.md
    ├── Prompts.md
    ├── 1.Tag/
    │   ├── README.md
    │   └── Checkpoint.md
    ├── 2.Tag/
    │   ├── README.md
    │   └── Checkpoint.md
    ├── ... (3–8. Tag analog)
    ├── Checkpoints/
    │   └── README.md
    └── LB3-Praxisarbeit/
        ├── README.md
        └── (DDL, DCL, Scripts, Demo)
```

---

## 🎯 Lernansatz

Dieses Modul folgt dem **Selbst-Lern-Zyklus**:
- **Learn:** Konzepte verstehen (Theorie)
- **Reflect:** Wissen überprüfen (Checkpoints)
- **Train DIY:** Praktisch anwenden (Übungen mit DBMS)
- **Demo:** Ergebnis präsentieren (Praxisarbeit)

---

[📖 Zur Portfolio-Übersicht](./Lernportfolio/README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

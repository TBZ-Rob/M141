# 🗄️ Tag 1 – Installation

![Status](https://img.shields.io/badge/Status-Abgeschlossen-green)
![Durchgeführt](https://img.shields.io/badge/Durchgeführt-12.05.2026-blue)
![Zeitaufwand](https://img.shields.io/badge/Zeitaufwand-~10min-lightgrey)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

> 💬 **Claude Prompt für dieses File:**
> *„Analysiere das ganze Repo, aktualisiere jedes Diagramm oder Darstellung auf den neusten Stand und füge bei neuen Seiten hinzu."*

---

### 🔧 XAMPP – Was ist das und warum?

XAMPP ist ein kostenloses Software-Bundle, das **Apache**, **MySQL/MariaDB** und **phpMyAdmin** in einer Installation bündelt. Anstatt jeden Dienst einzeln zu installieren und zu konfigurieren, läuft mit XAMPP alles mit wenigen Klicks.

**Warum XAMPP statt MySQL Workbench?**
Der Lehrer bevorzugt einen klassischeren, eher altmodischen Ansatz. XAMPP mit phpMyAdmin im Browser ist einfacher zugänglich und benötigt keine separate GUI-Installation.

**Wichtig bei der Installation:**
XAMPP sollte nach `C:\xampp` installiert werden und **nicht** nach `C:\Program Files`. Der Grund: Windows UAC (User Account Control) schränkt Schreibrechte in `Program Files` ein, was zu Fehlfunktionen führen kann.

---

### ⚙️ Dienste starten

Nach der Installation werden im **XAMPP Control Panel** zwei Dienste gestartet:

| Dienst | Funktion | Port |
|--------|----------|------|
| **Apache** | Webserver – stellt phpMyAdmin im Browser bereit | 80 |
| **MySQL** | Datenbankserver (MariaDB) | 3306 |

Sobald beide Dienste grün leuchten, ist phpMyAdmin unter `http://localhost/phpmyadmin` erreichbar.

---

### 🌐 phpMyAdmin

phpMyAdmin ist eine browserbasierte Oberfläche zur Verwaltung von MySQL/MariaDB-Datenbanken. Damit lassen sich Datenbanken erstellen, Tabellen verwalten, SQL-Befehle ausführen und Daten importieren/exportieren – alles ohne Kommandozeile.

**Warum phpMyAdmin?**
Im Vergleich zu MySQL Workbench ist phpMyAdmin leichtgewichtiger, läuft direkt im Browser und ist in der Schulumgebung weit verbreitet.

![phpMyAdmin erreichbar](./screenshots/1t_phpmyadmin-erreichbar.png)

---

### 🖥️ GitHub Repository & Lernportfolio

Da die Installation selbst nur ca. 10 Minuten dauerte (bekannte Grundlagen), wurde der Fokus dieses Tages auf den **Aufbau des GitHub-Repositories** gelegt.

**Was wurde aufgesetzt:**
- Ordnerstruktur für das gesamte Modul (Lernportfolio, Tage, Checkpoints)
- Einheitliches Design mit Badges, Navigation und Footer
- **Filesystem MCP Server** konfiguriert → Claude AI kann direkt auf lokale Dateien zugreifen und diese bearbeiten

**Was ist der Filesystem MCP Server?**
MCP (Model Context Protocol) ist ein Protokoll von Anthropic, das es Claude ermöglicht, über eine Konfigurationsdatei (`claude_desktop_config.json`) auf lokale Verzeichnisse zuzugreifen. Damit kann Claude Dateien lesen, erstellen und bearbeiten – ohne dass Inhalte manuell kopiert werden müssen.

---

### 💡 Erkenntnisse

Die Installation war reibungslos – XAMPP ist eine bewährte Lösung für lokale Entwicklungsumgebungen. Neu war die Einrichtung des **Filesystem MCP Servers**, der die Zusammenarbeit mit Claude AI erheblich vereinfacht. Die Konfiguration erforderte eine korrekte JSON-Struktur und Node.js als Voraussetzung.

---

### ✅ [Checkpoint](./Checkpoint.md)

| Ziel | Status |
|------|--------|
| XAMPP installiert | ✅ |
| Apache gestartet | ✅ |
| MySQL gestartet | ✅ |
| phpMyAdmin erreichbar | ✅ |
| GitHub Repository aufgesetzt | ✅ |
| Lernportfolio-Struktur erstellt | ✅ |
| Filesystem MCP Server konfiguriert | ✅ |

---

| [🏠 Übersicht](../README.md) | [➡️ Tag 2](../2.Tag/README.md) |
|---|---|

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

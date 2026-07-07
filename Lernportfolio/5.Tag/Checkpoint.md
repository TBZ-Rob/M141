# ✅ Checkpoint – 5. Tag

![Modul](https://img.shields.io/badge/Modul-M141-blue)
![Tag](https://img.shields.io/badge/Tag-5-orange)
![Autor](https://img.shields.io/badge/Autor-Robin%20Nydegger-lightgrey)

[⬅️ Tag 5](./README.md) · [🏠 Übersicht](../README.md)

Lösungen zum Checkpoint **Datenbank-Sicherheit / Zugriffssystem**.

---

## 🔘 Multiple Choice

| # | Frage | Antwort |
|---|-------|---------|
| 1 | Bedeutung von „Authentifizierung" bei einem DB-Server | ✅ Antwort auf die Frage: **Wer?** · ✅ **Identitätsprüfung** |
| 2 | Wann werden Änderungen im Zugriffssystem wirksam? | ✅ Nach `FLUSH PRIVILEGES` · ✅ Nach Neustart des DB-Servers |
| 3 | Was bewirkt `GRANT ... ON ... TO ...`? | ✅ **Privileg(ien) erteilen** · ✅ **User erstellen**, falls noch nicht vorhanden |
| 4 | Befehl zur Kontrolle der Zugriffsrechte? | ✅ `SHOW GRANTS FOR ...;` |
| 5 | Die zwei wichtigsten DCL-Befehle? | ✅ **GRANT** · ✅ **REVOKE** |
| 6 | Was ist nötig, damit User „meier" keinen Zugang mehr hat? | ✅ `DELETE FROM user WHERE user = 'meier';` und `FLUSH PRIVILEGES;` · ✅ In **allen** Systemtabellen für diesen Benutzer jedes Privileg auf „N" setzen |

---

## ✏️ Offene Fragen

**7. Erklären Sie den Begriff „Autorisierung" im Zusammenhang mit einem DB-Server.**

Autorisierung ist die **zweite Phase** der Zugangskontrolle (nach der Authentifizierung). Sie prüft bei **jedem einzelnen SQL-Befehl**, ob der bereits angemeldete Benutzer die nötigen **Privilegien** besitzt, um die gewünschte Aktion auszuführen (z.B. SELECT, INSERT, DELETE). Die Rechte können global, auf DB-, Tabellen- oder Spaltenebene vergeben werden.

**8. Wann wird das Schlüsselwort `IDENTIFIED BY` verwendet?**

`IDENTIFIED BY` wird bei `CREATE USER` oder `GRANT` verwendet, um **gleichzeitig ein Passwort** für den Benutzer zu setzen. Beispiel: `GRANT ALL ON db.* TO user@host IDENTIFIED BY 'Passw0rt';` – erstellt den User (falls nötig) und setzt das Passwort in einem Befehl.

**9. Ergänzen Sie `REVOKE ... ON ... FROM ...;` mit eigenen Angaben.**

```sql
REVOKE INSERT, UPDATE, DELETE ON hotel.* FROM hotel_user@localhost;
```

Entzieht dem Benutzer `hotel_user` die Schreibrechte auf die Datenbank `hotel` – er behält nur noch `SELECT` (falls vorher separat vergeben).

**10. Beschreiben Sie den Begriff der MySQL-Testdatenbank.**

Die Testdatenbank (`test`) wird bei manchen MySQL/MariaDB-Installationen standardmässig angelegt. Sie ist für **jeden Benutzer** zugänglich – auch ohne explizite Rechte. Im Produktivbetrieb sollte sie **gelöscht** werden (`DROP DATABASE test;`), da sie ein Sicherheitsrisiko darstellt.

**11. Passwort von Benutzer Meier auf „abc123" ändern?**

```sql
SET PASSWORD FOR 'meier'@'localhost' = PASSWORD('abc123');
FLUSH PRIVILEGES;
```

Alternativ (neuere MariaDB-Versionen): `ALTER USER 'meier'@'localhost' IDENTIFIED BY 'abc123';`

**12. Erklärung für die Fehlermeldung bei `GRANT USAGE ON *.* TO abc IDENTIFIED BY 'a12';`**

Die Fehlermeldung `Access denied for user: '@127.0.0.1'` zeigt, dass der **ausführende Benutzer** (leer = anonymer User von 127.0.0.1) selbst **keine Berechtigung** hat, `GRANT`-Befehle auszuführen. Man muss als `root` oder als Benutzer mit `GRANT OPTION` eingeloggt sein.

**13. Korrigieren Sie: `REVOKE ALL FROM ''@localhost;`**

```sql
REVOKE ALL PRIVILEGES ON *.* FROM ''@localhost;
```

Es fehlt `PRIVILEGES` und die Angabe des Geltungsbereichs (`ON *.*`). Die korrekte Syntax ist immer `REVOKE ... ON ... FROM ...`.

---

[⬅️ Tag 5](./README.md) · [🏠 Übersicht](../README.md)

---

$\textcolor{#8b949e}{\text{Hinweis: Diagramme, Rechtschreibung und Repo-Struktur wurden mit }} \textcolor{#D4622A}{\text{Claude AI Pro}} \textcolor{#8b949e}{\text{ generiert und von mir überarbeitet.}}$

<a href="../Prompts.md" style="color:#D4622A;">Prompts</a>

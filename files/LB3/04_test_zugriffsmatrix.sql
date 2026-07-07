-- ============================================================
-- LB3: Backpacker DB – Testscript (Zugriffsmatrix + Konsistenz)
-- Robin Nydegger, PE24c
-- ============================================================
-- Dieses Script wird auch für die Demo beim Lehrer verwendet.
-- Es testet alle 3 User gegen die Zugriffsmatrix.
-- ============================================================

-- ############################################################
-- TEIL 1: DATENKONSISTENZ
-- ############################################################

USE backpacker_robin;

SELECT '========================================' AS '';
SELECT 'TEIL 1: DATENKONSISTENZ' AS Test;
SELECT '========================================' AS '';

-- 1.1 Zeilenzählung
SELECT 'Zeilenzählung' AS Test;
SELECT 'tbl_land' AS Tabelle, COUNT(*) AS Anzahl FROM tbl_land
UNION ALL SELECT 'tbl_leistung', COUNT(*) FROM tbl_leistung
UNION ALL SELECT 'tbl_personen', COUNT(*) FROM tbl_personen
UNION ALL SELECT 'tbl_benutzer', COUNT(*) FROM tbl_benutzer
UNION ALL SELECT 'tbl_buchung', COUNT(*) FROM tbl_buchung
UNION ALL SELECT 'tbl_positionen', COUNT(*) FROM tbl_positionen;

-- 1.2 Engine-Check
SELECT 'Engine-Check' AS Test;
SELECT TABLE_NAME, ENGINE, TABLE_COLLATION
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = 'backpacker_robin'
ORDER BY TABLE_NAME;

-- 1.3 FK-Constraints vorhanden?
SELECT 'FK-Constraints' AS Test;
SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'backpacker_robin'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

-- 1.4 Verwaiste FK-Werte (sollte alles 0 sein)
SELECT 'Verwaiste FKs' AS Test;
SELECT 'buchung→personen' AS Beziehung,
  COUNT(*) AS Verwaiste
  FROM tbl_buchung b
  LEFT JOIN tbl_personen p ON b.Personen_FS = p.Personen_ID
  WHERE b.Personen_FS IS NOT NULL AND p.Personen_ID IS NULL
UNION ALL
SELECT 'buchung→land',
  COUNT(*)
  FROM tbl_buchung b
  LEFT JOIN tbl_land l ON b.Land_FS = l.Land_ID
  WHERE b.Land_FS IS NOT NULL AND l.Land_ID IS NULL
UNION ALL
SELECT 'positionen→buchung',
  COUNT(*)
  FROM tbl_positionen po
  LEFT JOIN tbl_buchung b ON po.Buchungs_FS = b.Buchungs_ID
  WHERE po.Buchungs_FS IS NOT NULL AND b.Buchungs_ID IS NULL
UNION ALL
SELECT 'positionen→leistung',
  COUNT(*)
  FROM tbl_positionen po
  LEFT JOIN tbl_leistung l ON po.Leistung_FS = l.LeistungID
  WHERE po.Leistung_FS IS NOT NULL AND l.LeistungID IS NULL;

-- 1.5 Stichprobe: JOIN über alle Tabellen
SELECT 'Stichprobe JOIN' AS Test;
SELECT
  p.Vorname, p.Name AS Gast,
  b.Ankunft, b.Abreise,
  l.Land,
  po.Leistung_Text, po.Preis, po.Anzahl,
  be.Benutzername AS ErfasstVon
FROM tbl_positionen po
JOIN tbl_buchung b ON po.Buchungs_FS = b.Buchungs_ID
JOIN tbl_personen p ON b.Personen_FS = p.Personen_ID
LEFT JOIN tbl_land l ON b.Land_FS = l.Land_ID
LEFT JOIN tbl_benutzer be ON po.Benutzer_FS = be.Benutzer_ID
LEFT JOIN tbl_leistung le ON po.Leistung_FS = le.LeistungID
LIMIT 5;


-- ############################################################
-- TEIL 2: BENUTZER-ROLLE TESTEN
-- (Als bp_benutzer einloggen und diese Befehle ausführen)
-- ############################################################

SELECT '========================================' AS '';
SELECT 'TEIL 2: BENUTZER-ROLLE' AS Test;
SELECT '========================================' AS '';
SELECT 'Die folgenden Tests manuell als bp_benutzer ausführen:' AS Hinweis;

-- 2.1 SELECT auf tbl_personen → SOLL: OK
-- SELECT * FROM tbl_personen LIMIT 3;

-- 2.2 UPDATE auf tbl_personen → SOLL: OK
-- UPDATE tbl_personen SET Telefon = '000-TEST' WHERE Personen_ID = 1;
-- SELECT Telefon FROM tbl_personen WHERE Personen_ID = 1;
-- UPDATE tbl_personen SET Telefon = NULL WHERE Personen_ID = 1;

-- 2.3 INSERT auf tbl_personen → SOLL: FEHLER (kein INSERT-Recht)
-- INSERT INTO tbl_personen (Vorname, Name) VALUES ('Test', 'Fehler');

-- 2.4 DELETE auf tbl_personen → SOLL: FEHLER
-- DELETE FROM tbl_personen WHERE Personen_ID = 1;

-- 2.5 SELECT Password von tbl_benutzer → SOLL: FEHLER (kein Zugriff auf Password)
-- SELECT Password FROM tbl_benutzer LIMIT 1;

-- 2.6 SELECT deaktiviert von tbl_benutzer → SOLL: OK
-- SELECT Benutzer_ID, Benutzername, deaktiviert FROM tbl_benutzer LIMIT 3;

-- 2.7 UPDATE deaktiviert → SOLL: FEHLER (nur SELECT erlaubt)
-- UPDATE tbl_benutzer SET deaktiviert = '2026-01-01' WHERE Benutzer_ID = 1;

-- 2.8 CRUD auf tbl_buchung → SOLL: alles OK
-- SELECT * FROM tbl_buchung LIMIT 3;
-- INSERT INTO tbl_buchung (Personen_FS, Ankunft, Abreise) VALUES (1, NOW(), NOW());
-- DELETE FROM tbl_buchung WHERE Buchungs_ID = (SELECT MAX(Buchungs_ID) FROM tbl_buchung);

-- 2.9 SELECT auf tbl_land → SOLL: OK
-- SELECT * FROM tbl_land LIMIT 3;

-- 2.10 INSERT auf tbl_land → SOLL: FEHLER
-- INSERT INTO tbl_land (Land_ID, Land) VALUES (999, 'Testland');


-- ############################################################
-- TEIL 3: MANAGEMENT-ROLLE TESTEN
-- (Als bp_management einloggen und diese Befehle ausführen)
-- ############################################################

SELECT '========================================' AS '';
SELECT 'TEIL 3: MANAGEMENT-ROLLE' AS Test;
SELECT '========================================' AS '';
SELECT 'Die folgenden Tests manuell als bp_management ausführen:' AS Hinweis;

-- 3.1 SELECT auf tbl_buchung → SOLL: OK
-- SELECT * FROM tbl_buchung LIMIT 3;

-- 3.2 INSERT auf tbl_buchung → SOLL: FEHLER (nur SELECT)
-- INSERT INTO tbl_buchung (Personen_FS, Ankunft) VALUES (1, NOW());

-- 3.3 CRUD auf tbl_personen → SOLL: alles OK
-- SELECT * FROM tbl_personen LIMIT 3;
-- INSERT INTO tbl_personen (Vorname, Name) VALUES ('Mgmt', 'Test');
-- DELETE FROM tbl_personen WHERE Vorname = 'Mgmt' AND Name = 'Test';

-- 3.4 CRUD auf tbl_benutzer → SOLL: alles OK (inkl. Password!)
-- SELECT Benutzer_ID, Benutzername, Password FROM tbl_benutzer LIMIT 3;

-- 3.5 CRUD auf tbl_land → SOLL: alles OK
-- INSERT INTO tbl_land (Land_ID, Land) VALUES (999, 'Testland');
-- DELETE FROM tbl_land WHERE Land_ID = 999;


-- ############################################################
-- TEIL 4: ADMIN TESTEN
-- ############################################################

SELECT '========================================' AS '';
SELECT 'TEIL 4: ADMIN' AS Test;
SELECT '========================================' AS '';
SELECT 'Als bp_admin: Vollzugriff auf alles' AS Hinweis;

-- 4.1 Alle Tabellen → SOLL: volles CRUD
-- 4.2 GRANT-Recht → SOLL: OK
-- SHOW GRANTS FOR CURRENT_USER;

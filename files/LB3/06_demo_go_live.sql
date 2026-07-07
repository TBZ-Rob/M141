-- ============================================================
-- LB3: Demo-Script für Go-Live auf AWS RDS
-- Robin Nydegger, PE24c
-- ============================================================
-- Dieses Script zeigt alle 3 Benutzer in Aktion
-- und dokumentiert die erfolgreiche Migration.
-- ============================================================

-- ############################################################
-- TEIL 1: AS BP_ADMIN – Vollzugriff Check
-- ############################################################

-- Befehl 1.1: Datenzählung prüfen
SELECT 'ADMIN: Datenzählung' AS Demo;
SELECT 
  (SELECT COUNT(*) FROM tbl_land) AS land_count,
  (SELECT COUNT(*) FROM tbl_personen) AS personen_count,
  (SELECT COUNT(*) FROM tbl_buchung) AS buchung_count,
  (SELECT COUNT(*) FROM tbl_positionen) AS positionen_count;

-- Befehl 1.2: GRANT-Rechte prüfen (auf sich selbst)
SELECT 'ADMIN: Grants' AS Demo;
SHOW GRANTS FOR 'bp_admin'@'%';

-- Befehl 1.3: Beispieldaten lesen
SELECT 'ADMIN: Sample Gäste' AS Demo;
SELECT Personen_ID, Vorname, Name, Ort 
FROM tbl_personen LIMIT 5;


-- ############################################################
-- TEIL 2: AS BP_BENUTZER – Limitierter Zugriff
-- ############################################################

-- Befehl 2.1: SELECT auf tbl_land (SOLL: OK)
SELECT 'BENUTZER: SELECT tbl_land' AS Demo;
SELECT Land_ID, Land FROM tbl_land LIMIT 5;

-- Befehl 2.2: SELECT auf tbl_buchung (SOLL: OK)
SELECT 'BENUTZER: SELECT tbl_buchung' AS Demo;
SELECT Buchungs_ID, Personen_FS, Ankunft, Abreise 
FROM tbl_buchung LIMIT 5;

-- Befehl 2.3: Versuche Password zu lesen (SOLL: FEHLER 1143)
-- SELECT 'BENUTZER: Versuche Password zu lesen (SOLL blockiert)' AS Demo;
-- SELECT Password FROM tbl_benutzer LIMIT 1;
-- → Error: SELECT command denied for column 'Password'

-- Befehl 2.4: UPDATE auf tbl_personen (SOLL: OK)
SELECT 'BENUTZER: UPDATE tbl_personen (Test)' AS Demo;
UPDATE tbl_personen SET Telefon = '+41-TEST-DEMO' WHERE Personen_ID = 1;
SELECT Personen_ID, Telefon FROM tbl_personen WHERE Personen_ID = 1;
-- Rollback für Demo:
UPDATE tbl_personen SET Telefon = NULL WHERE Personen_ID = 1;

-- Befehl 2.5: Versuche DELETE auf tbl_personen (SOLL: FEHLER – kein DELETE-Recht)
-- DELETE FROM tbl_personen WHERE Personen_ID = 999;
-- → Error: DELETE command denied


-- ############################################################
-- TEIL 3: AS BP_MANAGEMENT – Manager-Zugriff
-- ############################################################

-- Befehl 3.1: SELECT auf tbl_buchung (SOLL: OK)
SELECT 'MANAGEMENT: SELECT tbl_buchung' AS Demo;
SELECT Buchungs_ID, Personen_FS, Ankunft 
FROM tbl_buchung LIMIT 5;

-- Befehl 3.2: Versuche INSERT auf tbl_buchung (SOLL: FEHLER – nur SELECT)
-- INSERT INTO tbl_buchung (Personen_FS, Ankunft) VALUES (1, NOW());
-- → Error: INSERT command denied

-- Befehl 3.3: CRUD auf tbl_personen (SOLL: alles OK)
SELECT 'MANAGEMENT: SELECT tbl_personen' AS Demo;
SELECT Personen_ID, Vorname, Name FROM tbl_personen LIMIT 5;

-- Befehl 3.4: CRUD auf tbl_land (SOLL: alles OK, auch Password sichtbar!)
SELECT 'MANAGEMENT: CRUD auf tbl_benutzer (inkl. Password)' AS Demo;
SELECT Benutzer_ID, Benutzername, Password FROM tbl_benutzer LIMIT 3;

-- Befehl 3.5: Versuche INSERT auf tbl_benutzer (SOLL: OK)
SELECT 'MANAGEMENT: INSERT tbl_benutzer (Test)' AS Demo;
INSERT INTO tbl_benutzer (Benutzername, Vorname, Name) 
VALUES ('testuser', 'Test', 'Demo');
SELECT Benutzer_ID, Benutzername FROM tbl_benutzer WHERE Benutzername = 'testuser';
-- Cleanup:
DELETE FROM tbl_benutzer WHERE Benutzername = 'testuser';


-- ############################################################
-- TEIL 4: MIGRATION-VALIDIERUNG
-- ############################################################

SELECT 'MIGRATION-CHECK: FK-Constraints' AS Demo;
SELECT CONSTRAINT_NAME, TABLE_NAME, REFERENCED_TABLE_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA = 'backpacker_robin'
  AND REFERENCED_TABLE_NAME IS NOT NULL;

SELECT 'MIGRATION-CHECK: Verwaiste FKs (sollte 0 sein)' AS Demo;
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
  WHERE po.Buchungs_FS IS NOT NULL AND b.Buchungs_ID IS NULL;

SELECT '=====================================' AS '';
SELECT 'DEMO ABGESCHLOSSEN!' AS Status;
SELECT '=====================================' AS '';

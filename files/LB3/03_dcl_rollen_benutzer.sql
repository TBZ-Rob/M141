-- ============================================================
-- LB3: Backpacker DB – DCL (Rollen & Benutzer)
-- Robin Nydegger, PE24c
-- ============================================================
-- Gemäss Zugriffsmatrix aus der Aufgabenstellung:
--
-- BENUTZER-Rolle:
--   tbl_personen:            SELECT, UPDATE
--   tbl_benutzer.Password:   KEIN Zugriff
--   tbl_benutzer.deaktiviert: nur SELECT
--   tbl_benutzer (rest):     SELECT, INSERT, UPDATE
--   tbl_buchung:             SELECT, INSERT, UPDATE, DELETE
--   tbl_positionen:          SELECT, INSERT, UPDATE, DELETE
--   tbl_land:                SELECT
--   tbl_leistung:            SELECT
--
-- MANAGEMENT-Rolle:
--   tbl_positionen, tbl_buchung: nur SELECT
--   alle anderen Tabellen:       SELECT, INSERT, UPDATE, DELETE
-- ============================================================

USE backpacker_robin;

-- ============================================================
-- 1. Alte Rollen & User aufräumen (idempotent)
-- ============================================================
DROP ROLE IF EXISTS 'role_benutzer';
DROP ROLE IF EXISTS 'role_management';
DROP USER IF EXISTS 'bp_benutzer'@'%';
DROP USER IF EXISTS 'bp_management'@'%';
DROP USER IF EXISTS 'bp_admin'@'%';

-- ============================================================
-- 2. Rollen erstellen
-- ============================================================

CREATE ROLE 'role_benutzer';
CREATE ROLE 'role_management';

-- ============================================================
-- 3. BENUTZER-Rolle: Rechte gemäss Zugriffsmatrix
-- ============================================================

-- tbl_personen: SELECT + UPDATE (kein INSERT, kein DELETE)
GRANT SELECT, UPDATE ON backpacker_robin.tbl_personen TO 'role_benutzer';

-- tbl_benutzer: Spaltenbasiert!
--   Password      → KEIN Zugriff
--   deaktiviert   → nur SELECT
--   Rest          → SELECT, INSERT, UPDATE (kein DELETE)
GRANT SELECT (Benutzer_ID, Benutzername, Vorname, Name, Benutzergruppe, erfasst, deaktiviert, aktiv)
  ON backpacker_robin.tbl_benutzer TO 'role_benutzer';
GRANT INSERT (Benutzer_ID, Benutzername, Vorname, Name, Benutzergruppe, aktiv)
  ON backpacker_robin.tbl_benutzer TO 'role_benutzer';
GRANT UPDATE (Benutzer_ID, Benutzername, Vorname, Name, Benutzergruppe, aktiv)
  ON backpacker_robin.tbl_benutzer TO 'role_benutzer';

-- tbl_buchung + tbl_positionen: volles CRUD
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_buchung TO 'role_benutzer';
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_positionen TO 'role_benutzer';

-- tbl_land + tbl_leistung: nur SELECT
GRANT SELECT ON backpacker_robin.tbl_land TO 'role_benutzer';
GRANT SELECT ON backpacker_robin.tbl_leistung TO 'role_benutzer';

-- ============================================================
-- 4. MANAGEMENT-Rolle: Rechte gemäss Zugriffsmatrix
-- ============================================================

-- tbl_positionen + tbl_buchung: nur SELECT
GRANT SELECT ON backpacker_robin.tbl_positionen TO 'role_management';
GRANT SELECT ON backpacker_robin.tbl_buchung TO 'role_management';

-- Alle anderen Tabellen: volles CRUD
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_personen TO 'role_management';
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_benutzer TO 'role_management';
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_land TO 'role_management';
GRANT SELECT, INSERT, UPDATE, DELETE ON backpacker_robin.tbl_leistung TO 'role_management';

-- ============================================================
-- 5. Benutzer erstellen & Rollen zuweisen
-- ============================================================

CREATE USER 'bp_benutzer'@'%' IDENTIFIED BY 'Benutzer_2026!';
CREATE USER 'bp_management'@'%' IDENTIFIED BY 'Management_2026!';
CREATE USER 'bp_admin'@'%' IDENTIFIED BY 'Admin_2026!';

-- Admin: Vollzugriff auf backpacker_robin
GRANT ALL PRIVILEGES ON backpacker_robin.* TO 'bp_admin'@'%' WITH GRANT OPTION;

-- Rollen zuweisen
GRANT 'role_benutzer' TO 'bp_benutzer'@'%';
GRANT 'role_management' TO 'bp_management'@'%';

-- Default-Rollen setzen (automatisch aktiv beim Login)
SET DEFAULT ROLE 'role_benutzer' FOR 'bp_benutzer'@'%';
SET DEFAULT ROLE 'role_management' FOR 'bp_management'@'%';

FLUSH PRIVILEGES;

-- ============================================================
-- 6. Kontrolle
-- ============================================================
SELECT '--- Benutzer-Rolle ---' AS Info;
SHOW GRANTS FOR 'role_benutzer';

SELECT '--- Management-Rolle ---' AS Info;
SHOW GRANTS FOR 'role_management';

SELECT '--- bp_benutzer ---' AS Info;
SHOW GRANTS FOR 'bp_benutzer'@'%';

SELECT '--- bp_management ---' AS Info;
SHOW GRANTS FOR 'bp_management'@'%';

SELECT '--- bp_admin ---' AS Info;
SHOW GRANTS FOR 'bp_admin'@'%';

SELECT 'DCL erfolgreich eingerichtet!' AS Status;

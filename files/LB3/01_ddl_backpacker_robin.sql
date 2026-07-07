-- ============================================================
-- LB3: Backpacker DB – Bereinigte DDL
-- Robin Nydegger, PE24c
-- ============================================================
-- Fixes gegenüber Original:
--   1. MyISAM → InnoDB
--   2. latin1 → utf8mb4
--   3. tbl_land: PRIMARY KEY hinzugefügt
--   4. TEXT-Spalten wo sinnvoll → VARCHAR
--   5. FK-Constraints auf alle Beziehungen
--   6. Indizes auf Fremdschlüssel
-- ============================================================

DROP DATABASE IF EXISTS backpacker_robin;
CREATE DATABASE backpacker_robin
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_general_ci;

USE backpacker_robin;

-- ============================================================
-- 1. Stammdaten-Tabellen (keine FK-Abhängigkeiten)
-- ============================================================

CREATE TABLE tbl_land (
  Land_ID     INT(11)      NOT NULL,
  Land        VARCHAR(100) NOT NULL,
  PRIMARY KEY (Land_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Ländercodes';

CREATE TABLE tbl_leistung (
  LeistungID    INT(11)     NOT NULL,
  Beschreibung  VARCHAR(70) DEFAULT NULL,
  PRIMARY KEY (LeistungID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Leistungsarten';

CREATE TABLE tbl_personen (
  Personen_ID   INT(11)      NOT NULL AUTO_INCREMENT,
  Titel         VARCHAR(20)  DEFAULT NULL,
  Vorname       VARCHAR(100) DEFAULT NULL,
  Name          VARCHAR(100) DEFAULT NULL,
  Strasse       VARCHAR(150) DEFAULT NULL,
  PLZ           VARCHAR(20)  DEFAULT NULL,
  Ort           VARCHAR(100) DEFAULT NULL,
  Anrede        VARCHAR(20)  DEFAULT NULL,
  Telefon       VARCHAR(30)  DEFAULT NULL,
  erfasst       DATETIME     DEFAULT NULL,
  Sprache       VARCHAR(10)  DEFAULT NULL,
  PRIMARY KEY (Personen_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Gäste';

CREATE TABLE tbl_benutzer (
  Benutzer_ID     INT(11)      NOT NULL AUTO_INCREMENT,
  Benutzername    VARCHAR(20)  NOT NULL DEFAULT '',
  Password        VARCHAR(255) DEFAULT NULL,
  Vorname         VARCHAR(20)  DEFAULT NULL,
  Name            VARCHAR(100) DEFAULT NULL,
  Benutzergruppe  TINYINT(4)   DEFAULT 1,
  erfasst         TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  deaktiviert     DATE         DEFAULT '1000-01-01',
  aktiv           TINYINT(4)   DEFAULT 1,
  PRIMARY KEY (Benutzer_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Mitarbeiter';

-- ============================================================
-- 2. Tabellen mit Fremdschlüsseln
-- ============================================================

CREATE TABLE tbl_buchung (
  Buchungs_ID   INT(11)   NOT NULL AUTO_INCREMENT,
  Personen_FS   INT(11)   DEFAULT NULL,
  Ankunft       DATETIME  DEFAULT NULL,
  Abreise       DATETIME  DEFAULT NULL,
  Land_FS       INT(11)   DEFAULT NULL,
  PRIMARY KEY (Buchungs_ID),
  INDEX idx_personen_fs (Personen_FS),
  INDEX idx_land_fs (Land_FS),
  CONSTRAINT fk_buchung_person
    FOREIGN KEY (Personen_FS) REFERENCES tbl_personen(Personen_ID)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CONSTRAINT fk_buchung_land
    FOREIGN KEY (Land_FS) REFERENCES tbl_land(Land_ID)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Buchungszeilen';

CREATE TABLE tbl_positionen (
  Positions_ID    INT(11)       NOT NULL AUTO_INCREMENT,
  Buchungs_FS     INT(11)       DEFAULT NULL,
  Konto           INT(11)       NOT NULL DEFAULT 0,
  Anzahl          INT(11)       NOT NULL DEFAULT 0,
  Preis           DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  Rabatt          DECIMAL(4,2)  NOT NULL DEFAULT 0.00,
  Benutzer_FS     INT(11)       NOT NULL DEFAULT 0,
  erfasst         DATETIME      NOT NULL DEFAULT '2000-01-01 00:00:00',
  Leistung_Text   TEXT          NOT NULL,
  Leistung_FS     INT(11)       DEFAULT NULL,
  PRIMARY KEY (Positions_ID),
  INDEX idx_buchungs_fs (Buchungs_FS),
  INDEX idx_benutzer_fs (Benutzer_FS),
  INDEX idx_leistung_fs (Leistung_FS),
  CONSTRAINT fk_position_buchung
    FOREIGN KEY (Buchungs_FS) REFERENCES tbl_buchung(Buchungs_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT fk_position_benutzer
    FOREIGN KEY (Benutzer_FS) REFERENCES tbl_benutzer(Benutzer_ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT fk_position_leistung
    FOREIGN KEY (Leistung_FS) REFERENCES tbl_leistung(LeistungID)
    ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Buchungspositionen';

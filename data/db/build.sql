--
-- File generated with SQLiteStudio v3.2.1 on Wed Sep 23 14:28:38 2020
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: guild_config
CREATE TABLE guild_config (
    guildId         STRING (18) PRIMARY KEY,
    name            STRING      UNIQUE
                                NOT NULL,
    setTime         DATETIME    NOT NULL,
    setByUserId     STRING      NOT NULL,
    commandPrefixes STRING      NOT NULL
);


-- Table: notes
CREATE TABLE notes (
    Id       INTEGER  PRIMARY KEY AUTOINCREMENT,
    Time     DATETIME NOT NULL,
    UserId   STRING   NOT NULL,
    Notebook STRING   NOT NULL
                      DEFAULT Main,
    Text     TEXT     NOT NULL
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;

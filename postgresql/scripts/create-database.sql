-- Database: socrate

DROP DATABASE IF EXISTS socrate;

CREATE DATABASE socrate
    WITH
    OWNER = sigl2023
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;

COMMENT ON DATABASE socrate
    IS 'Database for socrate';
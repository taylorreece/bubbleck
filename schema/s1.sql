-- s1.sql

BEGIN;

ALTER TABLE sessions ADD COLUMN ipaddress text NOT NULL;

SELECT update_setting('schema','version','1');
COMMIT;

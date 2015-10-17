-- s1.sql

BEGIN;

ALTER TABLE sessions ADD COLUMN ipaddress text NOT NULL;

CREATE TABLE email_users (
	emailid		SERIAL PRIMARY KEY,
	usersid		INTEGER REFERENCES users(usersid),
	additional_to	TEXT,
	additional_cc	TEXT,
	additional_bcc	TEXT,
	subject		TEXT NOT NULL,
	body		TEXT NOT NULL,
	sent_at		TIMESTAMP,
	show_as_web_msg	BOOLEAN NOT NULL DEFAULT TRUE,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_email_users_updated_at BEFORE UPDATE ON email_users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
ALTER TABLE email_users OWNER TO mat;


SELECT update_setting('schema','version','1');
COMMIT;
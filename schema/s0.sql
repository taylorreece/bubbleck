-- s0.sql - Initial Database schema

BEGIN;
--
-- Function for updating updated_at columns; generic for all tables.
CREATE OR REPLACE FUNCTION update_updated_at_column()	
RETURNS TRIGGER AS $$
BEGIN
	NEW.updated_at = NOW();
	RETURN NEW;	
END;
$$ language 'plpgsql';

--
-- Settings table holds all site-config settings 
CREATE TABLE settings (
	settingsid	SERIAL PRIMARY KEY,
	category	TEXT NOT NULL,
	name		TEXT NOT NULL,
	value		TEXT NOT NULL,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_settings_updated_at BEFORE UPDATE ON settings FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
ALTER TABLE settings ADD UNIQUE (category, name);

--
-- Stores simple users data; login data, etc, will be in another table
CREATE TABLE users (
	usersid 	SERIAL PRIMARY KEY,
	email		TEXT NOT NULL UNIQUE,
	password	TEXT NOT NULL,
	name		TEXT NOT NULL,
	teachername	TEXT NOT NULL,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Stores Course data
CREATE TABLE courses (
	coursesid	SERIAL PRIMARY KEY,
	name		TEXT NOT NULL,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_courses_updated_at BEFORE UPDATE ON courses FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();


-- 
-- Pivot table between courses and users
CREATE TYPE course_role AS ENUM('own','edit','view');
CREATE TABLE courses_users (
	usersid		INTEGER REFERENCES users(usersid),
	coursesid	INTEGER REFERENCES courses(coursesid),
	role		course_role NOT NULL,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE courses_users ADD UNIQUE (usersid, coursesid);
CREATE TRIGGER update_courses_users_updated_at BEFORE UPDATE ON courses_users FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Exams, which are tied to courses
CREATE TABLE exams (
	examsid		SERIAL PRIMARY KEY,
	coursesid	INTEGER REFERENCES courses(coursesid),
	name		TEXT NOT NULL,
	layout		TEXT NOT NULL,
	answers		TEXT,
	show_directions	BOOLEAN NOT NULL DEFAULT TRUE,
	show_teachername BOOLEAN NOT NULL DEFAULT TRUE,
	show_points	BOOLEAN NOT NULL DEFAULT TRUE,
	show_coursename	BOOLEAN NOT NULL DEFAULT TRUE,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_exams_updated_at BEFORE UPDATE ON exams FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Exam results can be shared with others using special keys
CREATE TABLE examshares (
	examsharesid	SERIAL PRIMARY KEY,
	examsid		INTEGER REFERENCES exams(examsid),
	key		text,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_examshares_updated_at BEFORE UPDATE ON examshares FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Courses can have multiple sections
CREATE TABLE sections (
	sectionsid	SERIAL PRIMARY KEY,
	examsid		INTEGER REFERENCES exams(examsid),
	name		text NOT NULL,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_sections_updated_at BEFORE UPDATE ON sections FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Student exams are owned by a section, and by an exam
CREATE TABLE studentexams (
	studentexamsid	SERIAL PRIMARY KEY,
	examsid		INTEGER REFERENCES exams(examsid),
	sectionsid	INTEGER REFERENCES sections(sectionsid),
	answers		text,
	active		BOOLEAN NOT NULL DEFAULT TRUE,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TRIGGER update_studentexams_updated_at BEFORE UPDATE ON studentexams FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();

--
-- Keeps track of users' sessions.  Designed so that one user can have multiple sessions.
CREATE TABLE sessions (
	usersid		INTEGER REFERENCES users(usersid),
	sessionid	INTEGER NOT NULL,
	created_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	updated_at	TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
ALTER TABLE sessions ADD UNIQUE (usersid, sessionid);

-- This function returns true if a userid/sessionid pair exists, and false otherwise.
-- If true, it updates the updated_at timestamp.  This will be helpful later as a cron job will delete
-- sessions that haven't been touched in X time.
-- Note: as such, no updated_at function need exist.
CREATE OR REPLACE FUNCTION check_user_session(u INTEGER, s INTEGER)
RETURNS BOOLEAN AS $$
BEGIN
	IF EXISTS (SELECT 1 FROM sessions WHERE usersid=u AND sessionid=s) THEN
		UPDATE sessions SET updated_at=NOW() WHERE usersid=u AND sessionid=s;
		RETURN TRUE;
	END IF;
	RETURN FALSE;
END;
$$ LANGUAGE plpgsql;

-- 
-- Clears out old settings, creates new with given category,name,value
CREATE OR REPLACE FUNCTION update_setting(c TEXT, n TEXT, v TEXT)
RETURNS VOID AS $$
BEGIN
	IF EXISTS (SELECT 1 FROM settings WHERE category=c AND name=n) THEN
		UPDATE settings SET value=v WHERE category=c AND name=n;
		RETURN;	
	END IF;
	INSERT INTO settings (category,name,value) VALUES (c,n,v);
END;
$$ LANGUAGE plpgsql;

-- SET SCHEMA VERSION:
SELECT update_setting('schema','version','0');
COMMIT;

-- This file contains some useful SQL for use while doing development

-- clean all data in the database
TRUNCATE TABLE users_files;
TRUNCATE TABLE file_history;
TRUNCATE TABLE files;
TRUNCATE TABLE users;
-- ----------------------------------

-- Before a fresh install kill all tables
DROP TABLE IF EXISTS sessions;
DROP TABLE IF EXISTS users_files;
DROP TABLE IF EXISTS permissions;
DROP TABLE IF EXISTS files_history;
DROP TABLE IF EXISTS files;
DROP TABLE IF EXISTS users;
-- ----------------------------------
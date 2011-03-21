-- =======================================
-- Fresh install
-- =======================================
-- Create users table
CREATE TABLE users (
	username VARCHAR(255) PRIMARY KEY, 
	password_hash CHAR(40) NOT NULL, 
	quota BIGINT UNSIGNED,
	salt CHAR(32) NOT NULL) ENGINE = INNODB;

-- Create files table
CREATE TABLE files (
	file_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	client_path VARCHAR(4096) NOT NULL, 
	server_path VARCHAR(4096) NOT NULL, 
	version SMALLINT UNSIGNED,
	last_modified TIMESTAMP, 
	last_author VARCHAR(255), 
	directory BOOL DEFAULT 0, -- is the file a directory?
	size BIGINT UNSIGNED,
	checksum CHAR(40) NOT NULL,
	deleted BOOL DEFAULT 0
	) ENGINE = INNODB;

-- file history and version control
CREATE TABLE file_history (
	file_id BIGINT UNSIGNED, 
	version SMALLINT UNSIGNED,
	client_path VARCHAR(4096) NOT NULL, 
	server_path VARCHAR(4096) NOT NULL, 
	last_modified TIMESTAMP, 
	last_author VARCHAR(255), 
	directory BOOL DEFAULT 0, -- is the file a directory?
	size BIGINT UNSIGNED NOT NULL,
	checksum CHAR(32) NOT NULL,
	deleted BOOL DEFAULT 0,
	FOREIGN KEY (file_Id) REFERENCES files(file_id),
	PRIMARY KEY (file_id, version) ) ENGINE = INNODB;

-- Simple look up table for permissions
CREATE TABLE permissions (
	permission_level TINYINT UNSIGNED PRIMARY KEY,
	description VARCHAR(255) NOT NULL) ENGINE = INNODB;
	
-- Create users_files table to resolve the many-to-many relation between files and users
CREATE TABLE users_files(
	username VARCHAR(255) NOT NULL, 
	file_id BIGINT UNSIGNED NOT NULL,
	permission_level TINYINT UNSIGNED NOT NULL,
	FOREIGN KEY (username) REFERENCES users(username),
	FOREIGN KEY (file_id) REFERENCES files(file_id),
	FOREIGN KEY (permission_level) REFERENCES permissions(permission_level),
	PRIMARY KEY (username, file_id)) ENGINE = INNODB;

-- =======================================
-- Patches
-- =======================================

-- patch 1 - date: 2011-3-16 22:27--
START TRANSACTION;
ALTER TABLE users ADD COLUMN quota BIGINT UNSIGNED;
ALTER TABLE files ADD COLUMN directory BOOL;
ALTER TABLE files ADD COLUMN size BIGINT UNSIGNED;

ALTER TABLE files MODIFY COLUMN version SMALLINT UNSIGNED;

-- COLUMN renames to be consistent with coding standards, this will result in
-- the loss of data!
ALTER TABLE users_files DROP FOREIGN KEY users_files_ibfk_1; 
ALTER TABLE users_files DROP FOREIGN KEY users_files_ibfk_2; 
ALTER TABLE users_files DROP COLUMN fileID ;  
ALTER TABLE users_files ADD COLUMN file_id BIGINT UNSIGNED;
ALTER TABLE users_files DROP PRIMARY KEY;
ALTER TABLE users_files ADD PRIMARY KEY (username, file_id);
ALTER TABLE users_files ADD FOREIGN KEY (username) REFERENCES users(username);

ALTER TABLE files DROP FOREIGN KEY files_ibfk_1;  
ALTER TABLE files MODIFY COLUMN parent BIGINT UNSIGNED;
ALTER TABLE files DROP COLUMN fileID;
ALTER TABLE files ADD COLUMN file_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY;

ALTER TABLE files ADD FOREIGN KEY (parent) REFERENCES files(file_id);
ALTER TABLE users_files ADD FOREIGN KEY (file_id) REFERENCES files(file_id);

ALTER TABLE users DROP COLUMN passwordHash;
ALTER TABLE users ADD COLUMN password_hash CHAR(64) NOT NULL;
COMMIT;
-- END Patch 1 ---------------------------------------

-- Patch 2 - date: 2011-3-20 12:29 --
-- Simple look up table for permissions
CREATE TABLE permissions (
	permission_level TINYINT UNSIGNED PRIMARY KEY,
	description VARCHAR(255) NOT NULL) ENGINE = INNODB;

-- link to permissions table	
ALTER TABLE users_files ADD COLUMN permission_level TINYINT UNSIGNED NOT NULL;
ALTER TABLE users_files ADD FOREIGN KEY (permission_level) REFERENCES permissions(permission_level);

-- file history and version control
CREATE TABLE file_history (
	file_id BIGINT UNSIGNED, 
	version SMALLINT UNSIGNED,
	client_path VARCHAR(4096) NOT NULL, 
	server_path VARCHAR(4096) NOT NULL, 
	last_modified TIMESTAMP, 
	last_author VARCHAR(255), 
	directory BOOL DEFAULT 0, -- is the file a directory?
	size BIGINT UNSIGNED NOT NULL,
	checksum CHAR(32) NOT NULL,
	deleted BOOL DEFAULT 0,
	FOREIGN KEY (file_Id) REFERENCES files(file_id),
	PRIMARY KEY (file_id, version) ) ENGINE = INNODB;
	
-- modify files table
ALTER TABLE files DROP FOREIGN KEY files_ibfk_1;
ALTER TABLE files DROP COLUMN parent;
ALTER TABLE files DROP COLUMN filename;
ALTER TABLE files DROP COLUMN path;

ALTER TABLE files ADD COLUMN client_path VARCHAR(4096) NOT NULL;
ALTER TABLE files ADD COLUMN server_path VARCHAR(4096) NOT NULL;
ALTER TABLE files ADD COLUMN deleted BOOL DEFAULT 0;
ALTER TABLE files ADD COLUMN checksum CHAR(32) NOT NULL;
ALTER TABLE files MODIFY directory BOOL DEFAULT 0;

ALTER TABLE users ADD COLUMN salt CHAR(32) NOT NULL;
-- END Patch 2 ----------------------------------------
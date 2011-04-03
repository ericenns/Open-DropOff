-- =======================================
-- Fresh install
-- =======================================
-- Create users table
CREATE TABLE users (
	username VARCHAR(255) PRIMARY KEY, 
	password_hash CHAR(40) NOT NULL, 
	quota BIGINT UNSIGNED,
	salt CHAR(40) NOT NULL) ENGINE = INNODB;

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
	checksum CHAR(40) NOT NULL
	) ENGINE = INNODB;

-- file history and version control
CREATE TABLE files_history (
	file_id BIGINT UNSIGNED, 
	version SMALLINT UNSIGNED,
	client_path VARCHAR(4096) NOT NULL, 
	server_path VARCHAR(4096) NOT NULL, 
	last_modified TIMESTAMP, 
	last_author VARCHAR(255), 
	directory BOOL DEFAULT 0, -- is the file a directory?
	size BIGINT UNSIGNED NOT NULL,
	checksum CHAR(40) NOT NULL,
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
	
CREATE TABLE sessions (
	session_id CHAR(40) PRIMARY KEY,
	username VARCHAR(255) NOT NULL,
	ip_address INT UNSIGNED NOT NULL,
	expiry TIMESTAMP NOT NULL,
	FOREIGN KEY (username) REFERENCES users(username)
	) ENGINE = INNODB;
	
-- Insert permissions to the permission look-up table
INSERT INTO permissions (permission_level, description) VALUES (0, 'Owner');
INSERT INTO permissions (permission_level, description) VALUES (1, 'Read & Write');
INSERT INTO permissions (permission_level, description) VALUES (2, 'Read Only');
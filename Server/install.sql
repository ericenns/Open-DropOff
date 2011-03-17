-----------------------------------------
-- Fresh install
-----------------------------------------
-- Create users table
CREATE TABLE users (
	username VARCHAR(255) PRIMARY KEY, 
	password_hash CHAR(64) NOT NULL, 
	quota BIGINT UNSIGNED) ENGINE = INNODB;

-- Create files table
CREATE TABLE files (
	file_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
	filename VARCHAR(255) NOT NULL, 
	path VARCHAR(4096) NOT NULL, 
	last_modified TIMESTAMP, 
	last_author VARCHAR(255), 
	version SMALLINT UNSIGNED,
	directory BOOL, -- is the file a directory?
	size BIGINT UNSIGNED,
	parent BIGINT UNSIGNED,
	FOREIGN KEY (parent) REFERENCES files(file_id)) ENGINE = INNODB;
	
-- Create users_files table to resolve the many-to-many relation between files and users
CREATE TABLE users_files(
	username VARCHAR(255) NOT NULL, 
	file_id BIGINT UNSIGNED NOT NULL,
	FOREIGN KEY (username) REFERENCES users(username),
	FOREIGN KEY (file_id) REFERENCES files(file_id),
	PRIMARY KEY (username, file_id)) ENGINE = INNODB;

------------------------------------
-- Patches
------------------------------------

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
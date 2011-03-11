-- Create users table
CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, passwordHash CHAR(64)) ENGINE = INNODB;

-- Create files table
CREATE TABLE files (fileID BIGINT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, path VARCHAR(4096) NOT NULL, last_modified TIMESTAMP, last_author VARCHAR(255), version TINYINT, parent BIGINT,
	FOREIGN KEY (parent) REFERENCES files(fileID)) ENGINE = INNODB;
	
-- Create users_files table to resolve the many-to-many relation between files and users
CREATE TABLE users_files(username VARCHAR(255) NOT NULL, fileID BIGINT NOT NULL,
	FOREIGN KEY (username) REFERENCES users(username),
	FOREIGN KEY (fileID) REFERENCES files(fileID),
	PRIMARY KEY (username, fileID)) ENGINE = INNODB;

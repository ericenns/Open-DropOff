'''
This objects provides access to the database and abstracts the actual database used
from the user of this API. Each and every database request will need a valid reference
to the DatabaseConnection object.

The connection method should be invoked when the client is ready to communicate with the
database.
Created on 2011-03-08

@author: Michael Yagudaev
'''

import MySQLdb

class DatabaseConnection(object):
    '''
    classdocs
    '''
    
    db = ""         #db connection
    cursor = ""     #cursor (you need this to execute sql comment
    data = ""       #data   (this will return tupples from the database

    def __init__(self):
        '''
        Constructor
        '''
        self.connect('euwern','Kr749ykw','opendropoff')
        
    def connect(self, username, password, database):
        '''
        Connects to the database using the given creditials. To disconnect call disconnect
        ''' 
        #db = MySQLdb.connect("localhost", "username", "password", "database")         #database connection
        #
        self.db = MySQLdb.connect("localhost",username,password,database)
        self.cursor = self.db.cursor()
        
    def disconnect(self):
        '''
        Closes the database connection. This should be called when client exits.
        '''
        self.db.close();
        
    def execute(self, sql):
        '''
        Executes sql code
        '''
        self.cursor.execute(sql)
        self.db.commit()
        
    def getResults(self):
        '''
        Gets the results of the last executed query
        '''
        '''
        TODO: write code...
        '''
    
    def fetchOne(self):
        data = self.cursor.fetchone()
        return data
    
    def fetchAll(self):
        data = self.cursor.fetchall()
        return data
    
    def createTable(self):
        sql = '''CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, passwordHash CHAR(64)) ENGINE = INNODB;'''
        self.execute(sql)
        sql = '''CREATE TABLE files (fileID BIGINT AUTO_INCREMENT PRIMARY KEY, filename VARCHAR(255) NOT NULL, path VARCHAR(4096) NOT NULL, last_modified TIMESTAMP, last_author VARCHAR(255), version TINYINT, parent BIGINT,
        FOREIGN KEY (parent) REFERENCES files(fileID)) ENGINE = INNODB;'''
        self.execute(sql)
        sql = '''CREATE TABLE users_files(
                    username VARCHAR(255) NOT NULL, 
                    fileID BIGINT NOT NULL,
                    FOREIGN KEY (username) REFERENCES users(username),
                    FOREIGN KEY (fileID) REFERENCES files(fileID),
                    PRIMARY KEY (username, fileID)) ENGINE = INNODB;
                    '''
        self.execute(sql)
        print 'tables created'
        
    def deleteTable(self):
        sql = '''DROP TABLE users_files'''
        self.execute(sql)
        sql = '''DROP TABLE users'''
        self.execute(sql)
        sql = '''DROP TABLE files'''
        self.execute(sql)

        print 'table deleted'
        
'''
Created on 2011-03-11

@author: Michael Yagudaev
'''
from DatabaseConnection import *

class UsersDB:
    '''
    All operations and data associated with a user in the database.
    '''
    dbConnection = ""
    
    def __init__(self):
        dbConnection = DatabaseConnection()
        
    def getFiles(self, username):
        '''
        Gets all the files a user has in their dropoff box
        '''
        usersFiles = "users_files"
        files = "files"
        
        sql = "SELECT * FROM " + usersFiles + " uf "+"," + files + " f "
        sql = sql + "WHERE uf.fileID = f.fileID" 
        sql = sql + " AND uf.username = " + "'" + username + "'"
        
        self.dbConnection.execute(sql)
        data = self.dbConnection.fetchAll()
        return data
        
    def authenticate(self, username, password):
        '''
        Returns true of false depending if the user passed authentication after
        information was retrived from the DB.
        '''
        tableName = 'users'
        sql = "SELECT passwordHash FROM " + tableName
        sql = sql + " WHERE username = " + "'" + username + "'"
        self.dbConnection.execute(sql)
        data = self.dbConnection.fetchOne()  
        userPassword = data[0]
        if password == userPassword:
            return True
        else:
            return False   
        
    def addUser(self, username, password):
        '''
        Adds a user to the database
        '''
        tableName = 'users'
        sql = "INSERT INTO " + tableName
        sql = sql + " ( username, passwordHash)"
        sql = sql + " VALUES ( '" + username + "' , " + password + " ) "
        
        self.dbConnection.execute(sql)
        
        
    def removeUser(self, username):
        '''
        Remove a user from the database.
        '''
        tableName = 'users'
        sql = "DELETE FROM " + tableName
        sql = sql + " WHERE username = " + "'" + username + "'" 

        self.dbConnection.execute(sql)
        
    def addFile(self, username, fileID, filename , path , last_author , version):
        '''
        Add a file to a specific users drop off account
        '''
        tableName = 'files'
        sql = "INSERT INTO " + tableName
        sql = sql + " ( fileID, filename, path , last_author, version )"
        sql = sql + " VALUES ( " + fileID +" , '" + filename + "'"
        sql = sql + ", '" + path + "' , '" + last_author + "'"
        sql = sql + ",  " + version
        sql = sql + " ) "
        self.dbConnection.execute(sql)
        
        
        tableName = "users_files"
        sql = "INSERT INTO " + tableName
        sql = sql + " ( username, fileID)"
        sql = sql + " VALUES ( '" + username + "' , " + fileID + " ) "
        
        self.dbConnection.execute(sql)
        
    def getFile(self, username, path):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unautorized to access the file. 
        '''
        usersFiles = "users_files"
        files = "files"
        
        sql = "SELECT * FROM " + usersFiles + " uf "+"," + files + " f "
        sql = sql + "WHERE uf.fileID = f.fileID AND f.path =" + "'" + path + "'"
        sql = sql + " AND uf.username = " + "'" + username + "'"
        
        self.dbConnection.execute(sql)
        data = self.dbConnection.fetchOne()
        return data
        
    def connect(self):
        self.dbConnection = DatabaseConnection()
        print "connected"
    
    def disconnect(self):
        self.dbConnection.disconnect()
        print "disconnected"
    
    def getAllUser(self):
        tableName = 'students'
        self.dbConnection.execute('SELECT * FROM ' + tableName)
        data = self.dbConnection.fetchAll()
        return data
    
    def createTable(self):
        self.dbConnection.createTable()
    
    def deleteTable(self):
        self.dbConnection.deleteTable()
    
        
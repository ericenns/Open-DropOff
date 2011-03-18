'''
Created on 2011-03-11

@author: Michael Yagudaev
'''
from DatabaseConnection import *

class UsersDB:
    '''
    All operations and data associated with a user in the database.
    '''
    
    def __init__(self, conn):
        self._conn = conn
        
    def getFiles(self, username):
        '''
        Gets all the files a user has in their dropoff box
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.fileID = f.fileID " 
        sql = sql + " AND uf.username = %s "
        
        self._conn._execute(sql, username)
        data = self._conn._fetchAll()
        return data
        
    def authenticate(self, username, password):
        '''
        Returns true of false depending if the user passed authentication after
        information was retrieved from the DB.
        '''
        sql = "SELECT passwordHash FROM users "
        sql = sql + " WHERE username = %s "
        self._conn._execute(sql, username)
        data = self._conn._fetchOne()
        
        if data != None:  
            userPassword = data[0]
            if password == userPassword:
                return True
            
        return False   
        
    def addUser(self, username, password):
        '''
        Adds a user to the database
        '''
        sql = "INSERT INTO users "
        sql = sql + " ( username, passwordHash) "
        sql = sql + " VALUES ( %s , %s ) "
        
        self._conn._execute(sql, username, password)
        
    def updateUsername(self, newUsername, username, password):
        '''
        Update an existing username
        '''
        sql = "UPDATE users "
        sql = sql + " SET username = %s"
        sql = sql + " WHERE username = %s AND password = %s"
        
        try:
            self._conn._execute(sql, username, password)
        except:
            print sys.exc_info()[1]; #Username, password not found
      
    def updatePassword(self, newPassword, username, password):
        '''
        Update an existing user password
        '''
        sql = "UPDATE users "
        sql = sql + " SET passwordHash = %s"
        sql = sql + " WHERE username = %s AND password = %s"
        
        try:
            self._conn._execute(sql, username, password)
        except:
            print sys.exc_info()[1];
        
    def removeUser(self, username):
        '''
        Remove a user from the database.
        '''
        sql = "DELETE FROM users "
        sql = sql + " WHERE username = %s " 

        self._conn._execute(sql, username)
        
    def addFile(self, username, filename , path , lastAuthor, lastModified, version):
        '''
        Add a file to a specific users drop off account.
        '''
        ''' TODO: kill fileID and let it use the auto increment...'''
        ''' TODO: filename and path can be merged into one... '''
        ''' TODO: wrap in transaction! '''
        
        sql = "INSERT INTO files "
        sql = sql + " ( filename, path , last_author, last_modified, version) "
        sql = sql + " VALUES ( %s, %s , %s, %s, %s ) "
        self._conn._execute(sql, filename, path, lastAuthor, lastModified, version)
        
        fileID = self._conn._getLastRowID()
        
        sql = "INSERT INTO users_files "
        sql = sql + " ( username, fileID) "
        sql = sql + " VALUES ( %s , %s ) "
        
        self._conn._execute(sql, username, fileID)
        
    def getFile(self, username, path):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unauthorised to access the file. 
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.fileID = f.fileID AND f.path = %s "
        sql = sql + " AND uf.username = %s"
        
        self._conn._execute(sql, path, username)
        data = self._conn._fetchOne()
        return data
    
    def getAllUser(self):
        self._conn._execute('SELECT * FROM students')
        data = self._conn._fetchAll()
        return data
    
        
###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Michael Yagudaev                                                         #
#    Robert Tetlock                                                           #
#    Marilyn Hacko                                                            #
#    Eu Wern                                                                  #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

import sys
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
        sql = sql + "WHERE uf.file_id = f.file_id " 
        sql = sql + " AND uf.username = %s "
        
        self._conn._execute(sql, username)
        data = self._conn._fetchAll()
        return data
    
    def userExists(self, username):
        sql = "SELECT * FROM users "
        sql = sql + "WHERE username = %s "
        self._conn._execute(sql, username)
        data = self._conn._getCount()
        
        if data == 1:
            return True
        else:
            return False
        
    def authenticate(self, username, password):
        '''
        Returns true of false depending if the user passed authentication after
        information was retrieved from the DB.
        '''
        sql = "SELECT password_hash FROM users "
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
        sql = sql + " ( username, password_hash) "
        sql = sql + " VALUES ( %s , %s ) "
        
        self._conn._execute(sql, username, password)
        
    def getUser(self, username):
        self._conn._execute('SELECT * FROM users WHERE username = %s', username)
        data = self._conn._fetchOne()
        return data
    
    def updateUsername(self, newUsername, username, password):
        '''
        Update an existing username
        '''
        sql = "UPDATE users "
        sql = sql + " SET username = %s"
        sql = sql + " WHERE username = %s AND password_hash = %s"
        
        try:
            self._conn._execute(sql, newUsername, username, password)
        except:
            print sys.exc_info()[1] #Username, password not found
      
    def updatePassword(self, newPassword, username, password):
        '''
        Update an existing user password
        '''
        sql = "UPDATE users "
        sql = sql + " SET password_hash = %s"
        sql = sql + " WHERE username = %s AND password_hash = %s"
        
        try:
            self._conn._execute(sql, newPassword, username, password)
        except:
            print sys.exc_info()[1]
        
    def removeUser(self, username):
        '''
        Remove a user from the database.
        '''
        sql = "DELETE FROM users "
        sql = sql + " WHERE username = %s " 

        try:
           self._conn._execute(sql, username)
        except:
            print sys.exc_info()[1]
        
    def addFile(self, username, filename , path , filesize , lastAuthor, lastModified, version):
        '''
        Add a file to a specific users drop off account.
        '''
        ''' TODO: filename and path can be merged into one... '''
        ''' TODO: wrap in transaction! '''
        
        '''Check if user has enough quota remaining 
        if(getSpaceRemaining() < filesize)
        '''
        
        sql = "INSERT INTO files "
        sql = sql + " ( filename, path , last_author, last_modified, version) "
        sql = sql + " VALUES ( %s, %s , %s, %s, %s ) "
        self._conn._execute(sql, filename, path, lastAuthor, lastModified, version)
        
        fileID = self._conn._getLastRowID()
        
        sql = "INSERT INTO users_files "
        sql = sql + " ( username, file_id) "
        sql = sql + " VALUES ( %s , %s ) "
        
        self._conn._execute(sql, username, fileID)
        
    def getFile(self, username, path):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unauthorised to access the file. 
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.file_id = f.file_id AND f.path = %s "
        sql = sql + " AND uf.username = %s"
        
        self._conn._execute(sql, path, username)
        data = self._conn._fetchOne()
        return data
    
    def removeFile(self,path):
        '''
        Remove a File from the database.
        '''
        
        sql = "SELECT file_id FROM files WHERE path = %s"
        self._conn._execute(sql,path) 
        data = self._conn._fetchOne()
        fileId = data[0]
        
        sql = "DELETE FROM users_files"
        sql = sql + " WHERE file_id = %s " 

        self._conn._execute(sql, fileId)
        
        sql = "DELETE FROM files WHERE file_id = %s"
        
        self._conn._execute(sql, fileId)
            
    def getAllUser(self):
        self._conn._execute('SELECT * FROM users')
        data = self._conn._fetchAll()
        return data
    
    def getFilesInDir(self, path):
        '''
        Get a list of files in a given directory
        '''
        
        sql = "SELECT * FROM files f"
        sql = sql + " WHERE f.path LIKE %s "
        
        path =  path + '%' #adding wildcard 
        
        self._conn._execute(sql,path)
        data = self._conn._fetchAll()
        return data
        
    def updateLastAuthor(self, path, newAuthor):   
        '''
        update last_author in a given file path
        '''
                
        sql = "UPDATE files f SET last_author = %s"
        sql = sql + " WHERE f.path = %s "
        
        self._conn._execute(sql,newAuthor,path)
        
    def getUserQuota():
        '''
        Return amount of space user has
        '''
                
        sql = "SELECT quota FROM users"
        sql = sql + " WHERE username = %s "
        
        try:
            self._conn._execute(sql)
        except:
            print sys.exc_info()[1]
       
    def setUserQuota(self, quota, username):
        '''
        Return amount of space user has
        '''
        
        sql = "UPDATE users "
        sql = sql + " SET quota = %s"
        sql = sql + " WHERE username = %s"
        
        try:
            self._conn._execute(sql, username)
        except:
            print sys.exc_info()[1]

    def getSpaceRemaining():
        '''
        Return amount of space left for user
        '''
    
        sql = "SELECT users "
        sql = sql + " SET quota = %s"
        sql = sql + " WHERE username = %s"
        
        try:
            self._conn._execute(sql, username)
        except:
            print sys.exc_info()[1]

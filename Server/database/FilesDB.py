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

import DatabaseConnection

class FilesDB:    
    '''
    All transactions associated primarily with a file. A connection with the database must be established before 
    using this class. Conn is a valid DatabaseConnection object.
    Note: the files on the server and the database will be to be kept in sync by the business
    logic layer.
    '''
    
    def __init__(self, conn):
        self._conn = conn
    
    def addFile(self, username, clientPath, serverPath , filesize , lastAuthor, lastModified, version, checksum):
        '''
        Add a file to a specific users drop off account.
        Caller must check that user has enough quota remaining 
        if UsersDB.getSpaceRemaining(username) > filesize:'''
        sql = "INSERT INTO files "
        sql = sql + " ( client_path, server_path , last_author, last_modified, version, size, checksum) "
        sql = sql + " VALUES ( %s , %s, %s, %s, %s, %s, %s ) "
        
        try:
            self._conn._execute(sql, clientPath, serverPath, lastAuthor, lastModified, version, filesize, checksum)
            
            fileID = self._conn._getLastRowID()
            
            sql = "INSERT INTO users_files "
            sql = sql + " ( username, file_id, permission_level) "
            sql = sql + " VALUES ( %s , %s, 0 ) "
            
            self._conn._execute(sql, username, fileID)
            self._conn._commit()
        except:
            self._conn._rollback()
            fileID = -1
            print sys.exc_info()[1]
        
        return fileID   
        
    def removeFile(self, username, client_path):
        '''
        Remove a File from the database.
        '''
        # TODO: what about file history??? This is an over simplified version and needs to be changed...
        
        sql = "SELECT f.file_id FROM files f INNER JOIN users_files uf ON f.file_id = uf.file_id "
        sql = sql + " WHERE f.client_path = %s and uf.username = %s"
        self._conn._execute(sql, client_path, username) 
        data = self._conn._fetchOne()
        fileId = data['file_id']
        
        try:
            sql = "DELETE FROM users_files "
            sql = sql + " WHERE file_id = %s " 
    
            self._conn._execute(sql, fileId)
            
            sql = "DELETE FROM files WHERE file_id = %s"
            
            self._conn._execute(sql, fileId)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
    
    def updateFile(self, originalFileId, newFile):
        '''
        Update the file by creating a new version of the file.
        @param newFile Dict A dictionary containing the description of the new file
        '''
        # TODO: implement method
        
    def getFile(self, username, clientPath, version):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unauthorised to access the file. 
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.file_id = f.file_id AND f.client_path = %s "
        sql = sql + " AND uf.username = %s"
        
        try:
            self._conn._execute(sql, clientPath, username)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
    
    def getFilesInDir(self, clientPath, username):
        '''
        Get a list of files in a given directory
        '''
        
        sql = "SELECT * FROM files f "
        sql = sql + " INNER JOIN users_files uf ON f.file_id = uf.file_id "
        sql = sql + " WHERE f.client_path LIKE %s AND uf.username = %s "
        
        clientPath =  clientPath + '%' #adding wildcard 
        
        try:
            self._conn._execute(sql, clientPath, username)
            data = self._conn._fetchAll()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
    
    def getAllFiles(self, username):
        '''
        Gets all the files a user has in their dropoff box
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.file_id = f.file_id " 
        sql = sql + " AND uf.username = %s "
        
        try:
            self._conn._execute(sql, username)
            data = self._conn._fetchAll()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
    
    def getFileHistory(self, file_id):
        '''
        Gets a list of all the versions of the given file
        '''
        ''' TODO: implement method '''
    
    def updateLastAuthor(self, path, newAuthor):   
        '''
        update last_author in a given file path
        Not Needed
        '''
                
        sql = "UPDATE files f SET last_author = %s"
        sql = sql + " WHERE f.client_path = %s "
        
        try:
            self._conn._execute(sql,newAuthor,path)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
        
    def getClientPath(self, file_id):
        '''
        Gets the file path on the clients machine
        '''
        sql = "SELECT client_path FROM files"
        sql = sql + " WHERE file_id = %s "
        
        try:
            self._conn._execute(sql,file_id)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        if data != None:
            return data['client_path']
        else:
            return None
        
    def getServerPath(self, file_id):
        '''
        Gets the file path on the server
        '''
        sql = "SELECT server_path FROM files"
        sql = sql + " WHERE file_id = %s "
        
        try:
            self._conn._execute(sql,file_id)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        if data != None:
            return data['server_path']
        else:
            return None
            
    def getChecksum(self, file_id):
        '''
        Gets the checksum for a file
        '''
        sql = "SELECT checksum FROM files"
        sql = sql + " WHERE file_id = %s "
        
        try:
            self._conn._execute(sql,file_id)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        if data != None:
            return data['checksum']
        else:
            return None
            
    def getLastModified(self, file_id):
        '''
        Gets the last modified timestamp for a file
        '''
        sql = "SELECT last_modified FROM files"
        sql = sql + " WHERE file_id = %s "
        
        try:
            self._conn._execute(sql,file_id)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        if data != None:
            return data['last_modified']
        else: 
            return None     
    
    def getPermission(self, username, fileId):
        '''
        Returns the file permission
        '''
    
        sql = "SELECT permission_level "
        sql = sql + " FROM users_files "
        sql = sql + " WHERE username = %s AND file_id = %s"
                
        try:
            self._conn._execute(sql, username, fileId)
            data = self._conn._fetchOne();
        except:
            print sys.exc_info()[1]
            
        if data != None:
            return data['permission_level']
        else:
            return None
    
    def setPermission(self, username, fileId, newPermission):
        '''
        Sets the file permission on the specified file
        '''
        sql = "UPDATE users_files "
        sql = sql + " SET permission_level = %s"
        sql = sql + " WHERE username = %s AND file_id = %s"
        
        try:
            self._conn._execute(sql, newPermission, username, fileId)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]   
    
        
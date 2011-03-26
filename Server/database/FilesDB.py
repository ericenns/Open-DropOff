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
    
    def addFile(self, username, path , filesize , lastAuthor, lastModified, version):
        '''
        Add a file to a specific users drop off account.
        '''
        
        '''Check if user has enough quota remaining 
        if UsersDB.getSpaceRemaining(username) > filesize:'''
        sql = "INSERT INTO files "
        sql = sql + " ( client_path, server_path , last_author, last_modified, version) "
        sql = sql + " VALUES ( %s , %s, %s, %s, %s ) "
        self._conn._execute(sql, path, "temp_crap", lastAuthor, lastModified, version)
        
        fileID = self._conn._getLastRowID()
        
        sql = "INSERT INTO users_files "
        sql = sql + " ( username, file_id, permission_level) "
        sql = sql + " VALUES ( %s , %s, 0 ) "
        
        self._conn._execute(sql, username, fileID)
        
        '''else:
            return 'User does not have enough space to add file' '''
        
    def removeFile(self,path):
        '''
        Remove a File from the database.
        '''
        
        sql = "SELECT file_id FROM files WHERE client_path = %s"
        self._conn._execute(sql, path) 
        data = self._conn._fetchOne()
        fileId = data[0]
        
        try:
            sql = "DELETE FROM users_files"
            sql = sql + " WHERE file_id = %s " 
    
            self._conn._execute(sql, fileId)
            
            sql = "DELETE FROM files WHERE file_id = %s"
            
            self._conn._execute(sql, fileId)
        except:
            '''print sys.exc_info()[1]'''
    
    def getFile(self, username, path):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unauthorised to access the file. 
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.file_id = f.file_id AND f.client_path = %s "
        sql = sql + " AND uf.username = %s"
        
        self._conn._execute(sql, path, username)
        data = self._conn._fetchOne()
        return data
    
    def getFilesInDir(self, path):
        '''
        Get a list of files in a given directory
        '''
        
        sql = "SELECT * FROM files f"
        sql = sql + " WHERE f.client_path LIKE %s "
        
        path =  path + '%' #adding wildcard 
        
        self._conn._execute(sql,path)
        data = self._conn._fetchAll()
        return data
    
    def getFiles(self, username):
        '''
        Gets all the files a user has in their dropoff box
        '''
        
        sql = "SELECT * FROM users_files uf, files f "
        sql = sql + "WHERE uf.file_id = f.file_id " 
        sql = sql + " AND uf.username = %s "
        
        self._conn._execute(sql, username)
        data = self._conn._fetchAll()
        return data if data != None else None
    
    def updateLastAuthor(self, path, newAuthor):   
        '''
        update last_author in a given file path
        Not Needed
        '''
                
        sql = "UPDATE files f SET last_author = %s"
        sql = sql + " WHERE f.client_path = %s "
        
        self._conn._execute(sql,newAuthor,path)

    def getLastAuthor(self, conn, path):
        '''
        Gets the last author of the file, i.e. who it was last modified by
        Not Needed
        '''
        
    def getClientPath(self, file_id):
        '''
        Gets the file path on the clients machine
        '''
        sql = "SELECT client_path FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data['client_path'] if data != None else None
        
    def getServerPath(self, file_id):
        '''
        Gets the file path on the server
        '''
        sql = "SELECT server_path FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data['server_path'] if data != None else None
            
    def getChecksum(self, file_id):
        '''
        Gets the checksum for a file
        '''
        sql = "SELECT checksum FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data['checksum'] if data != None else None
            
    def getLastModified(self, file_id):
        '''
        Gets the last modified timestamp for a file
        '''
        sql = "SELECT last_modified FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data['last_modified'] if data != None else None        
    
        
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
import sys

class FilesDB:    
    '''
    FilesDB Stub class... should look the same but be more fake than Hollywood itself :)
    
    tuple format fileList - (fileID , client_path , server_path, version, last_modified, size, checksum)
    tuple format usersFilesList - (fileID , username)
    '''
    
    def __init__(self, conn):
        self._conn = conn
        self._fileList = []    
        self._usersFilesList = []
        self._fileID = 0
        
    def addFile(self, username, path , filesize , lastAuthor, lastModified, version):
        self._fileID += 1
        file = ( self._fileID , path , 0 , 0, lastModified, filesize)
        self._fileList.append(file)
        
        fileRef = (self._fileID , username)
        self._usersFilesList.append(fileRef)
        
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
            print sys.exc_info()[1]
    
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
            
    def getChecksum(self, file_id):
        '''
        Gets the checksum for a file
        '''
        sql = "SELECT checksum FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data[0]
            
    def getLastModified(self, file_id):
        '''
        Gets the last modified timestamp for a file
        '''
        sql = "SELECT last_modified FROM files"
        sql = sql + " WHERE file_id = %s "
        
        self._conn._execute(sql,file_id)
        data = self._conn._fetchOne()
        return data[0]        
        
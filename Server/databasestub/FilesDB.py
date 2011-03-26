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
        
    def addFile(self, username, path , filesize , lastAuthor, lastModified, version, checksum):
        self._fileID += 1
        file = {'file_id': self._fileID , 'client_path': path , 'server_path': 0 , 'version': version, 'last_modified': lastModified, 'size': filesize, 'checksum': checksum}
        self._fileList.append(file)
        
        fileRef = {'file_id': self._fileID , 'username': username}
        self._usersFilesList.append(fileRef)
        
    def removeFile(self,path):
        '''
        Remove a File from the database.
        '''
        pass
    
    def getFile(self, username, client_path):
        for userFile in self._usersFilesList:
            if userFile['username'] == username:
                for file in self._fileList:
                    if file['file_id'] == userFile['file_id'] and file['client_path'] == client_path:
                        return file
    
    def getAllFiles(self, username):
        data = []
        
        for userFile in self._usersFilesList:
            if userFile['username'] == username:
                for file in self._fileList:
                    if file['file_id'] == userFile['file_id']:
                        data.append(file)
        
        return data
    
    def getAllFilesSize(self, username):
        size = 0
        
        for userFile in self._usersFilesList:
            if userFile['username'] == username:
                for file in self._fileList:
                    if file['file_id'] == userFile['file_id']:
                        size += file['size']
        
        return size
            
    def getChecksum(self, file_id):
        for file in self._usersFilesList:
            if file['file_id'] == file_id:
                return file['checksum']
        
        return None
            
    def getLastModified(self, file_id):
        for file in self._usersFilesList:
            if file['file_id'] == file_id:
                return file['last_modified']
        
        return None
        

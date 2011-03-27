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

class FilesDB:    
    '''
    FilesDB Stub class... should look the same but be more fake than Hollywood itself :)
    
    tuple format fileList - (fileID , client_path , server_path, version, last_modified, size, checksum)
    tuple format usersFilesList - (fileID , username, permission_level)
    '''
    
    def __init__(self, conn):
        self._conn = conn
        self._fileList = []    
        self._usersFilesList = []
        self._fileID = 0
        
    def addFile(self, username, clientPath, serverPath , filesize , lastAuthor, lastModified, version, checksum):
        self._fileID += 1
        file = {'file_id': self._fileID , 'client_path': clientPath , 'server_path': serverPath , 'version': version, 'last_modified': lastModified, 'size': filesize, 'checksum': checksum}
        self._fileList.append(file)
        
        fileRef = {'file_id': self._fileID , 'username': username, 'permission_level': 0}
        self._usersFilesList.append(fileRef)
        
        return self._fileID
        
    def removeFile(self, username, clientPath):
        '''
        Remove a File from the database.
        '''
        for userFile in self._usersFilesList:
            for file in self._fileList:
                if file['file_id'] == userFile['file_id'] and userFile['username'] == username and file['client_path'] == clientPath:
                    self._fileList.remove(file)
                    return self._usersFilesList.remove(userFile)
    
    def getFile(self, username, clientPath):
        for userFile in self._usersFilesList:
            if userFile['username'] == username:
                for file in self._fileList:
                    if file['file_id'] == userFile['file_id'] and file['client_path'] == clientPath:
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
            
    def getFilesInDir(self, client_path, username):
        data = []
        
        for userFile in self._usersFilesList:
            if userFile['username'] == username:
                for file in self._fileList:
                    if file['file_id'] == userFile['file_id'] and file['client_path'].startswith(client_path):
                        data.append(file)
        
        return data
    
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
    
    def getPermission(self, username, fileId):
        for userFile in self._usersFilesList:
            if userFile['username'] == username and userFile['file_id'] == fileId:
                return userFile['permission_level']
    
    def setPermission(self, username, fileId, newPermission):
        for userFile in self._usersFilesList:
            if userFile['username'] == username and userFile['file_id'] == fileId:
                userFile['permission_level'] = newPermission

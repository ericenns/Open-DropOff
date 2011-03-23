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
    FilesDB Stub class... should look the same but be more fake than Hollywood itself :)
    '''
    
    def __init__(self, conn):
        self._conn = conn
        self._fileList = []
    
    def addFile(self, username, path , filesize , lastAuthor, lastModified, version):
        pass
    
    def removeFile(self,path):
        pass
    
    def getFile(self, username, path):
        pass
    
    def getFilesInDir(self, path):
        pass
    
    def getFiles(self, username):
        pass
    
    def updateLastAuthor(self, path, newAuthor):   
        pass

    def getLastAuthor(self, conn, path):
        pass
        
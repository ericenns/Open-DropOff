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
    FilesDB Stub class... should look the same but be more fake than Hollywood itself :)
    '''
    
    def __init__(self, conn):
        self._conn = conn
        
    def userExists(self, username):
        pass
        
    def authenticate(self, username, password):
        pass
        
    def addUser(self, username, password):
        pass
        
    def getUser(self, username):
        pass
    
    def updateUsername(self, newUsername, username, password):
        pass
      
    def updatePassword(self, newPassword, username, password):
        pass
        
    def removeUser(self, username):
        pass
            
    def getAllUser(self):
        pass
                
    def getUserQuota():
        pass
       
    def setUserQuota(self, quota, username):
        pass

    def getSpaceRemaining(self, username):
        pass
            
    def getPermission(self, username, fileId):
        pass
    
    def setPermission(self, username, fileId, newPermission):
        pass
            
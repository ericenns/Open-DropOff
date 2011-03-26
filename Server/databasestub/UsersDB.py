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

class UsersDB:
    '''
    FilesDB Stub class... should look the same but be more fake than Hollywood itself :)
    '''
    #we will be storing the data as tuples in a list - check out addUser
    '''
    tuple format - ("username" , password , quota , salt) - default quota and salt to zero
    '''
    
    def __init__(self, conn):
        self._conn = conn
        self._userList = [] 
        
    def _getUserIndex(self, username):
        '''
        This function is only created in Stub database : it will return -1 if no username are found
        '''
        index = 0
        foundUser = False        
        while (index < len(self._userList)) & (foundUser == False) :
            currUser = self._userList[index]
            if currUser['username'] == username :
                foundUser = True
            else:
                index += 1       
        
        if foundUser == True:
            return index
        else:
            return -1
        
    def userExists(self, username):
        user = self.getUser(username)
        if user != None:
            return True
        else:
            return False
        
    def authenticate(self, username, password):
        user = self.getUser(username)
        if user['password_hash'] == password:
            return True
        else:
            return False
        
    def addUser(self, username, password, quota=0, salt="abcdefg"):
        user = { 'username' : username , 'password_hash' : password ,'quota': quota ,'salt': salt}
        self._userList.append(user)
        
    def getUser(self, username):
        index = 0
        foundUser = False

        while (index < len(self._userList)) & (foundUser == False) :
            currUser = self._userList[index]
            if currUser['username'] == username :
                foundUser = True
            else:
                index += 1
        
        if foundUser == True:
            return self._userList[index]
        else:
            return None
        
    
    def updateUsername(self, newUsername, username, password):
        index = self._getUserIndex(username)
        if index != -1:
            user = self._userList[index]
            self._userList[index] = { 'username' : newUsername 
                                    , 'password_hash' : user['password_hash'] 
                                    , 'quota' : user['quota'] 
                                    , 'salt' : user['salt'] }
                
        
    def updatePassword(self, newPassword, username, password):
        index = self._getUserIndex(username)
        if index != -1:
            user = self._userList[index]
            self._userList[index] = { 'username' : user['username'] 
                                    , 'password_hash' : newPassword 
                                    , 'quota' : user['quota'] 
                                    , 'salt' : user['salt'] }
    def removeUser(self, username):
        user = self.getUser(username)
        if user != None:
            self._userList.remove(user)
            
    def getAllUser(self):
        return tuple(self._userList)
                
    def getUserQuota(self, username):
        user = self.getUser(username)
        if user != None:
            return user[2]
       
    def setUserQuota(self, quota, username):
        index = self._getUserIndex(username)
        if index != -1:
            user = self._userList[index]
            self._userList[index] = ( user[0] , user[1] , quota , user[3] )
                
    def getSpaceRemaining(self, username):
        pass
            
    def getPermission(self, username, fileId):
        pass
    
    def setPermission(self, username, fileId, newPermission):
        pass
            
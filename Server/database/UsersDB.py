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

from DatabaseConnection import *

class UsersDB:
    '''
    All operations and data associated with a user in the database.
    '''
    
    def __init__(self, conn):
        self._conn = conn
        
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
        sql = sql + " WHERE username = %s AND password = %s"
        
        try:
            self._conn._execute(sql, username, password)
        except:
            print sys.exc_info()[1] #Username, password not found
      
    def updatePassword(self, newPassword, username, password):
        '''
        Update an existing user password
        '''
        sql = "UPDATE users "
        sql = sql + " SET password_hash = %s"
        sql = sql + " WHERE username = %s AND password = %s"
        
        try:
            self._conn._execute(sql, username, password)
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
            
    def getAllUser(self):
        self._conn._execute('SELECT * FROM users')
        data = self._conn._fetchAll()
        return data
                
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

    def getSpaceRemaining(self, username):
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
            
    def getPermission(self, username, file_id):
        '''
        Returns the file permission
        '''
    
        sql = "SELECT permission "
        sql = sql + " FROM users_files "
        sql = sql + " WHERE username = %s"
        
        data = None
        
        try:
            self._conn._execute(sql, username)
            data 
        except:
            print sys.exc_info()[1]
    
    def setPermission(self, username, file_id, newPermission):
        '''
        Sets the file permission on the specified file
        '''
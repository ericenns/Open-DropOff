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
        
    def userExists(self, username):
        sql = "SELECT * FROM users "
        sql = sql + "WHERE username = %s "
        
        try:
            self._conn._execute(sql, username)
            data = self._conn._getCount()
        except:
            data = None
            print sys.exc_info()[1]
        
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
        
        try:
            self._conn._execute(sql, username)
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
        
        if data != None:  
            userPassword = data['password_hash']
            if password == userPassword:
                return True
            
        return False
        
    def addUser(self, username, password, quota=0, salt="abcdefg"):
        '''
        Adds a user to the database
        '''
        sql = "INSERT INTO users "
        sql = sql + " ( username, password_hash, quota, salt) "
        sql = sql + " VALUES ( %s , %s, %s, %s ) "
        
        try:
            self._conn._execute(sql, username, password, quota, salt)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
        
    def getUser(self, username):
        '''
        Gets a user record using the given username. Returns None if user not found.
        '''
        self._conn._execute('SELECT * FROM users WHERE username = %s', username)
        
        try:
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
    
    def updateUsername(self, newUsername, username):
        '''
        Update an existing username
        '''
        sql = "UPDATE users "
        sql = sql + " SET username = %s"
        sql = sql + " WHERE username = %s"
        
        try:
            self._conn._execute(sql, newUsername, username)
            self._conn._commit()
        except:
            self._conn._rollback()
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
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
        
    def removeUser(self, username):
        '''
        Remove a user from the database.
        '''
        sql = "DELETE FROM users "
        sql = sql + " WHERE username = %s " 

        try:
            self._conn._execute(sql, username)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
            
    def getAllUser(self):
        '''
        Gets all the registered users on the system, or None if there are none.
        '''
        try:
            self._conn._execute('SELECT * FROM users')
            data = self._conn._fetchAll()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
                
    def getUserQuota(self, username):
        '''
        Return amount of space user has
        '''
                
        sql = "SELECT quota FROM users"
        sql = sql + " WHERE username = %s "
        
        result = -1
        
        try:
            self._conn._execute(sql, username)
            data = self._conn._fetchOne()
            
            if data != None:
                result = data['quota']
        except:
            print sys.exc_info()[1]
            
        return result
            
       
    def setUserQuota(self, quota, username):
        '''
        Return amount of space user has
        '''
        
        sql = "UPDATE users "
        sql = sql + " SET quota = %s"
        sql = sql + " WHERE username = %s"
        
        try:
            self._conn._execute(sql, quota, username)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]

    def getSpaceRemaining(self, username):
        '''
        Return amount of space left for user or -1 on error
        '''
    
        sql = "SELECT sum(files.size) AS space_used FROM users_files JOIN files "
        sql = sql + " ON files.file_id = users_files.file_id WHERE username = %s"
        result = -1
        
        try:
            self._conn._execute(sql, username)
            data = self._conn._fetchOne()
            spaceUsed = 0
            
            if(data != None):
                spaceUsed = data['space_used']
                
            result = self.getUserQuota(username) - spaceUsed
       
        except:
            print sys.exc_info()[1]
            
        return result
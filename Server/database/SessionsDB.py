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
import datetime
import socket
import struct
from DatabaseConnection import *

class SessionsDB:
    '''
    All operations and data associated with a session in the database.
    '''
    
    def __init__(self, conn):
        self._conn = conn
        
    def createSession(self, session_id, username, ip_address, expiry):
        '''
        Adds a session to sessions Table
        '''
        print session_id
        print username
        print ip_address
        print expiry
        sql = "INSERT INTO sessions "
        sql = sql + " ( session_id, username, ip_address, expiry) "
        sql = sql + " VALUES ( %s , %s, INET_ATON(%s), %s ) "
        
        try:
            self._conn._execute(sql, session_id, username, ip_address, expiry)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
        
    def getSession(self, session_id):
        '''
        Gets a session record using the given session_id. Returns None if user not found.
        '''
        sql = 'SELECT session_id, username, INET_NTOA(ip_address) AS ip_address, expiry FROM sessions WHERE session_id = %s'
        
        self._conn._execute(sql, session_id)
        
        try:
            data = self._conn._fetchOne()
        except:
            data = None
            print sys.exc_info()[1]
            
        return data
        
    def getUserFromSession(self, session_id):
        '''
        Gets the username for a session_id
        '''
        self._conn._execute('SELECT username FROM sessions WHERE session_id = %s', session_id)
        
        try:
            data = self._conn._fetchOne()
            
            if data != None:
                result = data['username']
            else:
                result = None
        except:
            result = None
            print sys.exc_info()[1]
            
        return result
        
    def endSession(self, session_id):
        '''
        Removes the session with given id from sessions table
        '''
        try:
            self._conn._execute('DELETE FROM sessions WHERE session_id = %s', session_id)
        except:
            print sys.exc_info()[1]
            
    def removeExpiredSessions(self):
        '''
        Removes sessions which have expired
        '''
        currentDate = datetime.datetime.now()
        
        try:
            self._conn._execute('DELETE FROM sessions WHERE expiry <= %s', currentDate)
            self._conn._commit()
        except:
            self._conn._rollback()
            print sys.exc_info()[1]
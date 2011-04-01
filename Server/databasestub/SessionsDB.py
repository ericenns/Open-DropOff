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
from DatabaseConnection import *

class SessionsDB:
    '''
    All operations and data associated with a session in the database.
    '''
    
    def __init__(self, conn):
        self._conn = conn
        self._sessionList = []   
        
    def createSession(self, session_id, username, ip_address, expiry):
        '''
        Adds a session to sessions Table
        '''
        session = {'session_id': session_id , 'username': username , 'ip_address': ip_address , 'expiry': expiry}
        self._sessionList.append(session)
    
    def getSession(self, session_id):
        for session in self._sessionList:
            if session['session_id'] == session_id:
                return session
            else:
                return "session %s not found", session_id
        
    def getUserFromSession(self, session_id):
        for session in self._sessionList:
            if session['session_id'] == session_id:
                return session['username']
        
        return None
        
        
    def endSession(self, session_id):
        for session in self._sessionList:
            if session['session_id'] == session_id:
                self._sessionList.remove(session)
            
    def removeExpiredSessions(self):
        for session in self._sessionList:
            if session['expiry'] <= datetime.datetime.now():
                self._sessionList.remove(file)
                return self._sessionList.remove(session)
                
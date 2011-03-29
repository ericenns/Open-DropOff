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
import ConfigParser
import unittest
import datetime

from database.DatabaseConnection import DatabaseConnection
from database.UsersDB import UsersDB
from database.SessionsDB import SessionsDB

class SessionsDBTest(unittest.TestCase):

    def setUp(self):
        self._connection = DatabaseConnection()
        
        # read data from config file, we don't want to be modifying this code  all the time
        config = ConfigParser.ConfigParser()
        config.readfp(open('../test/test-db.cfg'))
        DBHOST = config.get("Database", "host")
        DB = config.get("Database", "database")
        DBUSER = config.get("Database", "user")
        DBPASS = config.get("Database", "pass")
        
        self._connection.connect(DBHOST, DBUSER, DBPASS, DB)
        self._userDB = UsersDB(self._connection)
        
        self._sessionsDB = SessionsDB(self._connection)
        self._userDB.addUser('user1','123')
        
    def tearDown(self):
        self._connection._execute('TRUNCATE sessions')
        self._connection._execute('TRUNCATE users')
        self._connection._commit()
        self._connection.disconnect()

    def testSession(self):
        sessionId = '440f23c58848769685e481ff270b046659f40b7c'
        self._sessionsDB.createSession(sessionId, 'user1', '216.27.61.137', datetime.datetime.now())
        session = self._sessionsDB.getSession(sessionId)
        self.assertEqual( session['username'], 'user1')
        self.assertEqual( self._sessionsDB.getUserFromSession(sessionId), 'user1')
        self.assertEqual( session['ip_address'], '216.27.61.137')        
        self._sessionsDB.endSession(sessionId)
        self.assertEqual( None, self._sessionsDB.getSession(sessionId))
    
    def testRemoveExpiredSessions(self):
        sessionIds = ('440f23c58848769685e481ff270b046659f40b7a','440f23c58848769685e481ff270b046659f40b7b', '440f23c58848769685e481ff270b046659f40b7c')
        self._sessionsDB.createSession(sessionIds[0], 'user1', '216.27.61.137', datetime.datetime.now() + datetime.timedelta(hours = 2))
        self._sessionsDB.createSession(sessionIds[1], 'user1', '216.27.61.138', datetime.datetime.now() - datetime.timedelta(hours = 2))
        self._sessionsDB.createSession(sessionIds[2], 'user1', '216.27.61.139', datetime.datetime.now() - datetime.timedelta(hours = 2))
        self._sessionsDB.removeExpiredSessions()
        
        self.assertEqual( sessionIds[0], self._sessionsDB.getSession(sessionIds[0])['session_id'])
        self.assertEqual( None, self._sessionsDB.getSession(sessionIds[1]))
        self.assertEqual( None, self._sessionsDB.getSession(sessionIds[2]))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
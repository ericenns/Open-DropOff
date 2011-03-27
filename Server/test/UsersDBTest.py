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

from database.DatabaseConnection import DatabaseConnection
from database import UsersDB


class UsersDBTest(unittest.TestCase):


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
        self._userDB = UsersDB.UsersDB(self._connection)
        self._userDB.addUser("_TestUser" , "123")
        
    def tearDown(self):
        self._connection._execute('TRUNCATE users_files')
        self._connection._execute('TRUNCATE files')
        self._connection._execute('TRUNCATE users')
        self._connection.disconnect()
                
    def testAddUser(self):
        self._userDB.addUser("TestUser1" , 123)
        self._userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser1'")
        self.assertEqual({'username': 'TestUser1', 'salt': 'abcdefg', 'quota': 0, 'password_hash': '123'},self._userDB._conn._fetchOne())

    def testGetUser(self):
        self._userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser2', '456')")
        self.assertEqual({'username': 'TestUser2', 'salt': '', 'quota': None, 'password_hash': '456'},self._userDB.getUser('TestUser2'))

    def testUpdateUsername(self):
        self._userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser3', '789')")
        self._userDB.updateUsername('NewName','TestUser3', '789')
        self._userDB._conn._execute("SELECT * FROM users WHERE username = 'NewName'")
        self.assertEqual({'username': 'NewName', 'salt': '', 'quota': None, 'password_hash': '789'},self._userDB._conn._fetchOne())        

    def testUpdatePassword(self):
        self._userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser4', 'pass1')")
        self._userDB.updatePassword('new_pass', 'TestUser4', 'pass1')
        self._userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser4'")
        self.assertEqual({'username': 'TestUser4', 'salt': '', 'quota': None, 'password_hash': 'new_pass'},self._userDB._conn._fetchOne())

    def testRemoveUser(self):
        self._userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser5', 'pass2')")
        self._userDB.removeUser("TestUser5")
        self._userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser5'")
        self.assertEqual(None,self._userDB._conn._fetchOne())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

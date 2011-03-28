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
from database import FilesDB
import datetime


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
        self._connection._commit()
        self._connection.disconnect()
                
    def testUser(self):
        # note how getUser addUser and removeUser are all used to test each other
        self._userDB.addUser("_TestUser2" , "456")
        self.assertEqual({'username': '_TestUser2', 'salt': 'abcdefg', 'quota': 0L, 'password_hash': '456'}, self._userDB.getUser('_TestUser2'))
        self._userDB.removeUser("_TestUser2")
        self.assertEqual(None, self._userDB.getUser("_TestUser2"))
    
    def testAuthenticate(self):
        self.assertEqual(True, self._userDB.authenticate("_TestUser", "123"))
        self.assertEqual(False, self._userDB.authenticate("_TestUser", "wrongpass"))
        self.assertEqual(False, self._userDB.authenticate("_wronguser", "wrongpass"))
    
    def testUserExists(self):    
        self.assertEqual(True, self._userDB.userExists("_TestUser"))
        self.assertEqual(False, self._userDB.userExists("_RandomUser"))
    
    def testUpdateUsername(self):
        self._userDB.updateUsername('NewName','_TestUser')
        self.assertEqual({'username': 'NewName', 'salt': 'abcdefg', 'quota': 0L, 'password_hash': '123'},self._userDB.getUser("NewName"))        

    def testUpdatePassword(self):
        self._userDB.updatePassword('new_pass', '_TestUser', '123')
        self.assertEqual({'username': '_TestUser', 'salt': 'abcdefg', 'quota': 0L, 'password_hash': 'new_pass'},self._userDB.getUser("_TestUser"))
        
    def testUserQuota(self):
        self._userDB.setUserQuota(100 * 1024 * 1024 * 1024, "_TestUser")
        self.assertEqual(100 * 1024 * 1024 * 1024, self._userDB.getUserQuota("_TestUser"))

    def testGetSpaceRemaining(self):
        quota = 100 * 1024 * 1024 * 1024
        self._userDB.setUserQuota(quota, "_TestUser")
        fileDB = FilesDB.FilesDB(self._connection)
        fileDB.addFile("_TestUser", "/home/canada/32-c.bill", "/mnt/HD_a2/_TestUser/cRaZyHaShVaLuE/32-c.bill", 2048, "_TestUser", datetime.datetime(2011, 3, 26, 15, 6, 17), 1, "2b61cdf97336e06740df")
        fileDB.addFile("_TestUser", "/home/canada/human-rights.bill", "/mnt/HD_a2/_TestUser/cRaZyHaShVaLuE/human-rights.bill", 2048, "_TestUser", datetime.datetime(2011, 3, 26, 15, 6, 17), 1, "2b61chq97336e06740df")
        self.assertEqual(quota - (2 * 2048), self._userDB.getSpaceRemaining("_TestUser"))
        
    def testGetAllUser(self):
        userDB = self._userDB
        userTuples = (  {'username': "user1",'password_hash': '123', 'quota': 0, 'salt': "abcdefg"}
                      , {'username': "user2",'password_hash': '223', 'quota': 0, 'salt': "abcdefg"}
                      , {'username': "user3",'password_hash': '333', 'quota': 0, 'salt': "abcdefg"}
                      , {'username': "user4",'password_hash': '443', 'quota': 0, 'salt': "abcdefg"})
        self._addUsers(userDB, userTuples)
        userTuplesFromDB = userDB.getAllUser()
        userTuples += ({'username': "_TestUser",'password_hash': '123', 'quota': 0, 'salt': "abcdefg"},)
        self.assertEqual( userTuples, userTuplesFromDB)
        
    def _addUsers(self, userDB, userTuples):
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.addUser(user['username'] , user['password_hash'])
            index += 1
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

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
from UsersDB import *
from FilesDB import *
from DatabaseConnection import *

class FilesDBTest(unittest.TestCase):
    def setUp(self):
        self.connection = DatabaseConnection()
        
        # read data from config file, we don't want to be modifying this code  all the time
        config = ConfigParser.ConfigParser()
        config.readfp(open('../test/test-db.cfg'))
        DBHOST = config.get("Database", "host")
        DB = config.get("Database", "database")
        DBUSER = config.get("Database", "user")
        DBPASS = config.get("Database", "pass")
        
        self.connection.connect(DBHOST, DBUSER, DBPASS, DB)
        self.userDB = UsersDB(self.connection)
#        self.userDB.addUser("_TestUser" , 123)
#        self.userDB.addFile("_TestUser","testFile1","c:/folder1/folder2/testFile1.txt","_TestUser","NULL",1)
#        self.userDB.addFile("_TestUser","testFile2","c:/folder1/folder2/testFile2.txt","_TestUser","NULL",1)
        
    def tearDown(self):
#        self.userDB.removeFile("c:/folder1/folder2/testFile1.txt")
#        self.userDB.removeFile("c:/folder1/folder2/testFile2.txt")
#        self.userDB.removeUser("_TestUser")
        self.connection.disconnect()
        
    def testAddUser(self):
        self.userDB.addUser("_TestUser2" , 123)
        data = self.userDB.getUser("_TestUser2")
        self.assertEqual("_TestUser2",data[0])
        self.userDB.removeUser("_TestUser2")

    def testGetUser(self):
        self.assertTrue(True)

    def testUpdateUsername(self):
        self.assertTrue(True)        

    def testUpdatePassword(self):
        self.assertTrue(True)

    def testRemoveUser(self):
        self.assertTrue(True)

    def testGetFile(self):
        self.assertTrue(True)

    def testGetFiles(self):
        self.assertTrue(True)
        
    def testUpdateLastAuthor(self):
        self.assertTrue(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
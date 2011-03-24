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
        
        self.fileDB = FilesDB(self.connection)
        
    def tearDown(self):
        self.connection._execute('TRUNCATE users_files')
        self.connection._execute('TRUNCATE files')
        self.connection._execute('TRUNCATE users')
        self.connection.disconnect()

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
        
    def testGetServerPath(self):
        self.assertTrue(True)
        
    def testGetClientPath(self):
        self.userDB.addUser("_TestUser" , "123")
        self.fileDB.addFile("_TestUser","folder2/testFile1.txt", 35, "_TestUser","NULL",1)
        file = self.fileDB.getFile("_TestUser","folder2/testFile1.txt")
        self.assertEqual(self.fileDB.getClientPath(file[1]), "folder2/testFile1.txt")
        
    def testGetChecksum(self):
        self.assertTrue(True)
        
    def testGetLastModified(self):
        self.assertTrue(True)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
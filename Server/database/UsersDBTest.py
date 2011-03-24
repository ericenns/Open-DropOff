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

import UsersDB
import FilesDB
from DatabaseConnection import *


class UsersDBTest(unittest.TestCase):


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
        self.userDB = UsersDB.UsersDB(self.connection)
        self.userDB.addUser("_TestUser" , "123")
        
        self.fileDB = FilesDB.FilesDB(self.connection)
        self.fileDB.addFile("_TestUser","folder2/testFile1.txt", 35, "_TestUser","NULL",1)
#        self.userDB.addFile("_TestUser","testFile2","folder2/testFile2.txt","_TestUser","NULL",1)
       
    def tearDown(self):
        self.connection._execute('TRUNCATE users_files')
        self.connection._execute('TRUNCATE files')
        self.connection._execute('TRUNCATE users')
        self.connection.disconnect()
                
    def testAddUser(self):
        self.userDB.addUser("TestUser1" , 123)
        self.userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser1'")
        self.assertEqual(("TestUser1",'123',None,''),self.userDB._conn._fetchOne())

    def testGetUser(self):
        self.userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser2', '456')")
        self.assertEqual(("TestUser2",'456',None,''),self.userDB.getUser('TestUser2'))

    def testUpdateUsername(self):
        self.userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser3', '789')")
        self.userDB.updateUsername('NewName','TestUser3', '789')
        self.userDB._conn._execute("SELECT * FROM users WHERE username = 'NewName'")
        self.assertEqual(("NewName",'789',None,''),self.userDB._conn._fetchOne())        

    def testUpdatePassword(self):
        self.userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser4', 'pass1')")
        self.userDB.updatePassword('new_pass', 'TestUser4', 'pass1')
        self.userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser4'")
        self.assertEqual(("TestUser4",'new_pass',None,''),self.userDB._conn._fetchOne())

    def testRemoveUser(self):
        self.userDB._conn._execute("INSERT INTO users (username, password_hash) VALUES ('TestUser5', 'pass2')")
        self.userDB.removeUser("TestUser5")
        self.userDB._conn._execute("SELECT * FROM users WHERE username = 'TestUser5'")
        self.assertEqual(None,self.userDB._conn._fetchOne())

    def testGetFile(self):
        self.assertTrue(True)

    def testGetFiles(self):
        self.assertTrue(True)
        
    def testUpdateLastAuthor(self):
        self.assertTrue(True)
        
    def testPermissions(self):
        file = self.fileDB.getFile("_TestUser", "folder2/testFile1.txt")
        self.userDB.setPermission("_TestUser", file[1], 0)
        self.assertTrue(self.userDB.getPermission("_TestUser", file[1]) == 0)
        randomFileID = 3145156
        self.assertTrue(self.userDB.getPermission("_TestUser", randomFileID) == None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

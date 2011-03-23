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
                
    def test_Add_Get_Remove_User(self):
        userDB = self.userDB
        userDB.addUser("user1" , 123)
        
        data = self.userDB.getUser("user1")

        self.assertTrue( data[0] == "user1")
        self.assertTrue( data[1] == "123" )
        userDB.removeUser('user1')
        
        data = self.userDB.getUser("user1")
        self.assertTrue(data == None)
    
    def testUserExist(self):
        userDB = self.userDB
        userDB.addUser("user1", 123)
        value = userDB.userExists("user1")
        self.assertTrue( value == True )
        value = userDB.userExists("user123123")
        self.assertTrue( value == False )
        
    def testAuthenticate(self):
        userDB = self.userDB
        userDB.addUser("user1", "123")
        value = userDB.authenticate("user1" , "123")
        self.assertTrue( value == True)
        
        
    def testUpdateUsername(self):
        userDB = self.userDB
        userDB.addUser('user1', '123')
        
        userDB.updateUsername('user2', 'user1', '123')
        user = userDB.getUser('user2')
        self.assertTrue( user[0] == 'user2')
        user = userDB.getUser('user1')
        self.assertTrue( user == None)
        
        userDB.removeUser('user1') 

    def testUpdatePassword(self):
        userDB = self.userDB
        userDB.addUser('user1', '123')
        
        userDB.updatePassword('234' , 'user1', '123')
        user = userDB.getUser('user1')
        self.assertTrue( user[1] == '234')
        
        userDB.removeUser('user1')

    def testGetAllUser(self):
        userDB = self.userDB
        userTuples = (("user1", '123',0,0), ("user2", '223',0,0), ("user3", '323',0,0), ("user4", '423',0,0))
        self.addUsers(userDB, userTuples)
        userTuplesFromDB = userDB.getAllUser()
        self.verifyUsers(userTuples,userTuplesFromDB)

    def addUsers(self, userDB, userTuples):
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.addUser(user[0] , user[1])
            index += 1
    
    def verifyUsers(self, userTuples, userTuplesFromDB):
        index = 0
        for tuple in userTuples:
            tupleDB = userTuplesFromDB[index]
            self.assertTrue( tuple[0],tupleDB[0])
            self.assertTrue( tuple[1],tupleDB[1])
            index += 1
    '''
   
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

    '''

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
    

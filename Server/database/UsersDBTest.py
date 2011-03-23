'''
Created on Mar 19, 2011

@author: euwern
'''
import ConfigParser

import unittest
from DatabaseConnection import *
from UsersDB import *


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
        self.userDB = UsersDB(self.connection)
       
    def tearDown(self):
        self.userDB._conn._execute('TRUNCATE users')
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


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    

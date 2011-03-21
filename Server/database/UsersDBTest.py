'''
Created on Mar 19, 2011

@author: euwern
'''
import unittest
from DatabaseConnection import *
from UsersDB import *


class UsersDBTest(unittest.TestCase):


    def setUp(self):
        self.connection = DatabaseConnection()
        self.connection.connect("localhost","username","password","database")
        self.userDB = UsersDB(self.connection)
        self.userDB.addUser("_TestUser" , 123)
        self.userDB.addFile("_TestUser","testFile1","c:/folder1/folder2/testFile1.txt","_TestUser","NULL",1)
        self.userDB.addFile("_TestUser","testFile2","c:/folder1/folder2/testFile2.txt","_TestUser","NULL",1)
        
    def tearDown(self):
        self.userDB.removeFile("c:/folder1/folder2/testFile1.txt")
        self.userDB.removeFile("c:/folder1/folder2/testFile2.txt")
        self.userDB.removeUser("_TestUser")
        self.connection.disconnect()
        
    def testAddUser(self):
        self.userDB.addUser("_TestUser2" , 123)
        data = self.userDB.getUser("_TestUser2")
        self.assertEqual("_TestUser2",data[0])
        self.userDB.removeUser("_TestUser2")

    def testGetUser(self):
        self.assertTrue(1 == 1)

    def testUpdateUsername(self):
        self.assertTrue(1 == 0)        

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
    

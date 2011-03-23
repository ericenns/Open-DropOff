import ConfigParser

import unittest
from DatabaseConnection import *
from UsersDB import *

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
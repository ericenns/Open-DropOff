'''
Created on Mar 19, 2011

@author: euwern
'''
import unittest
from UsersDB import *
from FilesDB import *

class UsersDBTest(unittest.TestCase):


    def setUp(self):
        self.userDB = UsersDB("dummyConnection")


    def tearDown(self):
        pass


    def test_Add_Get_Remove_User(self):
        self.addAndTestUser(self.userDB)
        self.removeAndTestUser(self.userDB)
    
    def addAndTestUser(self, userDB):
        userDB.addUser('user1',123)
        user = userDB.getUser('user1')
        self.assertTrue( user['username'] == 'user1')
        self.assertTrue( user['password_hash'] == 123 )        
    
    def removeAndTestUser(self, userDB):
        userDB.removeUser('user1')
        user = userDB.getUser('user1')
        self.assertTrue(user == None)        
    
    def testUserExists(self):
        userDB = self.userDB
        userDB.addUser('user1','123')
        self.assertTrue(True == userDB.userExists('user1'))
        self.assertTrue(False == userDB.userExists('user123'))
        userDB.removeUser('user1')

    def testAuthenticate(self):
        userDB = self.userDB
        userDB.addUser('user1', '123')
        value = userDB.authenticate('user1','123')
        self.assertTrue(value == True)
        value = userDB.authenticate('user1','234')
        self.assertTrue(value == False)
        userDB.removeUser('user1')
    
    def testUpdateUsername(self):
        userDB = self.userDB
        userDB.addUser('user1', '123')
        
        userDB.updateUsername('user2', 'user1', '123')
        user = userDB.getUser('user2')
        self.assertTrue( user['username'] == 'user2')
        user = userDB.getUser('user1')
        self.assertTrue( user == None)
        
        userDB.removeUser('user1')

    def testUpdatePassword(self):
        userDB = self.userDB
        userDB.addUser('user1', '123')
        
        userDB.updatePassword('234' , 'user1', '123')
        user = userDB.getUser('user1')
        self.assertTrue( user['password_hash'] == '234')
        
        userDB.removeUser('user1')

    def testGetAllUser(self):
        userDB = self.userDB
        userTuples = (  {'username': "user1",'password_hash': '123', 'quota': 0, 'salt': 0}
                      , {'username': "user2",'password_hash': '223', 'quota': 0, 'salt': 0}
                      , {'username': "user3",'password_hash': '333', 'quota': 0, 'salt': 0}
                      , {'username': "user4",'password_hash': '443', 'quota': 0, 'salt': 0})
        self.addUsers(userDB, userTuples)
        userTuplesFromDB = userDB.getAllUser()
        self.assertTrue( userTuples == userTuplesFromDB)
        self.removeAllUsers(userDB, userTuples)

    def addUsers(self, userDB, userTuples):
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.addUser(user['username'] , user['password_hash'])
            index += 1
    
    def removeAllUsers(self, userDB, userTuples):   
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.removeUser(user['username'])
            index += 1        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
'''
Created on Mar 19, 2011

@author: euwern
'''
import unittest
from UsersDBStub import *
from FilesDBStub import *

class UsersDBStubTest(unittest.TestCase):


    def setUp(self):
        self.userDB = UsersDBStub("dummyConnection")


    def tearDown(self):
        pass


    def test_Add_Get_Remove_User(self):
        self.addAndTestUser(self.userDB)
        self.removeAndTestUser(self.userDB)
    
    def addAndTestUser(self, userDB):
        userDB.addUser('user1',123)
        user = userDB.getUser('user1')
        self.assertTrue( user[0] == 'user1')
        self.assertTrue( user[1] == 123 )        
    
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
        self.assertTrue( userTuples == userTuplesFromDB)
        self.removeAllUsers(userDB, userTuples)

    def addUsers(self, userDB, userTuples):
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.addUser(user[0] , user[1])
            index += 1
    
    def removeAllUsers(self, userDB, userTuples):   
        index = 0
        while (index < len( userTuples ) ):
            user = userTuples[index]
            userDB.removeUser(user[0])
            index += 1        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
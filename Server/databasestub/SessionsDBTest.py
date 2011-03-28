'''
Created on 2011-03-28

@author: Marilyn Hacko
'''
import unittest
import datetime
from SessionsDB import *

class SessionsDBTest(unittest.TestCase):

    def setUp(self):
        self._sessionsDB = SessionsDB("dummyConnection")

    def addAndTestSession(self, userDB):
        self._sessionsDB.createSession('440f23c58848769685e481ff270b046659f40b7c' , 'user1', '216.27.61.137', datetime.datetime.now())
        session = self._sessionsDB.getSession('440f23c58848769685e481ff270b046659f40b7c')
        self.assertTrue( session['username'] == 'user1')
        self.assertTrue( session['ip_address'] == '216.27.61.137')        
    
    def removeAndTestUser(self, userDB):
        userDB.removeUser('user1')
        user = userDB.getUser('user1')
        self.assertTrue(user == None)        
    
    def testUserExists(self):
        userDB = self._userDB
        userDB.addUser('user1','123')
        self.assertTrue(True == userDB.userExists('user1'))
        self.assertTrue(False == userDB.userExists('user123'))
        userDB.removeUser('user1')

    def testAuthenticate(self):
        userDB = self._userDB
        userDB.addUser('user1', '123')
        value = userDB.authenticate('user1','123')
        self.assertTrue(value == True)
        value = userDB.authenticate('user1','234')
        self.assertTrue(value == False)
        userDB.removeUser('user1')


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
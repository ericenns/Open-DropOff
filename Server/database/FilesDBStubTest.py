'''
Created on Mar 19, 2011

@author: euwern
'''
import unittest
from UsersDBStub import *
from FilesDBStub import *

class FilesDBStubTest(unittest.TestCase):


    def setUp(self):
        self.fileDB = FilesDBStub("dummyConnection")

    def tearDown(self):
        pass

    def testName(self):
        pass
          
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
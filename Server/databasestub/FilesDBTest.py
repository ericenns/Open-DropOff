'''
Created on Mar 19, 2011

@author: euwern
'''
import unittest
from UsersDB import *
from FilesDB import *

class FilesDBStubTest(unittest.TestCase):


    def setUp(self):
        self.fileDB = FilesDB("dummyConnection")
        self.fileDB.addFile("_TestUser","folder2/testFile1.txt", 35, "_TestUser","NULL",1, 0)
        self.fileDB.addFile("_TestUser","folder2/testFile2.txt", 35, "_TestUser","NULL",1, 0)

    def tearDown(self):
        pass

    def testAddFile(self):
        pass
    
    def testGetFile(self):
        self.assertTrue({'username': "_TestUser", 'client_path': "folder2/testFile1.txt", 'server_path': 35, 'last_author': "_TestUser", 'last_modified': "NULL", 'version': 1}, \
                        self.fileDB.getFile("_TestUser", "folder2/testFile1.txt"))
    
    def testGetAllFiles(self):
        files = self.fileDB.getAllFiles("_TestUser")
        self.assertTrue(files[0]['client_path'], "folder2/testFile1.txt")
        self.assertTrue(files[1]['client_path'], "folder2/testFile2.txt")
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
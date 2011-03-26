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
import unittest
from UsersDB import *
from FilesDB import *

class FilesDBTest(unittest.TestCase):
    '''
    
    '''

    def setUp(self):
        self._fileDB = FilesDB("dummyConnection")
        self._fileDB.addFile("_TestUser","folder2/testFile1.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", 35, "_TestUser","NULL",1, 0)
        self._fileDB.addFile("_TestUser","folder2/testFile2.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile2.txt", 35, "_TestUser","NULL",1, 0)

    def tearDown(self):
        pass
    
    def testFile(self):
        self._fileDB.addFile("_TestUser","folder5/testFile1.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", 35, "_TestUser", "NULL", 1, 0)
        self.assertTrue({'username': "_TestUser", 'client_path': "folder5/testFile1.txt", 'server_path': "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", 'last_author': "_TestUser", 'last_modified': "NULL", 'version': 1}, \
                        self._fileDB.getFile("_TestUser", "folder5/testFile1.txt"))
        self._fileDB.removeFile("_TestUser", "folder5/testFile1.txt")

    def testGetFilesInDir(self):
        files = self._fileDB.getFilesInDir("folder2/", "_TestUser")
        self.assertTrue(files[0]['client_path'], "folder2/testFile1.txt")
        self.assertTrue(files[1]['client_path'], "folder2/testFile2.txt")

    def testGetAllFiles(self):
        files = self._fileDB.getAllFiles("_TestUser")
        self.assertTrue(files[0]['client_path'], "folder2/testFile1.txt")
        self.assertTrue(files[1]['client_path'], "folder2/testFile2.txt")
        
    def testUpdateLastAuthor(self):
        self.assertTrue(True)
        
    def testGetServerPath(self):
        self.assertTrue(True)
        
    def testGetClientPath(self):
        file = self._fileDB.getFile("_TestUser","folder2/testFile1.txt")
        self.assertEqual(file['client_path'], "folder2/testFile1.txt")
        
    def testGetChecksum(self):
        self.assertTrue(True)
        
    def testGetLastModified(self):
        self.assertTrue(True)
                
    def testPermissions(self):
        file = self._fileDB.getFile("_TestUser", "folder2/testFile1.txt")
        self._fileDB.setPermission("_TestUser", file['file_id'], 0)
        self.assertTrue(self._fileDB.getPermission("_TestUser", file['file_id']) == 0)
        randomFileID = 3145156
        self.assertTrue(self._fileDB.getPermission("_TestUser", randomFileID) == None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
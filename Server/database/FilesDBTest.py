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
import datetime

from UsersDB import *
from FilesDB import *
from DatabaseConnection import *

class FilesDBTest(unittest.TestCase):
    def setUp(self):
        self._connection = DatabaseConnection()
        
        # read data from config file, we don't want to be modifying this code  all the time
        config = ConfigParser.ConfigParser()
        config.readfp(open('../test/test-db.cfg'))
        DBHOST = config.get("Database", "host")
        DB = config.get("Database", "database")
        DBUSER = config.get("Database", "user")
        DBPASS = config.get("Database", "pass")
        
        self._connection.connect(DBHOST, DBUSER, DBPASS, DB)
        self._userDB = UsersDB(self._connection)
        
        self._fileDB = FilesDB(self._connection)
        self._userDB.addUser("_TestUser" , "123")
        self._fileDB.addFile("_TestUser","folder2/testFile1.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", 35, "_TestUser","NULL",1, "2b61cdf97336e06720df")
        self._fileDB.addFile("_TestUser","folder2/testFile2.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile2.txt", 35, "_TestUser","NULL",1, "4bd950f32db28f05d972")
        
    def tearDown(self):
        self._connection._execute('TRUNCATE users_files')
        self._connection._execute('TRUNCATE files')
        self._connection._execute('TRUNCATE users')
        self._connection.disconnect() 

    def testFile(self):
        fileId = self._fileDB.addFile("_TestUser","folder5/testFile1.txt", "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", 35, "_TestUser", datetime.datetime(2011, 3, 26, 15, 6, 17), 1, "2b61cdf97336e06720df")
        self.assertEqual({'username': "_TestUser",
                          'file_id': fileId, \
                          'f.file_id': fileId, \
                          'client_path': "folder5/testFile1.txt", \
                          'server_path': "/mnt/HD_a2/_TestUser/f3bfa/testFile1.txt", \
                          'size': 35, \
                          'last_author': "_TestUser", \
                          'last_modified': datetime.datetime(2011, 3, 26, 15, 6, 17), \
                          'version': 1, \
                          'deleted': 0, \
                          'permission_level': 0,
                          'directory': 0, \
                          'checksum': "2b61cdf97336e06720df"}, \
                        self._fileDB.getFile("_TestUser", "folder5/testFile1.txt"))
        self._fileDB.removeFile("_TestUser", "folder5/testFile1.txt")
        self.assertEqual(None, self._fileDB.getFile("_TestUser", "folder5/testFile1.txt"))

    def testGetFilesInDir(self):
        files = self._fileDB.getFilesInDir("folder2/", "_TestUser")
        self.assertEqual(files[0]['client_path'], "folder2/testFile1.txt")
        self.assertEqual(files[1]['client_path'], "folder2/testFile2.txt")

    def testGetAllFiles(self):
        files = self._fileDB.getAllFiles("_TestUser")
        self.assertEqual(files[0]['client_path'], "folder2/testFile1.txt")
        self.assertEqual(files[1]['client_path'], "folder2/testFile2.txt")
        
    def testUpdateLastAuthor(self):
        self._fileDB.updateLastAuthor(path, newAuthor)
        
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
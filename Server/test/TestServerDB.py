###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Eric Enns                                                                #
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

import os
import sys

import unittest

import ConfigParser

sys.path.append("%s/" % os.path.split(os.getcwd())[0])

from databasestub import *

try: 
    from hashlib import sha1
    sha_constructor = sha1
except ImportError:
    import sha
    sha_constructor = sha.new
   
config = ConfigParser.ConfigParser()
config.readfp(open('odo-serverdb.cfg'))
   
class TestServerDB(unittest.TestCase):
    
    def setUp(self):
        self.conn = DatabaseConnection.DatabaseConnection()
        self.dbhost = config.get("Database", "host")
        self.dbuser = config.get("Database", "user")
        self.dbpass = config.get("Database", "pass")
        self.db = config.get("Database", "database")
        self.conn.connect(self.dbhost, self.dbuser, self.dbpass, self.db)
        self.udb = UsersDB.UsersDB(self.conn)
        
    def tearDown(self):
        self.conn.disconnect()
        
    def test_createUserAndLoginAndChangePass(self):
        nameTaken = self.udb.userExists("user")
        self.assertFalse(nameTaken)
        self.udb.addUser("user", "pass")
        nameTaken = self.udb.userExists("user")
        self.assertTrue(nameTaken)
        
        validPass = self.udb.authenticate("user", "pass")
        self.assertTrue(validPass)
        
        self.udb.updatePassword("newpass", "user", "pass")
        validPass = self.udb.authenticate("user", "newpass")
        self.assertTrue(validPass)
        
    def test_list(self):
        pass
    
    def test_receive(self):
        pass
    
    def test_send(self):
        pass
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestServerDB)
    unittest.TextTestRunner(verbosity=2).run(suite)
        
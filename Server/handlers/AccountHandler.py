###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Eric Enns                                                                #
#    Travis Martindale                                                        #
#    Andrew Matsuaka                                                          #
#    Chris Janssens                                                           #
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

import time
import datetime

try: 
    from hashlib import sha1
    sha_constructor = sha1
except ImportError:
    import sha
    sha_constructor = sha.new

from database import *
#from databasestub import *

class AccountHandler(object):
    '''
    classdocs
    '''

    def __init__(self, conn, dbconn, sdb):
        '''
        Constructor
        '''
        self.connHandler = conn
        self.dbConnection = dbconn
        self.udb = UsersDB.UsersDB(dbconn)
        self.sdb = sdb;
    
    def createNewUser(self, arguments):
        newuser, newpass = arguments.split("\r\n")
        print "New user: %s" % newuser
        print "new pass: %s" % newpass
        
        nameTaken = self.udb.userExists(newuser)
        if not nameTaken:
            meetsReq = True
            #meetsReq = checkPassReq(newpass)
            if meetsReq:
                self.udb.addUser(newuser, newpass, 1000)
                self.connHandler.send("STAT\r\n100")
            else:
                self.connHandler.send("STAT\r\n204")
        else:
            print "Name taken, try again!"
            self.connHandler.send("STAT\r\n203")
            

    def changePassword(self, newpass, oldpass, user):
        #newpass, oldpass, key = arguments.split("\r\n", 3)
        
        if(user != None):
            print oldpass
            print newpass
            self.udb.updatePassword(newpass, user, oldpass)
            self.connHandler.send("STAT\r\n100")
        else:
            self.connHandler.send("STAT\r\n200")
            return
    
    def checkPassReq(self, newpass):
        if len(newpass) > 8:
            return True
        else:
            return False
        
    def generateKey(self, username, ipAddr):
        #ipAddr = self.connHandler.clientAddr()
        #time = time.time()
        #ipAddr = "172.0.0.1"
        #time = "1234567"
        time = datetime.datetime.now()
        key = sha_constructor("%s%s%s" 
                              % (username, ipAddr
                                 , time)).hexdigest()
                                 
        return key
        
    def login(self, arguments):
        username = arguments
        print "User: %s" % username
        
        validUser = self.udb.userExists(username)
        
        if(validUser):
        #if(username == "user"):
            self.connHandler.send("STAT\r\n100")
            self.data = self.connHandler.recv()
            command, arguments = self.data.split("\r\n", 1)
            
            if(command == "PASS"):
                password = arguments
                print password
                validPass = self.udb.authenticate(username, password)
                if(validPass):
                #if(password == "pass"):
                    ipAddr = self.connHandler.clientAddr
                    expiry = datetime.datetime(2050,1,1)
                    key = self.generateKey(username, ipAddr)
                    self.sdb.createSession(key, username, ipAddr, expiry)
                    self.connHandler.send("STAT\r\n100\r\n%s" % key)
                else:
                    self.connHandler.send("STAT\r\n202")
            else:
                #not sure if this is needed
                self.connHandler.send("FAIL")
        else:
            self.connHandler.send("STAT\r\n201")
            
        

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

    def __init__(self, conn, udb, sdb):
        '''
        Constructor
        '''
        self.connHandler = conn
        self.udb = udb
        self.sdb = sdb
    
    def createNewUser(self, arguments):
        newuser, newpass = arguments.split("\r\n")
        print "New user: %s" % newuser
        print "new pass: %s" % newpass
        
        nameTaken = self.udb.userExists(newuser)
        if not nameTaken:
            meetsReq = True
            if meetsReq:
                self.udb.addUser(newuser, newpass, 1048576000)
                self.connHandler.send("STAT\r\n100")
            else:
                self.connHandler.send("STAT\r\n204")
        else:
            print "Name taken, try again!"
            self.connHandler.send("STAT\r\n203")
            

    def changePassword(self, newpass, oldpass, user):
        
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
            self.connHandler.send("STAT\r\n100")
            self.data = self.connHandler.recv()
            command, arguments = self.data.split("\r\n", 1)
            
            if(command == "PASS"):
                password = arguments
                print password
                validPass = self.udb.authenticate(username, password)
                if(validPass):
                    ipAddr = self.connHandler.clientAddr[0]
                    extension = datetime.timedelta(seconds=43200)
                    expiry = datetime.datetime.now() + extension
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
            
    def spaceRemaining(self, username):
        validUser = self.udb.userExists(username)
        if(validUser):
            qouta = self.udb.getUserQuota(username)
            remaining = self.udb.getSpaceRemaining(username)
            self.connHandler.send("STAT\r\n100\r\n%s\r\n%s" % (qouta, remaining))
        else:
            self.connHandler.send("STAT\r\n201")
        

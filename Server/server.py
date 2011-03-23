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

import os
import sys
import re

import SocketServer
import ConfigParser

try: 
   from hashlib import sha1
   sha_constructor = sha1
except ImportError:
   import sha
   sha_constructor = sha.new
#from database import *

RECEIVESIZE = 100
SENDSIZE = 100

config = ConfigParser.ConfigParser()
config.readfp(open('odo-server.cfg'))

class ODOTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        # get the protocol option
        while(1):
            self.data = self.request.recv(80)
            try:
                print "TEST11"
                command, arguments = self.data.split("\r\n", 1)
                print "TEST12"
                print "\nCommand:\t%s" % command
                if(command == "NUSR"):
                    self.createNewUser(arguments)
                elif(command == "USER"):
                   self.login(arguments)
                elif(command == "PUSH"):
                   self.receive(arguments)
                elif(command == "PULL"):
                   self.send(arguments)
                elif(command == "CLOS"):
                   print "Connection with Client closed"
                   break
            except ValueError:
                print "Connection with Client lost"
                break
            
        self.request.close()
        
    def createNewUser(self, arguments):
        newuser, newpass = arguments.split("\r\n")
        print "New user: %s" % newuser
        print "new pass: %s" % newpass
        
        #conn = DatabaseConnection()
        #conn.connect("localhost", "username", "password", "open-dropoff")
        #udb = UsersDB(conn)
        
        #nameTaken = udb.userExists(newuser)
        #if not nameTaken:
        #    meetsReq = checkPassReq(newpass)
        #    if meetsReq:
        #        udb.addUser( newuser, newpass )
        #        self.request.send("STAT 100")
        #    else:
        #        self.request.send("STAT 204")
        #else:
        #    print "Name taken, try again!"
        #    self.request.send("STAT 203")
        
        #conn.disconnect()
    
    def checkPassReq(self, newpass):
        if len(newpass) > 8:
            return True
        else:
            return False
        
    def login(self, arguments):
        username = arguments
        print "User: %s" % username
        #conn = DatabaseConnection.DatabaseConnection()
        #conn.connect(DBHOST, DBUSER, DBPASS, DB)
        #udb = UsersDB.UsersDB(conn)
        
        #validUser = udb.userExists(username)
        
        #if(validUser):
        if(username == "user"):
            self.request.send("STAT\r\n100")
            self.data = self.request.recv(RECEIVESIZE)
            command, arguments = self.data.split("\r\n", 1)
            
            if(command == "PASS"):
                password = arguments
                
                #validPass = udb.authenticate(username, password)
                #if(validPass):
                if(password == "pass"):
                    key = sha_constructor("%s%s" % (username, password)).hexdigest()
                    self.request.send("STAT\r\n100\r\n%s" % key)
                else:
                    self.request.send("STAT\r\n202")
            else:
                #not sure if this is needed
                self.request.send("FAIL")
        else:
            self.request.send("STAT\r\n201")
            
        #conn.disconnect()
            
    def receive(self, arguments):
        filename, filesize, key = arguments.split("\r\n", 2)
        print "FILENAME: %s" % filename
        filesize = int(filesize)
        
        #verify key
        if(key == "45f106ef4d5161e7aa38cf6c666607f25748b6ca"):
            self.request.send("STAT\r\n100")
        else:
            self.request.send("FAIL")
            return
        
        #authenticate user information
        #self.data = self.request.recv(80)
        #userN, password = self.data.split("\r\n", 1)
        
        #verify user
        
        #verity password
        
        #write the files to a test sub-directory prevents 
        #clogging up the server folder with random test files
        #newfile = open("./testfiles/" + filename, "wb")
        
        filename_hash = sha_constructor(filename).hexdigest()
        fullpath = "%s%s%s" % (BASEDIR,FILEDIR,filename_hash)
        if(os.path.isfile(fullpath)):
            print "File already exists"
        newfile = open(fullpath, "wb")
        #receives 100 bytes of the file at a time, loops until
        #the whole file is received
        totalReceived = -1
        
        print filesize
        
        while totalReceived <= filesize:
            if( totalReceived == -1 ):
                totalReceived =  0
            print "looping"
            content = self.request.recv(RECEIVESIZE)
            totalReceived += RECEIVESIZE
            newfile.write(content)

        newfile.close() #close the file
        
        #send a response to the client
        self.request.send("STAT\r\n100")
        print "PUSH Request finished"


    def send(self, arguments):
        filename, key = arguments.split("\r\n", 1)
        if(key == "45f106ef4d5161e7aa38cf6c666607f25748b6ca"):
            filename_hash = sha_constructor(filename).hexdigest()
            fullpath = "%s%s%s" % (BASEDIR,FILEDIR,filename_hash)
        
            filesize = os.path.getsize(fullpath)
        
            self.request.send("STAT\r\n100\r\n%i" % filesize)
        else:
            self.request.send("FAIL\r\n101")
            return
            
        response = self.request.recv(80)
        
        if response == "SEND":
            #start sending the file
            
            file = open(fullpath, "rb")
            
            line = file.read(SENDSIZE)
            
            while line:
                sent = self.request.send(line)
                while sent != len(line):
                    sent += self.request.send(line[sent:])
                line = file.read(SENDSIZE)
            
            file.close()
        else:
            print "Don't send."
        print "PULL Request finished"
             
if __name__ == "__main__":
    #HOST, PORT = "localhost", 30000
    HOST = config.get("Network", "host")
    PORT = config.getint("Network", "port")
    BASEDIR = config.get("Storage", "basedir")
    FILEDIR = config.get("Storage", "files")
    DBHOST = config.get("Database", "host")
    DB = config.get("Database", "database")
    DBUSER = config.get("Database", "user")
    DBPASS = config.get("Database", "pass")

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), ODOTCPHandler)
    
    #connect to user database
    #userconnect = DatabaseConnection.__init__()
    #userconnect.connect(HOST,"User","Pass","UsersDB")
    #userdb = UsersDB.__init__(userconnect)
    #userdb.connect()

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Running..."
    #server.timeout = 60
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    

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
import socket

try: 
    from hashlib import sha1
    sha_constructor = sha1
except ImportError:
    import sha
    sha_constructor = sha.new

RECEIVESIZE = 100
SENDSIZE = 100
key = 0;

class RequestController(object):
    '''
    classdocs
    '''
    
    def __init__(self, server, port):
        self.server = server
        self.port = int(port)
        #TODO: THIS IS VERY BAD. Only here for getting things running
        self.key = "45f106ef4d5161e7aa38cf6c666607f25748b6ca"


    def connect(self):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )  # create a TCP socket
        
        try:
            self.sock.connect((self.server, self.port)) # connect to server on the port
        except:
            print "Unable to connect to server specified. %s" % self.server
    
    
    def disconnect(self):
        self.sock.send("CLOS\r\n")
        self.sock.close()
        
        
    def close(self):
        self.connect()
        self.sock.send("CLOS\r\n")
        self.disconnect()
        
        
    def changePassword(self, password):
        self.connect()
        print "changePassword(RC)p: %s" % password
        print "key: %s" % self.key
        self.sock.send("PASS\r\n%s\r\n%s" % (password, self.key))
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        print "%s %s" % (status, code)
        
        password_hash = sha_constructor(password).hexdigest()
        print "Password hash: %s" % password_hash    
    
        self.disconnect()
        
        

        
    #Creates a new user with the given information:
    #params:    username    name to be used for new user
    #            password    password for the new user
    #returns: true if user creation was successful, false if not
    def newUser(self, username, password):
        self.connect()
        
        print "newUser(RC)u: %s" % username
        print "newUser(RC)p: %s" % password
        
        self.sock.send("NUSR\r\n%s\r\n%s" % (username, password))
        
        response = self.sock.recv(RECEIVESIZE)
        
        if( response == "STAT 100"):
            print "New user made!"
            return True
        else:
            print "Unable to create user"
            return False
        
        self.disconnect()


    def login(self):
        self.connect()
        
        #Simply data access for initial use
        username = raw_input("Please enter your username: ")
        print username
        ##################Can be removed^^^
        
        self.sock.send("USER\r\n%s" % username)
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        print "%s %s" % (status, code)
        if(status == "STAT" and code == "100"):
            password = raw_input("Please enter your password: ")
            self.sock.send("PASS\r\n%s" % password)
            response = self.sock.recv(RECEIVESIZE)
            status, code, key = response.split("\r\n",2)
            if(status == "STAT" and code =="100"):
                self.key = key
            else:
                return "";
        else:
            return "";
        
        self.disconnect()
        
        
    #Sends a listing of contents request to connection
    #params:    sock    connection to send list request to
    #Returns: list of items returned by the server
    #def list(self, key):
    def list(self):
        self.connect()
        print "IN LIST, RC"
        self.sock.send("LIST\r\n")
        self.disconnect()
        #should figure out what format contents list should have
        #contentsList = self.sock.recv(RECEIVESIZE)
        
        #return contentsList
        
        
    #send file to server
    #params:    sock    connection to have file sent through
    #            filename    name of file to be sent
    #            filesize    size of file being sent
    def push(self, filename, filesize):
        self.connect()
        
        f = open(filename,"rb")
        self.sock.send("PUSH\r\n%s\r\n%i\r\n%s" % (filename, filesize, self.key))
        # wait for a response then start sending the file
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        if(status == "STAT" and code == "100"):
            print "%s %s" % (status, code)
        else:
            return
        
        #sock.send("%s\r\n%s" % ("JohnDoe","homie4life"))
        
        line = f.read(SENDSIZE)
        while line:
            sent = self.sock.send(line)
            while sent != len(line):
                sent += self.sock.send(line[sent:])
            line = f.read(SENDSIZE)
        f.close()
        
        data = self.sock.recv(80)
        print data
        
        self.disconnect()

        
    #Send a request for a file to be pulled from connection
    #params:    key    key that confirms identity of request sender
    #            filename    name of file to be pulled and saved
    #Returns: File data
    def pull(self, filename):
        self.connect()
        self.sock.send("PULL\r\n%s\r\n%s" % (filename, self.key))
        response = self.sock.recv(80)
        status, code, filesize = response.split("\r\n", 2)
        filesize = int(filesize)
        if(status == "STAT" and code == "100"):
            self.sock.send("SEND")
            newfile = open(filename, "wb")
            totalReceived = -1
            
            while totalReceived <= filesize:
                if( totalReceived == -1 ):
                    totalReceived =  0
                
                content = self.sock.recv(RECEIVESIZE)
                totalReceived += RECEIVESIZE
                newfile.write(content)
            
            newfile.close() #close the file
            self.disconnect()
        else:
            print "FAILURE!"

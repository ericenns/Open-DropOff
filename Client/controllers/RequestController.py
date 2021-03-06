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
CHECKREADSIZE = 128
key = 0;

class RequestController(object):
    '''
    classdocs
    '''
    
    def __init__(self, server, port):
        self.server = server
        self.port = int(port)
        self.key = "0"


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
        #self.connect()
        self.sock.send("CLOS\r\n")
        #self.disconnect()
        
        
    def changePassword(self, newpass, oldpass):
        #self.connect()
        newpass_hash = sha_constructor(newpass).hexdigest()
        oldpass_hash = sha_constructor(oldpass).hexdigest()
        print self.key
        self.sock.send("PASS\r\n%s\r\n%s\r\n%s" % (newpass_hash, oldpass_hash, self.key))
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        print "%s %s" % (status, code)  
    
        #self.disconnect()
        
        
    #Creates a new user with the given information:
    #params:    username    name to be used for new user
    #            password    password for the new user
    #returns: true if user creation was successful, false if not
    def newUser(self, username, password):
        #self.connect()
        
        print "newUser(RC)u: %s" % username
        print "newUser(RC)p: %s" % password
        password_hash = sha_constructor(password).hexdigest()
        self.sock.send("NUSR\r\n%s\r\n%s" % (username, password_hash))
        
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        
        if(status == "STAT" and code == "100"):
            print "New user made!"
            return True
        else:
            print "Unable to create user"
            return False
        
        #self.disconnect()

    def sendUser(self, username):
        self.sock.send("USER\r\n%s" % username)
        response = self.sock.recv(RECEIVESIZE)
        
        return response
    
    def sendPass(self, password):
        password_hash = sha_constructor(password).hexdigest()
        print password_hash
        self.sock.send("PASS\r\n%s" % password_hash)
        response = self.sock.recv(RECEIVESIZE)
        
        return response

    #Ideally you would pass in the username and password to this function
    #    instead of having it entered in using raw_input()
    def login(self, username, password):
        #self.connect()
        response = self.sendUser(username)
        status, code = response.split("\r\n", 1)
        
        if(status == "STAT" and code == "100"):
            response = self.sendPass(password)
            status, code = response.split("\r\n",1)
            
            if(status == "STAT" and code[:3] =="100"):
                code, key = code.split("\r\n",1)
                self.key = key
            else:
                return "Password is invalid";
        else:
            return "";
        
        #self.disconnect()
        
    def responseOK(self, response):
        status, code = response.split("\r\n",1)
        
        if status == "STAT" and code == "100":
            return True
        else:
            return False
        
    #Sends a listing of contents request to connection
    #params:    sock    connection to send list request to
    #Returns: list of items returned by the server
    def listAll(self):
        self.sock.send("LIST\r\n%s" % self.key)

        response = self.sock.recv(9)
        
        if(self.responseOK(response)):
            checkEnd = ""
            responseString = ""
            #responseBuild = []
            while(not checkEnd == "STAT\r\n100"):
                response = self.sock.recv(RECEIVESIZE)
                responseString = responseString + response;
                checkEnd = responseString[-9:]
                #checkEnd = response[-9:]
                if(checkEnd == "STAT\r\n100"):
                    responseString = responseString[:-9]
                    #response = response[:-9]
                #responseBuild.append(response)
            return self.ResponseMessageToListFiles(responseString)
            #return self.ResponseMessageToListFiles(''.join(responseBuild))
        else:
            return ""
                    
        #return self.ResponseMessageToListFiles(''.join(responseBuild))
    

    #Sends a listing of contents request to connection
    #params:    sock    connection to send list request to
    #           clientPath the file to return versions for
    #Returns: list of versions returned by the server
    def listVersions(self, clientPath):
        self.sock.send("LIST\r\n%s\r\n%s" % (self.key, clientPath))
        
        response = self.sock.recv(9)
        responseString = ""
        
        if(self.responseOK(response)):
            checkEnd = ""
            #responseBuild = []
            while(not checkEnd == "STAT\r\n100"):
                response = self.sock.recv(RECEIVESIZE)
                responseString = responseString + response;
                print "responseString = %s" % responseString
                checkEnd = responseString[-9:]
                print checkEnd
                #checkEnd = response[-9:]
                if(checkEnd == "STAT\r\n100"):
                    responseString = responseString[:-9]
                    #response = response[:-9]
                #responseBuild.append(response)
         
        return self.ResponseMessageToListVersions(responseString)           
        #return self.ResponseMessageToListVersions(''.join(responseBuild))
    
    
    def ResponseMessageToListFiles(self, response):
        files = response.split("\r\n")
        dictList = []
        
        for file in files:
            if not file == "":
                clientPath, checksum, date, size = file.split("\t")
                newFile = {'clientPath':clientPath, 'checksum':checksum, 'dateModified':date , 'size':size}
                dictList.append(newFile)
            
        return dictList
    
    
    def ResponseMessageToListVersions(self, response):
        versions= response.split("\r\n")
        dictList = []
        
        for version in versions:
            if not version == "":
                clientPath, version, date, size = version.split("\t")
                newVersion = {'clientPath':clientPath, 'version':version, 'date':date, 'size':size}
                dictList.append(newVersion)
            
        return dictList
    
        
    def computeChecksum(self, filename):
        file_hash = sha_constructor()
        
        file = open(filename, "rb")
        line = file.read(128)
        while line:
            file_hash.update(line)
            line = file.read(128)
        file.close()
        
        return file_hash.hexdigest()
        
    #send file to server
    #params:    sock    connection to have file sent through
    #            filename    name of file to be sent
    #            filesize    size of file being sent
    def push(self, filename, filesize):
        #self.connect()
        
        checksum = self.computeChecksum(filename)
        self.sock.send("PUSH\r\n%s\r\n%i\r\n%s\r\n%s" % (filename, filesize, checksum, self.key))
        # wait for a response then start sending the file
        response = self.sock.recv(RECEIVESIZE)
        status, code = response.split("\r\n", 1)
        if(status == "STAT" and code == "100"):
            print "%s %s" % (status, code)
        else:
            return
        
        f = open(filename,"rb")
        line = f.read(SENDSIZE)
        while line:
            sent = self.sock.send(line)
            while sent != len(line):
                sent += self.sock.send(line[sent:])
            line = f.read(SENDSIZE)
        f.close()
        
        data = self.sock.recv(80)
        print data
        
        #self.disconnect()

        
    #Send a request for a file to be pulled from connection
    #params:    key    key that confirms identity of request sender
    #            filename    name of file to be pulled and saved
    #Returns: File data
    def pull(self, filename, version=0):
        #self.connect()
        self.sock.send("PULL\r\n%s\r\n%s\r\n%s" % (filename, version, self.key))
        
        response = self.sock.recv(80)
        values = response.split("\r\n")
        #status, code, filesize = response.split("\r\n")
        status = values[0]
        code = values[1]
        filesize = 0
        if len(values) == 3:
            filesize = int(values[2])
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
            print "File Received"
            #self.disconnect()
        else:
            print "FAILURE!"
            
    
    #Removes file with matching filename
    #params:    sock    connection to send list request to
    #Returns: list of items returned by the server
    def removeFile(self, filename):
        #self.connect()
        print "IN REMV, RC"
        self.sock.send("REMV\r\n%s\r\n%s" % (filename, self.key))
        #self.disconnect()

    def qoutaAndSpaceRemaining(self):
        self.sock.send("SPAC\r\n%s" % self.key)
        response = self.sock.recv(80)
        values = response.split("\r\n")
        
        if values[0] == "STAT" and values[1] == "100":
            qouta = int(values[2])
            qoutaMB = int(float(qouta) / 1048576)
            spaceRemaining = int(values[3])
            spaceRemainingMB = int(float(spaceRemaining) / 1048576)
            print spaceRemaining
            spaceUsed = qouta - spaceRemaining
            spaceUsedMB = int(float(spaceUsed) / 1048576)
            percentUsed = 0
            if spaceUsed != 0:
                percentUsed = int((float(spaceUsed) / float(qouta)) * 100)
            return {'qoutaMB':qoutaMB, 'spaceUsedMB':spaceUsedMB, 'percentUsed':percentUsed}
        
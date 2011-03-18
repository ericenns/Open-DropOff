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

import SocketServer
import ConfigParser
import re
import os

import os

#from database import *
#from database.DatabaseConnection import DatabaseConnection
#from database.UsersDB import UsersDB

RECEIVESIZE = 100

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
            command, arguments = self.data.split("\r\n", 1)
            if(command == "PUSH"):
                self.push(arguments)
            elif(command == "PULL"):
                self.pull(arguments)
            elif(command == "CLOS");
                break
        self.request.close()
            
    def push(self, arguments):
        # get the filename and filesize then tell the client to continue
        filename, filesize = arguments.split("\r\n", 1)
        filesize = int(filesize)
        print "filesize: ", filesize
        #echoing data for now, may be useful
        self.request.send(self.data)
        
        #authenticate user information
        self.data = self.request.recv(80)
        userN, password = self.data.split("\r\n", 1)
        
        #verify user
        
        #verity password
        
        #write the files to a test sub-directory prevents 
        #clogging up the server folder with random test files
        #newfile = open("./testfiles/" + filename, "wb")
        fullpath = "%s%s%s" % (BASEDIR,FILEDIR,filename)
        if(os.path.isfile(fullpath)):
            print "File already exists"
        newfile = open(fullpath, "wb")
        
        #receives 100 bytes of the file at a time, loops until
        #the whole file is received
        #content = self.request.recv(filesize)
        totalReceived = -1
        
        while totalReceived <= filesize:
            if( totalReceived == -1 ):
                totalReceived =  0
            #print "looping!"
            
            content = self.request.recv(RECEIVESIZE)
            totalReceived += RECEIVESIZE
            newfile.write(content)

        newfile.close() #close the file
        
        #send a response to the client
        self.request.send("Received %s" % filename)
        self.request.close()
        print "Finished!\n"


    def pull(self, filename):
        
        filesize = os.path.getsize(filename)
        print "filename: ", filesize
        self.request.send("%i" % filesize)

            
if __name__ == "__main__":
    #HOST, PORT = "localhost", 30000
    HOST = config.get("Network", "host")
    PORT = config.getint("Network", "port")
    BASEDIR = config.get("Storage", "basedir")
    FILEDIR = config.get("Storage", "files")

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
    

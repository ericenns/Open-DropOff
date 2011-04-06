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
from handlers import GeneralHandler

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
        genHandler = GeneralHandler.GeneralHandler(self.request
                                                   , self.client_address
                                                   , BASEDIR, FILEDIR, SEPARATER
                                                   , DBHOST, DB
                                                   , DBUSER, DBPASS)
        
        while(1):
            self.data = genHandler.recvRequest(130)
            print self.client_address
            try:
                command, arguments = self.data.split("\r\n", 1)
                print "\nCommand:\t%s" % command
                if(command == "NUSR"):
                    genHandler.createNewUser(arguments)
                elif(command == "PASS"):
                    genHandler.changePassword(arguments)
                elif(command == "USER"):
                    genHandler.login(arguments)
                elif(command == "LIST"):
                    genHandler.list(arguments)
                elif(command == "PUSH"):
                    genHandler.push(arguments)
                elif(command == "PULL"):
                    genHandler.pull(arguments)
                elif(command == "REMV"):
                    genHandler.remvFile(arguments)
                elif(command == "SPAC"):
                    genHandler.spaceRemaining(arguments)
                elif(command == "CLOS"):
                    print "Connection with Client closed"
                    break
            except ValueError:
                print "Connection with Client lost"
                break
            
        self.request.close()
             
             
if __name__ == "__main__":
    #HOST, PORT = "localhost", 30000
    HOST = config.get("Network", "host")
    PORT = config.getint("Network", "port")
    BASEDIR = config.get("Storage", "basedir")
    FILEDIR = config.get("Storage", "files")
    SEPARATER = config.get("Storage", "separater")
    DBHOST = config.get("Database", "host")
    DB = config.get("Database", "database")
    DBUSER = config.get("Database", "user")
    DBPASS = config.get("Database", "pass")
    
    currentDir = os.getcwd()
    sys.path.append("%s/" % currentDir)

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), ODOTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Running..."
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    

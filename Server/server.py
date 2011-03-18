#!/usr/bin/python
#COMMENT!!!!
#from socket import *

#myHost = 'localhost'             # me
#myPort = 30000           # arbitrary port
#myFile = "sentReadme"   # file to write to

#f = open(myFile,"wb")
#s = socket( AF_INET, SOCK_STREAM )
#s.bind((myHost,myPort))
#s.listen(5)

#while 1:
#    connection, address = s.accept()
#    print address
#    while 1:
#        data = connection.recv(1024)            # receive data from client
#        if data:
#            f.write(data)                       # write to file
#            connection.send('echo -> ' + data)  # echo for confirmation
#        else:
#            break
#    f.close()
#    connection.close()

import SocketServer
import ConfigParser
import re

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
        self.data = self.request.recv(80)
        command, arguments = self.data.split("\r\n", 1)
        if(command == "PUSH"):
            push(arguments)
            
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
        newfile = open(filename, "wb")
        
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
        
            
if __name__ == "__main__":
    #HOST, PORT = "localhost", 30000
    HOST = config.get("Network", "host")
    PORT = config.getint("Network", "port")

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
    server.serve_forever()
    

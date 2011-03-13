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
import re

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
            # get the filename and filesize then tell the client to continue
            filename, filesize = arguments.split("\r\n", 1)
            filesize = int(filesize)
            # I am not sure what we send back
            self.request.send("Onward")
            
            #receive the entire file at once
            #could be split into a loop only reading a certain number of bytes at a time
            content = self.request.recv(filesize)
            print content
            
            #send a response to the client
            self.request.send("Received %s" % filename)
            self.request.close()
            print "Finished!"
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 30000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), ODOTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Running..."
    server.timeout = 60
    server.serve_forever()
    

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
        self.data = self.request.recv(1024).strip()
        command = self.data[:4]
        if(command == "PUSH"):
            filename = self.data[5:]
            print "%s sending: %s" % (self.client_address[0], filename)
        
            while 1:
                self.data = self.request.recv(1024).strip()
                
                if self.data:
                    print self.data
                else:
                    break
            # just send back the same data, but upper-cased
            self.request.send("Received %s" % filename)

if __name__ == "__main__":
    HOST, PORT = "localhost", 30000

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), ODOTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    

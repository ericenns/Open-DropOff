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
        print self.data
        command, content = self.data.split("\r\n", 1)
        if(command == "PUSH"):
            filename, content = content.split("\r\n", 1)
            print content
            while 1:
                print "WHILE TIME"
                content = self.request.recv(1024).strip()
                
                if not content:
                    break
                else:
                    print content
            # just send back the same data, but upper-cased
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
    server.serve_forever()
    

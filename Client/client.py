import socket
import sys
import getopt
import os
from Controllers import *

RECEIVESIZE = 100
SENDSIZE = 100

def main():
    #Reading in options from the command line
    optlist, args = getopt.getopt(sys.argv[1:], 's:p:', ['server', 'port'] )
        
    if(not optlist):
        print """Options are:
            -s (--server): specify name of server to connect to
            -p (--port): specify port number to connect to
            """
        exit()
    else:
        #Parsing options specified in command line
        for opt, val in optlist:
            if opt == "-s" or opt == "--server":
                serverHost = val
                print "`%s`" % serverHost
            if opt == "-p" or opt == "--port":
                serverPort = int(val)
    
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )  # create a TCP socket
    rc = RequestController.RequestController()
    rc.createConect( serverHost, serverPort)
    
    while 1:
        filename = raw_input("Please enter name of file to transfer: ")
        filesize = os.path.getsize(filename)
        rc.sendFile(filename, filesize)
        #data = sock.recv(80)                 # receive up to 1K bytes
        #sock.close()
        #print data
   
#send file to server
def sendFile(sock,filename, filesize):
    f = open(filename,"rb")
    sock.send("PUSH\r\n%s\r\n%d" % (filename, filesize))
    # wait for a response then start sending the file
    reply = sock.recv(80)
    print reply
    
    sock.send("%s\r\n%s" % ("JohnDoe","homie4life"))
    
    line = f.read(SENDSIZE)
    while line:
        sent = sock.send(line)
        while sent != len(line):
            sent += sock.send(line[sent:])
        line = f.read(SENDSIZE)
    f.close()
    
if __name__ == "__main__":
    main()
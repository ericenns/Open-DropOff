import sys
import getopt
from socket import *

#Reading in options from the command line
optlist, args = getopt.getopt(sys.argv[1:], 's:p:o', ['server', 'port', 'options'] )

#send file to server
def sendFile():
    f = open(fileName,"rb")
    for line in f:
        s.send(line)
    f.close()
    print "hi"
    
#Parsing options specified in command line
for opt, val in optlist:
    if opt == "-o" or opt == "--options":
        print """Options are:
            -s (--server): specify name of server to connect to
            -p (--port): specify port number to connect to
            """
    elif opt == "-s" or opt == "--server":
        serverHost = val
    elif opt == "-p" or opt == "--port":
        serverPort = val
            
s = socket( AF_INET, SOCK_STREAM )  # create a TCP socket

try:
    s.connect(('localhost', '30000')) # connect to server on the port
    
    while 1:
        filename = input("Please enter name of file to transfer: ")
        sendFile()                          # send the data
        data = s.recv(1024)                 # receive up to 1K bytes
        print data
except:
    print "Unable to connect to server specified."
    
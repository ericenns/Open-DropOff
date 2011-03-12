import sys
import getopt
from socket import *

#Reading in options from the command line
optlist, args = getopt.getopt(sys.argv[1:], 's:p:o', ['server', 'port', 'options'] )

SENDSIZE = 100

#send file to server
def sendFile(sock,filename):
    f = open(fileName,"rb")
    sock.send("PUSH\r\n%s\r\n" % filename)
    sock.send("SOMEDATA")
    line = f.read(SENDSIZE)
    while line:
        sent = s.send(line)
        while sent != SENDSIZE:
            sent += s.send(line[sent:])
        line = f.read(SENDSIZE)
    f.close()
    
#Parsing options specified in command line
for opt, val in optlist:
    if opt == "-o" or opt == "--options":
        print """Options are:
            -s (--server): specify name of server to connect to
            -p (--port): specify port number to connect to
            """
    elif opt == "-s" or opt == "--server":
        serverHost = val
	print "`%s`" % serverHost
    elif opt == "-p" or opt == "--port":
        serverPort = int(val)
            
s = socket( AF_INET, SOCK_STREAM )  # create a TCP socket

try:
    s.connect((serverHost, serverPort)) # connect to server on the port
   # while 1:
    filename = raw_input("Please enter name of file to transfer: ")
    sendFile(s, filename)   
    #s.send("PUSH %s" % filename)                       # send the data
    data = s.recv(1024)                 # receive up to 1K bytes
    print data
except:
    print "Unable to connect to server specified. %s" % serverHost

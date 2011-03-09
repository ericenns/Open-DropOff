import sys
import getopt
from socket import *

optlist, args = getopt.getopt(sys.argv[1:], 's:p:o', ['server', 'port'] )

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
    s.connect((serverHost, serverPort)) # connect to server on the port
    s.send( 'Hey Travis!' )               # send the data
    data = s.recv(1024)                 # receive up to 1K bytes
    
    print data
except:
    print "Unable to connect to server specified."
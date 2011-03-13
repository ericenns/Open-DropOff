import socket
import sys
import getopt
import os

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

    try:
        sock.connect((serverHost, serverPort)) # connect to server on the port
       # while 1:
        filename = raw_input("Please enter name of file to transfer: ")
        filesize = os.path.getsize(filename)
        sendFile(sock, filename, filesize)
        data = sock.recv(1024)                 # receive up to 1K bytes
        sock.close()
        print data
    except:
        print "Unable to connect to server specified. %s" % serverHost
           
#send file to server
def sendFile(sock,filename, filesize):
    f = open(filename,"rb")
    sock.send("PUSH\r\n%s\r\n%d" % (filename, filesize))
    reply = sock.recv(80)
    print reply
    
    line = f.read(SENDSIZE)
    while line:
        sent = sock.send(line)
        while sent != len(line):
            sent += sock.send(line[sent:])
        line = f.read(SENDSIZE)
    print "bitch"
    f.close()
        
if __name__ == "__main__":
    main()


#HOST, PORT = "localhost", 9999
#data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server and send data
#sock.connect((HOST, PORT))
#sock.send(data + "\n")

# Receive data from the server and shut down
#received = sock.recv(1024)
#sock.close()

#print "Sent:     %s" % data
#print "Received: %s" % received

import socket
import sys
import getopt
import os

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

    try:
        sock.connect((serverHost, serverPort)) # connect to server on the port
        
        
        while 1:
            ppSelection = raw_input("Push or pull? Enter 1 for push, 2 for pull, q to close: ")
            
            if ppSelection == "1":
                filename = raw_input("Please enter name of file to transfer: ")
                filesize = os.path.getsize(filename)
                sendFile(sock, filename, filesize)
                data = sock.recv(80)                 # receive up to 1K bytes
                #sock.close()
                print data
            elif ppSelection == "2":
                filename = raw_input("Please enter name of file to retrieve: ")
                retrieveFile(sock,filename)
            elif ppSelection == "q":
                print "Closing!"
                sock.send("CLOS\r\n")
                sock.close()
                break
        
    except:
        print "Unable to connect to server specified. %s" % serverHost

#retrieve file from server
def retrieveFile(sock,filename):
    
    #fullpath = "%s%s%s" % (BASEDIR,FILEDIR,filename)
    sock.send("PULL\r\n%s" % filename)
    arguments = sock.recv(80)
    command, filesize = arguments.split("\r\n", 1)
    filesize = int(filesize)
    if command == "RECV":
        sock.send("SEND")
        newfile = open(filename, "wb")
        totalReceived = -1
        
        while totalReceived <= filesize:
            if( totalReceived == -1 ):
                totalReceived =  0
            
            content = sock.recv(RECEIVESIZE)
            totalReceived += RECEIVESIZE
            newfile.write(content)
        
        newfile.close() #close the file
    else:
        print "FAILURE!"
    
    
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

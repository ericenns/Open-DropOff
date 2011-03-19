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
        key = "";
        
        while 1:
            ppSelection = raw_input("Push or pull? Enter l for login, 1 for push, 2 for pull, q to close: ")
            
            if ppSelection == "l":
                key = login(sock)
                print key
            elif ppSelection == "1":
                filename = raw_input("Please enter name of file to transfer: ")
                filesize = os.path.getsize(filename)
                sendFile(sock, filename, filesize, key)
            elif ppSelection == "2":
                filename = raw_input("Please enter name of file to retrieve: ")
                retrieveFile(sock,filename, key)
            elif ppSelection == "q":
                print "Closing!"
                sock.send("CLOS\r\n")
                sock.close()
                break
        
    except:
        print "Unable to connect to server specified. %s" % serverHost

#retrieve file from server
def retrieveFile(sock,filename, key):
    sock.send("PULL\r\n%s\r\n%s" % (filename, key))
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
def sendFile(sock,filename, filesize, key):
    f = open(filename,"rb")
    sock.send("PUSH\r\n%s\r\n%i\r\n%s" % (filename, filesize, key))
    # wait for a response then start sending the file
    reply = sock.recv(80)
    if(reply == "OKAY"):
        print reply
    else:
        return
    
    #sock.send("%s\r\n%s" % ("JohnDoe","homie4life"))
    
    line = f.read(SENDSIZE)
    while line:
        sent = sock.send(line)
        while sent != len(line):
            sent += sock.send(line[sent:])
        line = f.read(SENDSIZE)
    f.close()
    
    data = sock.recv(80)
    print data

def login(sock):
    username = raw_input("Please enter your username: ")
    print username
    sock.send("USER\r\n%s" % username)
    response = sock.recv(80)
    if(response == "OKAY"):
        password = raw_input("Please enter your password: ")
        sock.send("PASS\r\n%s" % password)
        data = sock.recv(80)
        response, key = data.split("\r\n",1)
        if(response == "OKAY"):
            return key;
        else:
            return "";
    else:
        return "";
    
if __name__ == "__main__":
    main()

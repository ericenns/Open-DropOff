import socket
import sys
import getopt
import os
from Controllers import RequestController

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
    
    rc = RequestController.RequestController( serverHost, serverPort )
    print "RC server: %s" % rc.server
    print "RC port: %s" % rc.port
    
    while 1:
        ppSelection = raw_input("Push or pull? Enter:\n\tc for to create new user\n\tl for login\n\t1 for push\n\t2 for pull\n\tq to close: ")
        
        if ppSelection == "l":
            rc.login()
        elif ppSelection == "1":
            filename = raw_input("Please enter name of file to transfer: ")
            filesize = os.path.getsize(filename)
            rc.push(filename, filesize)
        elif ppSelection == "2":
            filename = raw_input("Please enter name of file to retrieve: ")
            rc.pull(filename)
        elif ppSelection == "q":
            print "Closing!"
            break
        elif ppSelection == "c":
            newuser = raw_input("Please enter your new user name: ")
            newpass = ""
            while newpass == "":
                firstPass = raw_input("Please enter your new password: ")
                secondPass = raw_input("Please confirm your password: ")
                if firstPass == secondPass:
                    newpass = firstPass
                    print newpass
                else:
                    print "Passwords do not match, please try again."
            
            done = rc.newUser(newuser, newpass)
            
            if done:
                print "Successfully created your new account!"
            else:
                print "Unable to create your account, try again!"

if __name__ == "__main__":
    main()

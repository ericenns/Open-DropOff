'''
Created on Mar 17, 2011

@author: Andrew
'''

import socket

RECEIVESIZE = 100
SENDSIZE = 100

class RequestController(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        
    def createConect(self, server, port):
        self.sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )  # create a TCP socket

        try:
            self.sock.connect((server, port)) # connect to server on the port
        except:
            print "Unable to connect to server specified. %s" % server
               
        
    #send file to server
    #params:    sock    connection to have file sent through
    #            filename    name of file to be sent
    #            filesize    size of file being sent
    def sendFile(self, filename, filesize):
        f = open(filename,"rb")
        self.sock.send("PUSH\r\n%s\r\n%d" % (filename, filesize))
        # wait for a response then start sending the file
        reply = self.sock.recv(80)
        print reply
        
        self.sock.send("%s\r\n%s" % ("JohnDoe","homie4life"))
        
        line = f.read(SENDSIZE)
        while line:
            sent = self.sock.send(line)
            while sent != len(line):
                sent += self.sock.send(line[sent:])
            line = f.read(SENDSIZE)
        f.close()
            
    #Send a user to be logged in to the connection
    #params:    sock    connection to send username to
    #            user    username to be sent over connection
    def user(self, username):
        self.sock.send("USER %s" % username)
        #Could encrypt this as well
        
    #Sends a password to the socket specified
    #params:    sock    connection to send password to
    #            password    password to be sent
    def pwd(self, password):
        self.sock.send("PASS %s" % password)
        #Should add encryption at this point
        
    #Sends a listing of contents request to connection
    #params:    sock    connection to send list request to
    #Returns: list of items returned by the server
    def list(self):
        self.sock.send("LIST")
        #should figure out what format contents list should have
        contentsList = self.sock.recv(RECEIVESIZE)
        
        return contentsList
        
    #Send a request for a file to be pulled from connection
    #params:    sock    connection to have file pulled from
    #            filename    name of file to be pulled and saved
    #Returns: File data
    def pull(self, filename):
        self.sock.send("PULL\r\n%s" % filename)
        newfile = open(filename, "wb")
        
        #Receive a message indicating size of file coming
        #filesize = self.sock.recv(whatever)
        
        #receives 100 bytes of the file at a time, loops until
        #the whole file is received
        #content = self.request.recv(filesize)
        totalReceived = -1
        
        '''while totalReceived <= filesize:
            if( totalReceived == -1 ):
                totalReceived =  0
                #print "looping!"
                
                content = self.sock.recv(RECEIVESIZE)
                totalReceived += RECEIVESIZE
                newfile.write(content)
        '''
        newfile.close()
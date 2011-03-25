'''
Created on Mar 24, 2011

@author: Andrew
'''
import os

try: 
   from hashlib import sha1
   sha_constructor = sha1
except ImportError:
   import sha
   sha_constructor = sha.new
   
class FileHandler(object):
    '''
    classdocs
    '''

    def __init__(self, conn, basedir, filedir):
        '''
        Constructor
        '''
        self.connHandler = conn
        self.BASEDIR = basedir
        self.FILEDIR = filedir
        
    def receive(self, arguments):
        filename, filesize, key = arguments.split("\r\n", 2)
        print "FILENAME: %s" % filename
        filesize = int(filesize)
        
        #verify key
        if(key == "45f106ef4d5161e7aa38cf6c666607f25748b6ca"):
            self.connHandler.send("STAT\r\n100")
        else:
            self.connHandler.send("FAIL")
            return
        
        #authenticate user information
        #self.data = self.request.recv(80)
        #userN, password = self.data.split("\r\n", 1)
        
        #verify user
        
        #verity password
        
        #write the files to a test sub-directory prevents 
        #clogging up the server folder with random test files
        #newfile = open("./testfiles/" + filename, "wb")
        
        filename_hash = sha_constructor(filename).hexdigest()
        fullpath = "%s%s%s" % (self.BASEDIR,self.FILEDIR,filename_hash)
        if(os.path.isfile(fullpath)):
            print "File already exists"
        newfile = open(fullpath, "wb")
        #receives 100 bytes of the file at a time, loops until
        #the whole file is received
        totalReceived = -1
        
        print filesize
        
        while totalReceived <= filesize:
            if( totalReceived == -1 ):
                totalReceived =  0
            print "looping"
            content = self.connHandler.recv()
            totalReceived += self.connHandler.recvSize
            newfile.write(content)

        newfile.close() #close the file
        
        #send a response to the client
        self.connHandler.send("STAT\r\n100")
        print "PUSH Request finished"


    def send(self, arguments):
        filename, key = arguments.split("\r\n", 1)
        if(key == "45f106ef4d5161e7aa38cf6c666607f25748b6ca"):
            filename_hash = sha_constructor(filename).hexdigest()
            fullpath = "%s%s%s" % (self.BASEDIR,self.FILEDIR,filename_hash)
        
            filesize = os.path.getsize(fullpath)
        
            self.request.send("STAT\r\n100\r\n%i" % filesize)
        else:
            self.request.send("FAIL\r\n101")
            return
            
        response = self.connHandler.recv()
        
        if response == "SEND":
            #start sending the file
            
            file = open(fullpath, "rb")
            
            line = file.read(self.connHandler.sendSize)
            
            while line:
                sent = self.request.send(line)
                while sent != len(line):
                    sent += self.request.send(line[sent:])
                line = file.read(self.connHandler.sendSize)
            
            file.close()
        else:
            print "Don't send."
        print "PULL Request finished"
             
             
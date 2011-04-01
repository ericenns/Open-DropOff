###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Eric Enns                                                                #
#    Travis Martindale                                                        #
#    Andrew Matsuaka                                                          #
#    Chris Janssens                                                           #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

import os
import datetime

import shutil
from database import FilesDB
#from databasestub import FilesDB

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

    def __init__(self, conn, basedir, filedir, dbconn):
        '''
        Constructor
        '''
        self.connHandler = conn
        self.BASEDIR = basedir
        self.FILEDIR = filedir
        self.fdb = FilesDB.FilesDB(dbconn)
        
    def verifyKey(self, key):
        #verify key
        if(key == "440f23c58848769685e481ff270b046659f40b7c"):
            return True
        else:
            self.connHandler.send("STAT\r\n200")
            return False
        
    def listFiles(self, username):
        files = self.fdb.getAllFiles(username)
        print files
        
        self.connHandler.send("STAT\r\n100")
        for file in files:
            self.writeFileInfoToSocket(file)
        self.connHandler.send("STAT\r\n100")
        
    def listFileVersions(self, username, filename):
        pass #DB function not done yet for this
    
    def createEntirePath(self, filename, username, baseDir, fileDir, version):
        fullPath = self.createFullPath(filename, username, baseDir, fileDir)
        fullFilePath = self.createFullFilePath(fullPath, filename)
        fullPathFile = self.createFullPathFile(fullFilePath, version)
        
        return fullPathFile
        

    def createFullPath(self, filename, username, baseDir, fileDir):
        filenameHash = sha_constructor(filename).hexdigest()
        userHash = sha_constructor(username).hexdigest()
        print "filename: %s" % filename
        print "filename hash: %s" % filenameHash
        fullPath = "%s%s/%s/%s" % (baseDir, fileDir, userHash, filenameHash)
        print "Building fullPathFile: %s" % fullPath
        
        return fullPath
        
    def createFullPathFile(self, fullPath, version):
        if(version == "0"):
            # should get newest version currently gets just the first version
            fileVersion = "%s" % 1
        else:
            fileVersion = "%s" % version
        fullPathFile = fullPath + fileVersion
        
        print "Created fullPathFile: %s" % fullPathFile
        return fullPathFile
    
    def createFullFilePath(self, fullPath, filename):
        filenameHash = sha_constructor(filename).hexdigest()
        
        fileName = "/" + filenameHash
        
        fullFilePath = fullPath + fileName
        
        print "Created fullFilePath: %s" % fullFilePath
        return fullFilePath
    
    def writeFileInfoToSocket(self, fileInfo):
        data = fileInfo['client_path'] + "\r" + fileInfo['checksum'] + "\r\n"
        self.connHandler.send("%s" % data)
    
    #Writes data found in the specified file to the socket
    def writeFileToSocket(self, fullPathFile):
        file = open(fullPathFile, "rb")
                
        line = file.read(self.connHandler.sendSize)
        
        while line:
            sent = self.connHandler.send(line)
            while sent != len(line):
                sent += self.connHandler.send(line[sent:])
            line = file.read(self.connHandler.sendSize)
        
        file.close()
    
    #Accepts data from the socket and writes out to a new file
    def writeFileFromSocket(self, fullPath, fileSize):
        newfile = open(fullPath, "wb")
        #receives 100 bytes of the file at a time, loops until
        #the whole file is received
        totalReceived = -1
        
        print fileSize
        
        while totalReceived <= fileSize:
            if( totalReceived == -1 ):
                totalReceived =  0
            print "looping"
            content = self.connHandler.recv()
            totalReceived += self.connHandler.recvSize
            newfile.write(content)

        newfile.close() #close the file
        
    def receive(self, filename, filesize, checksum, username):
        print "FILENAME: %s" % filename
        filesize = int(filesize)
        
        if username != None:
            self.connHandler.send("STAT\r\n100")
            print "Sent stat message"
            #write the files to a test sub-directory prevents 
            #clogging up the server folder with random test files
            #newfile = open("./testfiles/" + filename, "wb")
            
            fullPath = self.createFullPath(filename, username, self.BASEDIR, self.FILEDIR)
            fullFilePath = self.createFullFilePath(fullPath,filename)
            
            if not os.path.exists(fullPath):
                os.makedirs(fullPath)
                version = str(1)
                
                fullPathFile = self.createFullPathFile(fullFilePath, version)
                self.fdb.addFile(username, filename, fullPathFile, filesize, "user", datetime.datetime, version, checksum)
            else:
                version = self.fdb.updateFile(username,filename,fullFilePath)
                fullPathFile = self.createFullPathFile(fullFilePath, version)
            
            print "Writing from Socket"
            self.writeFileFromSocket(fullPathFile, filesize)
            
            #send a response to the client
            self.connHandler.send("STAT\r\n100")
            print "PUSH Request finished"
        else:
            self.connHandler.send("STAT\r\n200")

    #NOTE: Unable to implement version controlling properly at the moment.
    #Accepts filename from the socket and removes the file
    def remvFile(self, filename, username):
        print "In fileHandler! %s\n" % filename
        print "basedir: %s" % self.BASEDIR
        print "filedir: %s" % self.FILEDIR
        fullPath = self.createFullPath(filename, username, self.BASEDIR, self.FILEDIR)
        #os.remove(fullPath)
        self.fdb.removeFile(username, filename)
        shutil.rmtree(fullPath)


    #NOTE: Unable to implement version controlling properly at the moment.
    #        Ideally when sending a file, if the version is 0, then return the most recent version.
    #                                     else return the version specified
    #        At the moment there's no way of accessing an older version of the file since there's no
    #        update function in the database.
    
    def send(self, arguments):
        username = "user"
        filename, version, key = arguments.split("\r\n", 2)
        
        fullPath = self.createEntirePath(filename, username, self.BASEDIR, self.FILEDIR, version)
        
        if self.verifyKey(key):
            fileInfo = self.fdb.getFile(username, fullPath)
            fullPath = fileInfo['server_path']
            
            if(os.path.exists(fullPath)):
                fileSize = os.path.getsize(fullPath)
                self.connHandler.send("STAT\r\n100\r\n%i" % fileSize)
            else:
                self.connHandler.send("STAT\r\n302")
                return

            response = self.connHandler.recv()
            
            if response == "SEND":
                #start sending the file
                self.writeFileToSocket(fullPath)
            else:
                print "Don't send."
            print "PULL Request finished"
             
             

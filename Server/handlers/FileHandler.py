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

    def __init__(self, conn, basedir, filedir, separater, dbconn):
        '''
        Constructor
        '''
        self.connHandler = conn
        self.BASEDIR = basedir
        self.FILEDIR = filedir
        self.SEPARATER = separater
        self.fdb = FilesDB.FilesDB(dbconn)
        
    def listFiles(self, username):
        
        if username != None:
            files = self.fdb.getAllFiles(username)
            print "Files from Database:"
            print files
            
            print "Sending start of LIST response code..."
            self.connHandler.send("STAT\r\n100")
            #self.connHandler.send("README\t8934a7a9292d0a57c9f4a257eaa626cf117ce7e9")
            for file in files:
                print "Sending files: %s" % file
                self.writeFileInfoToSocket(file)
            print "Sending end of LIST response code..."
            self.connHandler.send("STAT\r\n100")
        else:
            self.connHandler.send("STAT\r\n200")
    

    def listFileVersions(self, username, filename):
        if username != None:
            fileInfo = self.fdb.getFile(username, filename)
            fileId = fileInfo['file_id']
            versions = self.fdb.getFileHistory(fileId)
            
            print "Versions from Database:"
            print versions
            
            print "Sending start of LIST response code..."
            self.connHandler.send("STAT\r\n100")
 
            for version in versions:
                print "Sending versions: %s" % version
                self.writeVersionInfoToSocket(version)
            print "Sending end of LIST response code..."
            self.connHandler.send("STAT\r\n100")
            
        else:
            self.connHandler.send("STAT\r\n200")

    
    def writeFileInfoToSocket(self, fileInfo):
        data = "%s\t%s\t%s\t%s\r\n" % (fileInfo['client_path'], fileInfo['checksum'], fileInfo['last_modified'], fileInfo['size'])
        #data = fileInfo['client_path'] + "\t" + fileInfo['checksum'] +"\r\n"
        print "Writing out..."
        print data
        self.connHandler.send("%s" % data)
        
        
    def writeVersionInfoToSocket(self, fileInfo):
        data = fileInfo['client_path'] + "\t" + str(fileInfo['version']) + "\r\n"
        print "Writing out..."
        print data
        self.connHandler.send("%s" % data)
    
        
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
        fullPath = "%s%s%s%s%s%s" % (baseDir, fileDir, self.SEPARATER, userHash, self.SEPARATER, filenameHash)
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
        
        fileName = "%s%s" % (self.SEPARATER, filenameHash)
        
        fullFilePath = fullPath + fileName
        
        print "Created fullFilePath: %s" % fullFilePath
        return fullFilePath
    
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
            
            fullPath = self.createFullPath(filename, username, self.BASEDIR, self.FILEDIR)
            fullFilePath = self.createFullFilePath(fullPath,filename)
            
            fileEntry = self.fdb.getFile(username , filename)
            
            if fileEntry == None:
                os.makedirs(fullPath)
                version = str(1)
                
                fullPathFile = self.createFullPathFile(fullFilePath, version)
                self.fdb.addFile(username, filename, fullPathFile, filesize, "user", datetime.datetime.now(), version, checksum)
                goodToWrite = True
            elif fileEntry['checksum'] == checksum:
                self.connHandler.send("STAT\r\n305")
                print "File sent was up-to-date."
                goodToWrite = False
            else:
                version = fileEntry['version'] + 1
                fullPathFile = self.createFullPathFile(fullFilePath, version)
                fileEntry['server_path'] = fullPathFile
                fileEntry['checksum'] = checksum
                fileEntry['last_modified'] = datetime.datetime.now()
                fileEntry['version'] = version
                newVersion = self.fdb.updateFile(username,filename,fileEntry)
                if version != newVersion:
                    print "Something went wrong"
                goodToWrite = True
                
            if(goodToWrite):
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
    def send(self, filename, version, username):
        #print "File Handler, Send\n"
        #print "FILENAME: %s VERSION: %s USERNAME: %s" % (filename, version, username)
        
        if username != None:

            fileInfo = self.fdb.getFile(username, filename)
            if fileInfo:
                if fileInfo['version'] == version or version == "0":
                    fullPath = fileInfo['server_path']
                else:
                    fileId = fileInfo['file_id']
                    fileInfo = self.fdb.getFileVersion(fileId, version)
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
            else:
                self.connHandler.send("STAT\r\n302")
        else:
            self.connHandler.send("STAT\r\n200")
             

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
from databasestub import FilesDB

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
        
    def receive(self, arguments):
        filename, filesize, checksum, key = arguments.split("\r\n", 3)
        print "FILENAME: %s" % filename
        filesize = int(filesize)
        
        #verify key
        if(key == "440f23c58848769685e481ff270b046659f40b7c"):
            self.connHandler.send("STAT\r\n100")
        else:
            self.connHandler.send("STAT\r\n200")
            return
        
        version = str(1)
        
        #write the files to a test sub-directory prevents 
        #clogging up the server folder with random test files
        #newfile = open("./testfiles/" + filename, "wb")
        
        filename_hash = sha_constructor(filename).hexdigest()
        user_hash = sha_constructor("user").hexdigest()
        fullpath = "%s%s/%s/%s" % (self.BASEDIR,self.FILEDIR,user_hash,filename_hash)
        fileversion = "/"+filename_hash+version
        fullpathfile = fullpath + fileversion
        
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)
        
        if(os.path.isfile(fullpath)):
            print "File already exists"
            
        self.fdb.addFile("user", filename, fullpath, filesize, "user", datetime.datetime, fileversion, checksum)
        
        newfile = open(fullpathfile, "wb")
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
        filename, version, key = arguments.split("\r\n", 2)
        if(key == "440f23c58848769685e481ff270b046659f40b7c"):
            filename_hash = sha_constructor(filename).hexdigest()
            user_hash = sha_constructor("user").hexdigest()
            fileInfo = self.fdb.getFile("user", filename)
            
            '''fullpath = "%s%s%s/%s" % (self.BASEDIR,self.FILEDIR,user_hash,filename_hash)
            fileversion = "/%s" % filename_hash
            if(version == "0"):
                # should get newest version currently gets just the first version
                fileversion = "%s%s" % (fileversion, 1)
            else:
                fileversion = "%s%s" % (fileversion, version)
            fullpathfile = "%s%s" % (fullpath, fileversion)'''
            fullpath = fileInfo['server_path']
            fileversion = 
            
            if(os.path.exists(fullpathfile)):
                filesize = os.path.getsize(fullpathfile)
                self.connHandler.send("STAT\r\n100\r\n%i" % filesize)
            else:
                self.connHandler.send("STAT\r\n302")
                return
        else:
            self.connHandler.send("STAT\r\n200")
            return
            
        response = self.connHandler.recv()
        
        if response == "SEND":
            #start sending the file
            
            file = open(fullpathfile, "rb")
            
            line = file.read(self.connHandler.sendSize)
            
            while line:
                sent = self.connHandler.send(line)
                while sent != len(line):
                    sent += self.connHandler.send(line[sent:])
                line = file.read(self.connHandler.sendSize)
            
            file.close()
        else:
            print "Don't send."
        print "PULL Request finished"
             
             

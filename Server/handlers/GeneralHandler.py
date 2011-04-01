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

import AccountHandler
import FileHandler
import ConnectionHandler

from database import *
#from databasestub import *


class GeneralHandler(object):
    '''
    classdocs
    '''

    def __init__(self, tcpConn, clientAddr, basedir, filedir, separater, dbhost, db, dbuser, dbpass):
        '''
        Constructor
        '''
        self.dbConnection = DatabaseConnection.DatabaseConnection()
        self.dbConnection.connect(dbhost, dbuser, dbpass, db)
        self.sdb = SessionsDB.SessionsDB(self.dbConnection)
        self.connHandler = ConnectionHandler.ConnectionHandler(tcpConn, clientAddr, 100, 100)
        self.accHandler = AccountHandler.AccountHandler(self.connHandler, self.dbConnection, self.sdb)
        self.fileHandler = FileHandler.FileHandler(self.connHandler, basedir, filedir, separater, self.dbConnection)

    def verifyKey(self, key):
        return self.sdb.getUserFromSession(key)

    def push(self, args):
        filename, filesize, checksum, key = args.split("\r\n", 3)
        username = self.verifyKey(key)
        self.fileHandler.receive(filename, filesize, checksum, username)
    
    def pull(self, args):
        self.fileHandler.send(args)
    
    def list(self, args):
        key = args
        username = self.verifyKey(key)
        print username
        self.fileHandler.listFiles(username)
        
    def createNewUser(self, args):
        self.accHandler.createNewUser(args)
        
    def changePassword(self, args):
        newpass, oldpass, key = args.split("\r\n", 3)
        username = self.verifyKey(key)
        self.accHandler.changePassword(newpass, oldpass, username)
    
    def login(self, args):
        self.accHandler.login(args)
        
    def recvRequest(self, size=100):
        return self.connHandler.recv(size)
    
    def remvFile(self, args):
        filename, key = args.split("\r\n",2)
        username = self.verifyKey(key)
        self.fileHandler.remvFile(filename, username)

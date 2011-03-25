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

class GeneralHandler(object):
    '''
    classdocs
    '''

    def __init__(self, tcpConn, basedir, filedir):
        '''
        Constructor
        '''
        self.connHandler = ConnectionHandler.ConnectionHandler(tcpConn, 100, 100)
        self.accHandler = AccountHandler.AccountHandler(self.connHandler)
        self.fileHandler = FileHandler.FileHandler(self.connHandler, basedir, filedir)
        
    def push(self, args):
        self.fileHandler.receive(args)
    
    def pull(self, args):
        self.fileHandler.send(args)
    
    def list(self):
        self.fileHandler.list()
        
    def createNewUser(self, args):
        self.accHandler.createNewUser(args)
        
    def changePassword(self, args):
        self.accHandler.changePassword(args)
    
    def login(self, args):
        self.accHandler.login(args)
        
    def recvRequest(self):
        return self.connHandler.recv()
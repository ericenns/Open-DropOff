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

import SocketServer

class ConnectionHandler(object):
    '''
    classdocs
    '''

    def __init__(self, conn, clientAddr, ssize, rsize):
        '''
        Constructor
        '''
        self.connection = conn
        self.recvSize = ssize
        self.sendSize = rsize
        self.clientAddr = clientAddr
        
    def send(self, data):
        '''SEND STUFF HERE'''
        print "Sending data..."
        return self.connection.send( data )
        
    def recv(self):
        '''RETURN STUFF HERE'''
        print "Receiving data..."
        data = self.connection.recv(self.recvSize)
        return data
    
    def clientAddr(self):
        return self.clientAddr
'''
Created on Mar 24, 2011

@author: Andrew
'''

import SocketServer

class ConnectionHandler(object):
    '''
    classdocs
    '''

    def __init__(self, conn, ssize, rsize):
        '''
        Constructor
        '''
        self.connection = conn
        self.recvSize = ssize
        self.sendSize = rsize
        
    def send(self, data):
        '''SEND STUFF HERE'''
        print "Sending data..."
        self.connection.send( data )
        
    def recv(self):
        '''RETURN STUFF HERE'''
        print "Receiving data..."
        data = self.connection.recv(self.recvSize)
        return data
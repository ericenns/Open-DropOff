'''
Created on Mar 24, 2011

@author: Andrew
'''

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
        self.accHandle = AccountHandler.AccountHandler(self.connHandler)
        self.fileHandle = FileHandler.FileHandler(self.connHandler, basedir, filedir)
        
    def push(self, args):
        self.fileHandle.receive(args)
    
    def pull(self, args):
        self.fileHandle.send(args)
    
    def list(self):
        self.fileHandle.list()
        
    def createNewUser(self, args):
        self.accHandle.createNewUser(args)
    
    def login(self, args):
        self.accHandle.login(args)
        
    def recvRequest(self):
        return self.connHandler.recv()
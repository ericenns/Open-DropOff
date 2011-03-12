'''
Created on 2011-03-11

@author: Michael Yagudaev
'''

import DatabaseConnection

class FileDB:
    '''
    All transactions associated primarly with a file. A connection with the database must be established before 
    using this class. Conn is a valid DatabaseConnection object.
    Note: the files on the server and the database will be to be kept in sync by the business
    logic layer.
    '''
    def getFilesInDir(self, conn, path):
        '''
        Gets the files in a specific directory
        '''
        '''
        TODO: write code
        '''
    
    def getFileSize(self, conn, path):
        '''
        Gets the file size
        '''
        '''
        TODO: write code
        '''
        
    def getLastAuthor(self, conn, path):
        '''
        Gets the last author of the file, i.e. who it was last modified by
        '''
        '''
        TODO: write code
        '''
    
    def updateLastAuthor(self, conn, path, newAuthor):
        '''
        Updates the last author of the file in the database
        '''
    
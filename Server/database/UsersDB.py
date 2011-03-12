'''
Created on 2011-03-11

@author: Michael Yagudaev
'''
import DatabaseConnection

class UsersDB:
    '''
    All operations and data associated with a user in the database.
    '''
    def getFiles(self, conn, username):
        '''
        Gets all the files a user has in their dropoff box
        '''
        '''
        TODO: write code...
        '''
        
    def authenticate(self, conn, username, password):
        '''
        Returns true of false depending if the user passed authentication after
        information was retrived from the DB.
        '''
        '''
        TODO: write code...
        '''
        
    def addUser(self, conn, username, password, quota):
        '''
        Adds a user to the database
        '''
        '''
        TODO: write code...
        '''
        
    def removeUser(self, conn, username):
        '''
        Remove a user from the database.
        '''
        '''
        TODO: write code...
        '''
        
    def addFile(self, conn, username, fileID):
        '''
        Add a file to a specific users drop off account
        '''
        
    def getFile(self, conn, username, path):
        '''
        Gets a file based on a the file path given. The system will also make sure 
        the user has permissions to access this file. An exception will be thrown if
        the user is unautorized to access the file. 
        '''
        '''
        TODO: write code...
        '''
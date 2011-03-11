'''
This objects provides access to the database and abstracts the actual database used
from the user of this API. Each and every database request will need a valid reference
to the DatabaseConnection object.

The connection method should be invoked when the client is ready to communicate with the
database.
Created on 2011-03-08

@author: Michael Yagudaev
'''

import MySQLdb

class DatabaseConnection(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def connect(self, username, password, database):
        '''
        Connects to the database using the given creditials. To disconnect call disconnect
        '''
        self.conn = MySQLdb.connect("localhost", user = username, passwd = password, db = database)
        print("connected!!! Yay")
        
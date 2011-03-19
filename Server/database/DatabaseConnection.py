###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Michael Yagudaev                                                         #
#    Robert Tetlock                                                           #
#    Marilyn Hacko                                                            #
#    Eu Wern                                                                  #
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

import MySQLdb

class DatabaseConnection(object):
    '''
    This object provides access to the database and abstracts the actual database used
    from the user of this API. Each and every database request will need a valid reference
    to the DatabaseConnection object.
    
    The connection method should be invoked when the client is ready to communicate with the
    database.
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        self._conn = None       #_conn connection
        self._cursor = None     #_cursor (you need this to _execute sql comment
        self._data = None       #_data   (this will return tupples from the database
        
    def connect(self, host, username, password, database):
        '''
        Connects to the database using the given creditials. To disconnect call disconnect
        ''' 
        self._conn = MySQLdb.connect(host, username, password, database)
        self._cursor = self._conn.cursor()
        
    def disconnect(self):
        '''
        Closes the database connection. This should be called when client exits.
        '''
        self._conn.close();
        
    def _execute(self, sql, *args):
        '''
        Executes provided sql code after binding parameters, if any.
        '''
        self._cursor.execute(sql, args)
        self._conn.commit()
    
    def _getLastRowID(self):
        return self._cursor.lastrowid
        
    def _fetchOne(self):
        '''
        Return one row from the database resulting from the most recent query
        '''
        data = self._cursor.fetchone()
        return data
    
    def _fetchAll(self):
        '''
        Return all rows found in database resulting from the most recent query
        '''
        data = self._cursor.fetchall()
        return data
        
    def _getCount(self):
        data = self._cursor.rowcount
        return data
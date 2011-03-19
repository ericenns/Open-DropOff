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
    
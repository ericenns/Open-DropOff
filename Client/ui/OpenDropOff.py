###############################################################################
# Open DropOff                                                                #
# Copyright (C) 2011                                                          #
#                                                                             #
# Authors:                                                                    #
#    Cory Metcalfe                                                            #
#    Dave Fardoe                                                              #
#    Eric Osiowy                                                              #
#    Karl Wiens                                                               #
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

#imports
import sys
sys.path.append("../controllers") 
from PySide import QtCore, QtGui
from HomeScreen import HomeWindow
from LoginForm import LoginDialog
import RequestController

#Gobal constants
RECEIVESIZE = 100
SENDSIZE = 100
SERVER = "localhost"
PORT = 30000

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    # Set up the request controller and connect to the host
    rc = RequestController.RequestController( SERVER, PORT )
    
    rc.connect()
    
    # Handle login
    loginDialog = LoginDialog( rc )
    
    result = loginDialog.exec_()
    
    # Handle the results of the login attempt
    if( result == 0 ):
        mainWin = HomeWindow( rc )
        mainWin.show()
    elif( result == 1):
        rc.disconnect()
        app.quit()
    else:
        loginDialog.show()
    
    sys.exit(app.exec_())

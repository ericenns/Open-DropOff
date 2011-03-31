'''
Created on 2011-03-31

@author: Dave Fardoe
'''
import sys
from PySide import QtCore, QtGui
from HomeScreen import HomeWindow
from LoginForm import LoginDialog

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    loginDialog = LoginDialog()
    mainWin = HomeWindow()
    
    mainWin.hide()
    
    result = loginDialog.exec_()
    
    # Handle the results of the login attempt
    if( result == 0 ):
        mainWin.show()
    elif( result == 1):
        app.quit()
    else:
        loginDialog.show()
    
    sys.exit(app.exec_())
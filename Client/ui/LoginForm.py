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

#Imports
import RequestController
from ConfirmationDialog import ConfirmationDialog
from PySide import QtCore, QtGui

#Constants
LOGIN_FAILED_MESSAGE = "Login Failed.  Please try again."


class LoginDialog(QtGui.QDialog):
    def __init__(self, requestController, parent=None):
        
        #Initialize the HomeWindow object
        QtGui.QDialog.__init__(self, parent)
        
        #Assign the homeWindow object
        self.ui = Ui_LoginDialog()
        
        #Setup the window
        self.ui.setupUi(self)
        
        #Setup the RequestController
        self.rc = requestController
        
    #Handle events
    def accept(self):
        username = self.ui.UserNameTextBox.text()
        password = self.ui.PasswordTextBox.text()
        
        result = self.rc.login(username, password)
        
        if( result == None ):
            self.done(0)
        else:
            messageBox = QtGui.QMessageBox()
            messageBox.setText(LOGIN_FAILED_MESSAGE + "\n" + result)
            messageBox.exec_()
        
    def reject(self):
        self.done(1)

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(386, 185)
        LoginDialog.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(LoginDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.UserNameTextBox = QtGui.QLineEdit(LoginDialog)
        self.UserNameTextBox.setGeometry(QtCore.QRect(100, 30, 211, 22))
        self.UserNameTextBox.setObjectName("UserNameTextBox")
        self.PasswordTextBox = QtGui.QLineEdit(LoginDialog)
        self.PasswordTextBox.setGeometry(QtCore.QRect(100, 70, 211, 22))
        self.PasswordTextBox.setEchoMode(QtGui.QLineEdit.Password)
        self.PasswordTextBox.setObjectName("PasswordTextBox")
        self.label = QtGui.QLabel(LoginDialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(LoginDialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.label_2.setObjectName("label_2")

        self.retranslateUi(LoginDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), LoginDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), LoginDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(QtGui.QApplication.translate("LoginDialog", "Login Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LoginDialog", "User Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("LoginDialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))


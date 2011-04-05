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
from PySide import QtCore, QtGui

#Constants
USER_CREATE_FAILED_MESSAGE = "New user creation failed.  Please try again."
DIFFERENT_PASSWORDS_MESSAGE = "Passwords do not match.  Please try again."
USER_EXISTS_MESSAGE = "User Name already exists. Please try again."
NEW_USER_CREATED_MESSAGE = "New user created."

class CreateUserDialog(QtGui.QDialog):
    def __init__(self, requestController, parent=None):
        #Initialize the HomeWindow object
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_NewUserDialog()
        self.ui.setupUi(self)
        self.rc = requestController
            
    #Handle events
    def accept(self):
        username = self.ui.userText.text()
        pw1 = self.ui.pwText1.text()
        pw2 = self.ui.pwText2.text()
        
        if (pw1 != pw2):
            messageBox = QtGui.QMessageBox()
            messageBox.setText(DIFFERENT_PASSWORDS_MESSAGE)
            messageBox.exec_()
        elif (self.rc.newUser(username, pw1)):
            messageBox = QtGui.QMessageBox()
            messageBox.setText(NEW_USER_CREATED_MESSAGE)
            messageBox.exec_()
            self.done(1)
        else:
            messageBox = QtGui.QMessageBox()
            messageBox.setText(USER_CREATE_FAILED_MESSAGE)
            messageBox.exec_()
 
    def reject(self):
        self.done(1)

class Ui_NewUserDialog(object):
    def setupUi(self, NewUserDialog):
        NewUserDialog.setObjectName("NewUserDialog")
        NewUserDialog.resize(386, 171)
        NewUserDialog.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(NewUserDialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.userText = QtGui.QLineEdit(NewUserDialog)
        self.userText.setGeometry(QtCore.QRect(140, 20, 211, 21))
        self.userText.setObjectName("userText")
        self.pwText1 = QtGui.QLineEdit(NewUserDialog)
        self.pwText1.setGeometry(QtCore.QRect(140, 60, 211, 22))
        self.pwText1.setEchoMode(QtGui.QLineEdit.Password)
        self.pwText1.setObjectName("pwText1")
        self.userLabel = QtGui.QLabel(NewUserDialog)
        self.userLabel.setGeometry(QtCore.QRect(20, 20, 111, 21))
        self.userLabel.setObjectName("userLabel")
        self.pwLabel1 = QtGui.QLabel(NewUserDialog)
        self.pwLabel1.setGeometry(QtCore.QRect(20, 70, 71, 16))
        self.pwLabel1.setObjectName("pwLabel1")
        self.pwText2 = QtGui.QLineEdit(NewUserDialog)
        self.pwText2.setGeometry(QtCore.QRect(140, 90, 211, 22))
        self.pwText2.setEchoMode(QtGui.QLineEdit.Password)
        self.pwText2.setObjectName("pwText2")
        self.pwLabel2 = QtGui.QLabel(NewUserDialog)
        self.pwLabel2.setGeometry(QtCore.QRect(20, 90, 101, 21))
        self.pwLabel2.setObjectName("pwLabel2")

        self.retranslateUi(NewUserDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewUserDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewUserDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewUserDialog)
        NewUserDialog.setTabOrder(self.userText, self.pwText1)
        NewUserDialog.setTabOrder(self.pwText1, self.pwText2)
        NewUserDialog.setTabOrder(self.pwText2, self.buttonBox)

    def retranslateUi(self, NewUserDialog):
        NewUserDialog.setWindowTitle(QtGui.QApplication.translate("NewUserDialog", "Create New User", None, QtGui.QApplication.UnicodeUTF8))
        self.userLabel.setText(QtGui.QApplication.translate("NewUserDialog", "User Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.pwLabel1.setText(QtGui.QApplication.translate("NewUserDialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.pwLabel2.setText(QtGui.QApplication.translate("NewUserDialog", "Retype Password:", None, QtGui.QApplication.UnicodeUTF8))


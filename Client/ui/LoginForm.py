# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoginForm.ui'
#
# Created: Sun Mar 27 16:58:28 2011
#      by: pyside-uic 0.2.7 running on PySide 1.0.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

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


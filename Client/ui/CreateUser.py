# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateUser.ui'
#
# Created: Sun Apr  3 18:41:16 2011
#      by: PyQt4 UI code generator 4.7.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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


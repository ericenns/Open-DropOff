# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConfirmationDialog.ui'
#
# Created: Sat Apr  2 13:33:40 2011
#      by: pyside-uic 0.2.7 running on PySide 1.0.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class ConfirmationDialog(QtGui.QDialog):
    def __init__(self, message, parent=None):
        
        #Initialize the HomeWindow object
        QtGui.QDialog.__init__(self, parent)
        
        #Assign the homeWindow object
        self.ui = Ui_Dialog()
        
        #Setup the window
        self.ui.setupUi(self)
        self.ui.lbl_message.setText(message)
        
    #Handle events
    def accept(self):
        self.done(0)
        
    def reject(self):
        self.done(1)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(348, 125)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_message = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_message.sizePolicy().hasHeightForWidth())
        self.lbl_message.setSizePolicy(sizePolicy)
        self.lbl_message.setMaximumSize(QtCore.QSize(600, 400))
        self.lbl_message.setScaledContents(False)
        self.lbl_message.setWordWrap(True)
        self.lbl_message.setObjectName("lbl_message")
        self.verticalLayout.addWidget(self.lbl_message)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Are you sure?", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_message.setText(QtGui.QApplication.translate("Dialog", "This is some larger text to test how the label handles very large input, in case we decide to use a very large error message.  And now I\'m trying an even larger message to see what happens.  I sure hope this is enough text to get a good idea.", None, QtGui.QApplication.UnicodeUTF8))


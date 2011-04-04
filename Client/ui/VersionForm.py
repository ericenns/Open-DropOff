# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VersionForm.ui'
#
# Created: Sun Apr 03 22:15:23 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
    
class VersionForm(QtGui.QDialog):
    def __init__(self, requestController, parent=None):          
        #Initialize the HomeWindow object
        QtGui.QMainWindow.__init__(self, parent)
        
        #Setup the request controller
        self.rc = requestController
        
        #Assign the homeWindow object
        self.ui = Ui_VersioForm()
        
        #Setup the window
        self.ui.setupUi(self)

   # Handle the buttons
    def accept( self ):
        self.hide()
        
    def reject( self ):
        self.hide()

class Ui_VersioForm(object):
    def setupUi(self, VersioForm):
        VersioForm.setObjectName(_fromUtf8("VersioForm"))
        VersioForm.setWindowModality(QtCore.Qt.ApplicationModal)
        VersioForm.resize(420, 300)
        VersioForm.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(VersioForm)
        self.buttonBox.setGeometry(QtCore.QRect(70, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.treeView = QtGui.QTreeView(VersioForm)
        self.treeView.setGeometry(QtCore.QRect(20, 20, 281, 211))
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.downloadButton = QtGui.QPushButton(VersioForm)
        self.downloadButton.setGeometry(QtCore.QRect(320, 20, 93, 28))
        self.downloadButton.setObjectName(_fromUtf8("downloadButton"))

        self.retranslateUi(VersioForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), VersioForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), VersioForm.reject)
        QtCore.QMetaObject.connectSlotsByName(VersioForm)

    def retranslateUi(self, VersioForm):
        VersioForm.setWindowTitle(QtGui.QApplication.translate("VersioForm", "Versions", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("VersioForm", "Download", None, QtGui.QApplication.UnicodeUTF8))


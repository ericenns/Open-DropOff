# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewPWScreen_4.0.2.ui'
#
# Created: Sun Mar 27 01:36:22 2011
#      by: pyside-uic 0.2.7 running on PySide 1.0.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class NewPWDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        
        #Initialize the HomeWindow object
        QtGui.QDialog.__init__(self, parent)
        
        #Assign the homeWindow object
        self.ui = Ui_NewPWDialog()
        
        #Setup the window
        self.ui.setupUi(self)
        
    # Handle the buttons
    def accept( self ):
        self.hide()
        
    def reject( self ):
        self.hide()

class Ui_NewPWDialog(object):
    def setupUi(self, NewPWDialog):
        NewPWDialog.setObjectName("NewPWDialog")
        NewPWDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        NewPWDialog.resize(434, 159)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(NewPWDialog.sizePolicy().hasHeightForWidth())
        NewPWDialog.setSizePolicy(sizePolicy)
        NewPWDialog.setModal(True)
        self.verticalLayoutWidget = QtGui.QWidget(NewPWDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 40, 420, 116))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.passwordFieldLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.passwordFieldLayout.setSpacing(0)
        self.passwordFieldLayout.setMargin(0)
        self.passwordFieldLayout.setObjectName("passwordFieldLayout")
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.currPWLabel = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.currPWLabel.sizePolicy().hasHeightForWidth())
        self.currPWLabel.setSizePolicy(sizePolicy)
        self.currPWLabel.setMinimumSize(QtCore.QSize(150, 0))
        self.currPWLabel.setObjectName("currPWLabel")
        self.horizontalLayout_6.addWidget(self.currPWLabel)
        self.currPWlineEdit = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.currPWlineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.currPWlineEdit.setObjectName("currPWlineEdit")
        self.horizontalLayout_6.addWidget(self.currPWlineEdit)
        self.passwordFieldLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.newPWLabel1 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newPWLabel1.sizePolicy().hasHeightForWidth())
        self.newPWLabel1.setSizePolicy(sizePolicy)
        self.newPWLabel1.setMinimumSize(QtCore.QSize(150, 0))
        self.newPWLabel1.setObjectName("newPWLabel1")
        self.horizontalLayout_7.addWidget(self.newPWLabel1)
        self.newPWlineEdit1 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.newPWlineEdit1.setEchoMode(QtGui.QLineEdit.Password)
        self.newPWlineEdit1.setObjectName("newPWlineEdit1")
        self.horizontalLayout_7.addWidget(self.newPWlineEdit1)
        self.passwordFieldLayout.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.newPWLabel2 = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.newPWLabel2.sizePolicy().hasHeightForWidth())
        self.newPWLabel2.setSizePolicy(sizePolicy)
        self.newPWLabel2.setMinimumSize(QtCore.QSize(150, 0))
        self.newPWLabel2.setObjectName("newPWLabel2")
        self.horizontalLayout_8.addWidget(self.newPWLabel2)
        self.newPWlineEdit2 = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.newPWlineEdit2.setEchoMode(QtGui.QLineEdit.Password)
        self.newPWlineEdit2.setObjectName("newPWlineEdit2")
        self.horizontalLayout_8.addWidget(self.newPWlineEdit2)
        self.passwordFieldLayout.addLayout(self.horizontalLayout_8)
        self.buttonBox = QtGui.QDialogButtonBox(self.verticalLayoutWidget)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.passwordFieldLayout.addWidget(self.buttonBox)
        self.errorLabel = QtGui.QLabel(NewPWDialog)
        self.errorLabel.setEnabled(False)
        self.errorLabel.setGeometry(QtCore.QRect(50, 0, 331, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.errorLabel.sizePolicy().hasHeightForWidth())
        self.errorLabel.setSizePolicy(sizePolicy)
        self.errorLabel.setText("")
        self.errorLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setObjectName("errorLabel")

        self.retranslateUi(NewPWDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), NewPWDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), NewPWDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewPWDialog)

    def retranslateUi(self, NewPWDialog):
        NewPWDialog.setWindowTitle(QtGui.QApplication.translate("NewPWDialog", "Open DropOff - Change Password", None, QtGui.QApplication.UnicodeUTF8))
        self.currPWLabel.setText(QtGui.QApplication.translate("NewPWDialog", "Current Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.newPWLabel1.setText(QtGui.QApplication.translate("NewPWDialog", "New Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.newPWLabel2.setText(QtGui.QApplication.translate("NewPWDialog", "Retype New Password:", None, QtGui.QApplication.UnicodeUTF8))


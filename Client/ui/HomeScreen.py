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
import sys
import os
from PySide import QtCore, QtGui
from NewPWScreen import NewPWDialog
from ConfirmationDialog import ConfirmationDialog
import RequestController

#Constants
LOGOUT_MESSAGE = "Are you sure you would like to log out and close OpenDropOff?"

class HomeWindow(QtGui.QMainWindow):
    def __init__(self, requestController, parent=None):
        
        #Initialize the HomeWindow object
        QtGui.QMainWindow.__init__(self, parent)
        
        #Setup the request controller
        self.rc = requestController
        
        #Assign the homeWindow object
        self.ui = Ui_homeWindow()
        
        #Setup the window
        self.ui.setupUi(self)
        
        #Set up the New Password dialog and hide it
        self.newPWDialog = NewPWDialog(requestController)
        self.newPWDialog.hide()
        
        self.fileDialog = QtGui.QFileDialog()
        self.fileDialog.hide()
        
        # Get the users list of files and add them to the QTableWidget
        self.refreshFileList()
        
    #Handle events
    def changePw(self):
        self.newPWDialog.show()
        
    def selectionChanged(self):
        if( self.ui.fileTable.currentRow < 0):
            self.ui.downloadButton.setEnabled(False)
            self.ui.deleteButton.setEnabled(False)
        else:
            self.ui.downloadButton.setEnabled(True)
            self.ui.deleteButton.setEnabled(True)
        
    def addFile(self):
        #self.fileDialog.show()
        
        if self.fileDialog.exec_():
            selectedfiles = self.fileDialog.selectedFiles()
            
            if( len(selectedfiles) > 0 ):
                filename = selectedfiles.pop()["clientPath"]
                filesize = os.path.getsize(filename)
                self.rc.push(filename, filesize)
                
    def getFile(self):
        filename = self.ui.fileTable.item(self.ui.fileTable.currentRow(), 0).text()
        self.rc.pull( filename )
            
    
    def refreshFileList(self):
        self.ui.fileTable.clearContents()
        
        fileList = self.rc.listAll()
        for file in fileList:
            self.ui.fileTable.insertRow(0)
            newItem = QtGui.QTableWidgetItem()
            newItem.setText( file["clientPath"] )
            self.ui.fileTable.setItem(0, 0, newItem)
        print fileList       
        
    def logout(self):
        confirmCloseDialog = ConfirmationDialog(LOGOUT_MESSAGE)
        result = confirmCloseDialog.exec_()
        
        if( result == 0):
            self.close()
            #sys.exit()
            
    def closeEvent(self, event):
        self.rc.disconnect()
        event.accept()

class Ui_homeWindow(object):
    
    def setupUi(self, homeWindow):
        homeWindow.setObjectName("homeWindow")
        homeWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(homeWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(4, 520, 781, 25))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.usageLabel = QtGui.QLabel(self.centralwidget)
        self.usageLabel.setGeometry(QtCore.QRect(10, 481, 121, 20))
        self.usageLabel.setObjectName("usageLabel")
        self.usedLabel = QtGui.QLabel(self.centralwidget)
        self.usedLabel.setGeometry(QtCore.QRect(10, 500, 67, 17))
        self.usedLabel.setObjectName("usedLabel")
        self.maxLabel = QtGui.QLabel(self.centralwidget)
        self.maxLabel.setGeometry(QtCore.QRect(720, 500, 67, 17))
        self.maxLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.maxLabel.setObjectName("maxLabel")
        self.fileTable = QtGui.QTableWidget(self.centralwidget)
        self.fileTable.setGeometry(QtCore.QRect(5, 41, 791, 401))
        self.fileTable.setShowGrid(False)
        self.fileTable.setCornerButtonEnabled(False)
        self.fileTable.setColumnCount(3)
        self.fileTable.setObjectName("fileTable")
        self.fileTable.setColumnCount(3)
        self.fileTable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.fileTable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.fileTable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.fileTable.setHorizontalHeaderItem(2, item)
        self.fileTable.horizontalHeader().setCascadingSectionResizes(False)
        self.fileTable.horizontalHeader().setDefaultSectionSize(100)
        self.fileTable.horizontalHeader().setStretchLastSection(True)
        self.fileTable.verticalHeader().setCascadingSectionResizes(False)
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(400, 440, 391, 41))
        self.layoutWidget.setObjectName("layoutWidget")
        self.fileButtonLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.fileButtonLayout.setMargin(0)
        self.fileButtonLayout.setObjectName("fileButtonLayout")
        self.addButton = QtGui.QPushButton(self.layoutWidget)
        self.addButton.setObjectName("addButton")
        self.fileButtonLayout.addWidget(self.addButton)
        self.downloadButton = QtGui.QPushButton(self.layoutWidget)
        self.downloadButton.setEnabled(False)
        self.downloadButton.setObjectName("downloadButton")
        self.fileButtonLayout.addWidget(self.downloadButton)
        self.deleteButton = QtGui.QPushButton(self.layoutWidget)
        self.deleteButton.setEnabled(False)
        self.deleteButton.setObjectName("deleteButton")
        self.fileButtonLayout.addWidget(self.deleteButton)
        self.layoutWidget_2 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_2.setGeometry(QtCore.QRect(540, 0, 251, 41))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.accountButtonLayout = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.accountButtonLayout.setMargin(0)
        self.accountButtonLayout.setObjectName("accountButtonLayout")
        self.pwButton = QtGui.QPushButton(self.layoutWidget_2)
        self.pwButton.setObjectName("pwButton")
        self.accountButtonLayout.addWidget(self.pwButton)
        self.logoutButton = QtGui.QPushButton(self.layoutWidget_2)
        self.logoutButton.setObjectName("logoutButton")
        self.accountButtonLayout.addWidget(self.logoutButton)
        self.fileListLabel = QtGui.QLabel(self.centralwidget)
        self.fileListLabel.setGeometry(QtCore.QRect(10, 25, 211, 16))
        self.fileListLabel.setObjectName("fileListLabel")
        self.layoutWidget_3 = QtGui.QWidget(self.centralwidget)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 440, 122, 41))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.refreshButtonLayout_2 = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.refreshButtonLayout_2.setMargin(0)
        self.refreshButtonLayout_2.setObjectName("refreshButtonLayout_2")
        self.refreshButton = QtGui.QPushButton(self.layoutWidget_3)
        self.refreshButton.setObjectName("refreshButton")
        self.refreshButtonLayout_2.addWidget(self.refreshButton)
        homeWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(homeWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        homeWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(homeWindow)
        self.statusbar.setObjectName("statusbar")
        homeWindow.setStatusBar(self.statusbar)

        self.retranslateUi(homeWindow)
        QtCore.QObject.connect(self.pwButton, QtCore.SIGNAL("clicked()"), homeWindow.changePw)
        QtCore.QObject.connect(self.addButton, QtCore.SIGNAL("clicked()"), homeWindow.addFile)
        QtCore.QObject.connect(self.logoutButton, QtCore.SIGNAL("clicked()"), homeWindow.logout)
        QtCore.QObject.connect(self.fileTable, QtCore.SIGNAL("itemSelectionChanged()"), homeWindow.selectionChanged)
        QtCore.QObject.connect(self.downloadButton, QtCore.SIGNAL("clicked()"), homeWindow.getFile)
        QtCore.QMetaObject.connectSlotsByName(homeWindow)

    def retranslateUi(self, homeWindow):
        homeWindow.setWindowTitle(QtGui.QApplication.translate("homeWindow", "Open DropOff - Home Screen", None, QtGui.QApplication.UnicodeUTF8))
        self.usageLabel.setText(QtGui.QApplication.translate("homeWindow", "Current Usage", None, QtGui.QApplication.UnicodeUTF8))
        self.usedLabel.setText(QtGui.QApplication.translate("homeWindow", "0 MB", None, QtGui.QApplication.UnicodeUTF8))
        self.maxLabel.setText(QtGui.QApplication.translate("homeWindow", "2000 MB", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTable.setSortingEnabled(True)
        self.fileTable.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("homeWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTable.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("homeWindow", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.fileTable.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("homeWindow", "Active Revision Date", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("homeWindow", "Add New Files", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("homeWindow", "Download Files", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("homeWindow", "Delete Files", None, QtGui.QApplication.UnicodeUTF8))
        self.pwButton.setText(QtGui.QApplication.translate("homeWindow", "Change Password", None, QtGui.QApplication.UnicodeUTF8))
        self.logoutButton.setText(QtGui.QApplication.translate("homeWindow", "Logout", None, QtGui.QApplication.UnicodeUTF8))
        self.fileListLabel.setText(QtGui.QApplication.translate("homeWindow", "Files currently dropped off:", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("homeWindow", "Refresh File List", None, QtGui.QApplication.UnicodeUTF8))


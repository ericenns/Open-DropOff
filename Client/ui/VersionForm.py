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
        VersioForm.setObjectName("VersioForm")
        VersioForm.setWindowModality(QtCore.Qt.ApplicationModal)
        VersioForm.resize(420, 300)
        VersioForm.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(VersioForm)
        self.buttonBox.setGeometry(QtCore.QRect(70, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.treeView = QtGui.QTreeView(VersioForm)
        self.treeView.setGeometry(QtCore.QRect(20, 20, 281, 211))
        self.treeView.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.treeView.setObjectName("treeView")
        self.downloadButton = QtGui.QPushButton(VersioForm)
        self.downloadButton.setGeometry(QtCore.QRect(320, 20, 93, 28))
        self.downloadButton.setObjectName("downloadButton")

        self.retranslateUi(VersioForm)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), VersioForm.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), VersioForm.reject)
        QtCore.QMetaObject.connectSlotsByName(VersioForm)

    def retranslateUi(self, VersioForm):
        VersioForm.setWindowTitle(QtGui.QApplication.translate("VersioForm", "Versions", None, QtGui.QApplication.UnicodeUTF8))
        self.downloadButton.setText(QtGui.QApplication.translate("VersioForm", "Download", None, QtGui.QApplication.UnicodeUTF8))


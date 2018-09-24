#!/usr/bin/env python
#
# toy210 - the team210 live shader editor
#
# Copyright (C) 2017/2018 Alexander Kraus <nr4@z10.info>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import UiPreferencesDialog
import LicenseHeader

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

class PreferencesDialog(QDialog):
    def __init__(self, parent):
        super(PreferencesDialog, self).__init__()
        
        self.parent = parent
        self.ui = UiPreferencesDialog.Ui_PreferencesDialog()
        self.ui.setupUi(self)
        
        #fill fields
        head = self.parent.ui.tabWidget.currentWidget().license_header
        self.ui.lineEdit.setText(head.demoname)
        self.ui.lineEdit_2.setText(head.grouphandle)
        self.ui.comboBox.setCurrentText(head.compo)
        self.ui.lineEdit_3.setText(head.party)
        self.ui.comboBox_2.setCurrentText(head.license)
        self.ui.lineEdit_4.setText(head.author)
        self.ui.lineEdit_5.setText(head.email)
        self.ui.lineEdit_6.setText(head.year)
        self.ui.lineEdit_7.setText(head.authorhandle)
        
    def accept(self):
        super(PreferencesDialog, self).accept()
        
        self.parent.ui.tabWidget.currentWidget().license_header.demoname = self.ui.lineEdit.text()
        self.parent.ui.tabWidget.currentWidget().license_header.grouphandle = self.ui.lineEdit_2.text()
        self.parent.ui.tabWidget.currentWidget().license_header.compo = self.ui.comboBox.currentText()
        self.parent.ui.tabWidget.currentWidget().license_header.party = self.ui.lineEdit_3.text()
        self.parent.ui.tabWidget.currentWidget().license_header.license = self.ui.comboBox_2.currentText()
        self.parent.ui.tabWidget.currentWidget().license_header.author = self.ui.lineEdit_4.text()
        self.parent.ui.tabWidget.currentWidget().license_header.email = self.ui.lineEdit_5.text()
        self.parent.ui.tabWidget.currentWidget().license_header.year = self.ui.lineEdit_6.text()
        self.parent.ui.tabWidget.currentWidget().license_header.authorhandle = self.ui.lineEdit_7.text()
        self.hide()
        self.close()
        

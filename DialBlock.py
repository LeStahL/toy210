# toy210 - the team210 live shader editor
#
# Copyright (C) 2018  Alexander Kraus <nr4@z10.info>
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
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import numpy as np

import UiDialBlock

class DialBlock(QWidget):
    def __init__(self, parent):
        super(DialBlock, self).__init__()
        
        self.parent = parent
        
        self.ui = UiDialBlock.Ui_DialBlock()
        self.ui.setupUi(self)
        
        self.low = 0.
        self.high = 1.
        
        self.value = .5
        
        self.Logscale = False
        
        self.name = "p0"
        
        self.ui.lineEdit.setText(self.name)
        self.ui.radioButton_2.setChecked(self.Logscale)
        self.ui.radioButton.setChecked(not self.Logscale)
        
        self.ui.doubleSpinBox_3.setValue(self.value)
        self.ui.doubleSpinBox_2.setValue(self.high)
        self.ui.doubleSpinBox.setValue(self.low)
        
        r = int((self.value-self.low)/(self.high-self.low)*100.)
        
        self.ui.dial.setValue(r)
        self.ui.horizontalSlider.setValue(r)
        
    def lowChanged(self, value):
        self.low = float(self.ui.doubleSpinBox.value())
        
        if (self.low > self.high) or (self.low > self.value):
            self.low = self.high
            self.ui.doubleSpinBox.setValue(self.low)
        
        if self.low == self.high:
            return
        
        r = int((self.value-self.low)/(self.high-self.low)*100.)
        
        self.ui.dial.setValue(r)
        self.ui.horizontalSlider.setValue(r)
        
        return
    
    def highChanged(self, value):
        self.high = float(self.ui.doubleSpinBox_2.value())
        
        if (self.high < self.low) or (self.high < self.value):
            self.high = self.low
            self.ui.doubleSpinBox_2.setValue(self.high)
        
        if self.low == self.high:
            return
        
        r = int((self.value-self.low)/(self.high-self.low)*100.)
        
        self.ui.dial.setValue(r)
        self.ui.horizontalSlider.setValue(r)
        
        return
    
    def valueChanged(self, value):
        self.value = float(self.ui.doubleSpinBox_3.value())
        
        if (self.value < self.low):
            self.value = self.low
            self.ui.doubleSpinBox_3.setValue(self.value)
        if self.value > self.high:
            self.value = self.high
            self.ui.doubleSpinBox_3.setValue(self.value)
        
        if self.low == self.high:
            return
        
        r = int((self.value-self.low)/(self.high-self.low)*100.)
        
        self.ui.dial.setValue(r)
        self.ui.horizontalSlider.setValue(r)
        
        return
    
    def linSelected(self, state):
        self.Logscale = not state
        
        self.ui.radioButton_2.setChecked(self.Logscale)
        self.ui.radioButton.setChecked(not self.Logscale)
        return
    
    def logSelected(self, state):
        self.Logscale = state
        
        self.ui.radioButton_2.setChecked(self.Logscale)
        self.ui.radioButton.setChecked(not self.Logscale)
        
        return
    
    def dialTurned(self, value):
        if self.Logscale:
            return
            self.value = np.exp(self.low) + float(value)/float(self.ui.dial.maximum())*(np.exp(self.high) - np.exp(self.low))
        else:
            self.value = self.low + float(value)/float(self.ui.dial.maximum())*(self.high - self.low)
        
        self.ui.doubleSpinBox_3.setValue(self.value)
        
        return
    
    def sliderMoved(self, value):
        if self.Logscale:
            return
            self.value = np.exp(self.low) + float(value)/float(self.ui.horizontalSlider.maximum())*(np.exp(self.high) - np.exp(self.low))
        else:
            self.value = self.low + float(value)/float(self.ui.horizontalSlider.maximum())*(self.high - self.low)
        
        self.ui.doubleSpinBox_3.setValue(self.value)
        
        return
    
    def xPressed(self):
        self.parent.ui.verticalLayout_5.removeWidget(self)
        self.parent.dial_blocks.remove(self)
        self.setParent(None)
        del self
        return
    
    def nameChanged(self):
        self.name = self.ui.lineEdit.text()
        return 
    

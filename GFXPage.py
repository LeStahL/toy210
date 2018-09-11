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

import UiGFXPage

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from datetime import *

class GFXPage(QWidget):
    def __init__(self, parent):
        super(GFXPage, self).__init__()
        
        self.setParent(parent)
        self.ui = UiGFXPage.Ui_gfxPage()
        self.ui.setupUi(self)
        
        self.playing = False
        self.elapsed = 0.
        
        self.frametime = 1000./30.
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.setSingleShot(False)
        self.timer.start(self.frametime)
        
        self.starttime = datetime.now()
        self.fps = 0.
        
        self.parent = self.parentWidget()
        
    def modifyParent(self):
        if self.playing:
            self.parent.ui.actionPlay.setIcon(QIcon.fromTheme('media-playback-pause'))
        else:
            self.parent.ui.actionPlay.setIcon(QIcon.fromTheme('media-playback-start'))
        self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
        self.parent.ui.actionFPS_0.setText("FPS: 0")

    def pause(self):
        self.playing = not self.playing
        self.modifyParent()
        
    def tick(self):
        if self.playing:
            self.elapsed += self.frametime
            self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))

            now = datetime.now()
            dt = now - self.starttime
            self.parent.ui.actionFPS_0.setText('FPS: {:.1f}'.format(dt.total_seconds()*1.e3))
            self.starttime = now

    def forward(self):
        try: 
            self.elapsed = 1.e3*float(self.parent.ui.timeEdit.text())
            self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
        except ValueError:
            QMessageBox(QMessageBox.Critical, "Cast failed.", "Could not convert "+self.parent.timeEdit.text()+" to float.", QMessageBox.Ok).exec_()
            
        

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

import UiSFXPage

from SFXGLWidget import *

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from datetime import *

class SFXPage(QWidget):
    def __init__(self, parent):
        super(SFXPage, self).__init__()
   
        self.audiooutput = None
   
        self.setParent(parent)
        self.ui = UiSFXPage.Ui_sfxPage()
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
        
        self.defaultshader = '''vec2 mainSound( float time )
{
    // A 440 Hz wave that attenuates quickly overt time
    return vec2( sin(6.2831*440.0*time)*exp(-3.0*time) );
}'''
        self.ui.textEdit.insertPlainText(self.defaultshader)

        self.prefix = '''#version 130

uniform float iBlockOffset;
uniform float iSampleRate;'''
        self.suffix = '''void main()
{
   float t = iBlockOffset + ((gl_FragCoord.x-0.5) + (gl_FragCoord.y-0.5)*512.0)/iSampleRate;
   vec2 y = mainSound( t );
   vec2 v  = floor((0.5+0.5*y)*65536.0);
   vec2 vl = mod(v,256.0)/255.0;
   vec2 vh = floor(v/256.0)/255.0;
   gl_FragColor = vec4(vl.x,vh.x,vl.y,vh.y);
}'''

        self.filename = "Untitled SFX"
        self.music = None
                
    def modifyParent(self):
        if self.playing:
            self.parent.ui.actionPlay.setIcon(QIcon.fromTheme('media-playback-pause'))
        else:
            self.parent.ui.actionPlay.setIcon(QIcon.fromTheme('media-playback-start'))
        self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
        self.parent.ui.actionFPS_0.setText("Sample rate: 44.1 kHz")

    def pause(self):
        self.playing = not self.playing
        self.modifyParent()
        
        if self.audiooutput != None:
            if self.playing :
                self.audiooutput.start(self.audiobuffer)
            else :
                self.audiooutput.stop()
        
    def tick(self):
        if self.playing:
            self.elapsed += self.frametime
            self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))

            now = datetime.now()
            dt = now - self.starttime
            self.parent.ui.actionFPS_0.setText('Sample rate: 44.1 kHz')
            self.starttime = now
            
    def forward(self):
        try: 
            self.elapsed = 1.e3*float(self.parent.ui.timeEdit.text())
            self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
            self.pause()
            self.audiobuffer.reset()
            self.bytearray = QByteArray(self.music[int(self.parent.samplerate*self.elapsed*1.e-3)*4:])
            self.audiobuffer = QBuffer(self.bytearray)
            self.audiobuffer.open(QIODevice.ReadOnly)
            self.audiooutput = QAudioOutput(self.parent.audioformat)
            if not self.playing:
                self.audiooutput.stop()
            self.pause()
            
        except ValueError:
            QMessageBox(QMessageBox.Critical, "Cast failed.", "Could not convert "+self.parent.timeEdit.text()+" to float.", QMessageBox.Ok).exec_()
        except MemoryError:
            QMessageBox(QMessageBox.Critical, "Skip failed.", "Could not skip to "+self.parent.timeEdit.text()+" .", QMessageBox.Ok).exec_()
            
    def reset(self):
        self.elapsed = 0.
        self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
        self.pause()
        self.audiobuffer.reset()
        self.bytearray = QByteArray(self.music)
        self.audiobuffer = QBuffer(self.bytearray)
        self.audiobuffer.open(QIODevice.ReadOnly)
        self.audiooutput = QAudioOutput(self.parent.audioformat)
        if not self.playing:
            self.audiooutput.stop()
        self.pause()
        
    def close(self):
        if self.ui.textEdit.undostack.isClean():
            self.parent.ui.tabWidget.removeTab(self.parent.ui.tabWidget.indexOf(self))

    def fullShader(self):
        return self.prefix + self.ui.textEdit.toPlainText() + self.suffix

    def compileShader(self):
        glwidget = SFXGLWidget(self)
        
        glwidget.move(10000.,1000.)
        glwidget.show()
        self.log = glwidget.newShader(self.fullShader())
        self.ui.textEdit_2.setPlainText(self.log)
        self.music = glwidget.music
        
        glwidget.hide()
        glwidget.destroy()
        
        self.bytearray = QByteArray(self.music)
        
        self.audiobuffer = QBuffer(self.bytearray)
        self.audiobuffer.open(QIODevice.ReadOnly)
        
        self.audiooutput = QAudioOutput(self.parent.audioformat)
        self.audiooutput.stop()

        #self.parentWidget().stream.write(self.music)
        

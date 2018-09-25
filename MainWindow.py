#!/usr/bin/env python3
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

import UiMainWindow
from GFXPage import *
from SFXPage import *
from Preferences import *
from PreferencesDialog import *

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from OpenGL.GL import *
from OpenGL.GLU import *
import datetime
from numpy import *

from PyQt5.QtChart import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.samplerate = 44100
        self.nchannels = 2
        
        self.audioformat = QAudioFormat()
        self.updateAudioFormat()
        
        self.audiodeviceinfo = QAudioDeviceInfo(QAudioDeviceInfo.defaultOutputDevice())
        
        self.ui = UiMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.timeEdit = QLineEdit("22.3", self)
        self.ui.timeEdit.setEnabled(False)
        self.ui.toolBar_3.addWidget(self.ui.timeEdit)
        
        self.pages = []
        
        self.ui.tabWidget.setTabsClosable(True)
        
        self.preferences = Preferences(".toy210")
        self.preferences.load()
        
        # Populate recent projects list
        if self.preferences.hasRecents():
            self.ui.menu_Recent.removeAction(self.ui.actionNone)
            for filename in self.preferences.recentfiles:
                self.ui.menu_Recent.addAction(QAction(QIcon(None), filename, self.ui.menu_Recent))
        
        # TODO fix icons on windows
        #self.ui.actionClose.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        #self.ui.actionCompile.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        #self.ui.actionCopy
        
    def updateAudioFormat(self) :
        self.audioformat.setSampleRate(self.samplerate)
        self.audioformat.setChannelCount(self.nchannels)
        self.audioformat.setSampleSize(32)
        self.audioformat.setCodec("audio/pcm")
        self.audioformat.setByteOrder(QAudioFormat.LittleEndian)
        self.audioformat.setSampleType(QAudioFormat.Float)
        
    def newSFX(self):
        page = SFXPage(self)
        self.ui.tabWidget.addTab(page, QIcon(), "Untitled SFX*")
        self.ui.tabWidget.setCurrentWidget(page)
        self.pages += [page]
    
    def newGFX(self):
        page = GFXPage(self)
        self.ui.tabWidget.addTab(page, QIcon(), "Untitled GFX*")
        self.ui.tabWidget.setCurrentWidget(page)
        self.pages += [page]
        
    def updateTime(self, text):
        self.ui.actionTime.setText(text)
        
    def tabSwitched(self, index):
        if isinstance(self.ui.tabWidget.widget(index), GFXPage):
            self.enableEdit(True)
            self.enablePlayback(True)
            self.enableCapture(True, False, False)
            self.ui.tabWidget.widget(index).modifyParent()
        elif isinstance(self.ui.tabWidget.widget(index), SFXPage):
            self.enableEdit(True)
            self.enablePlayback(True)
            self.enableCapture(False, True, False)
            self.ui.tabWidget.widget(index).modifyParent()
        else: # Welcome Page
            self.enableEdit(False)
            self.enablePlayback(False)
            self.enableCapture(False, False, False)
        self.setWindowTitle("Toy210 - " + self.ui.tabWidget.tabText(index))
            
    def enableEdit(self, state):
        self.ui.actionUndo.setEnabled(state)
        self.ui.actionRedo.setEnabled(state)
        self.ui.actionCut.setEnabled(state)
        self.ui.actionCopy.setEnabled(state)
        self.ui.actionPaste.setEnabled(state)
        self.ui.actionDelete.setEnabled(state)
        self.ui.actionSelect_all.setEnabled(state)
    
    def enablePlayback(self, state):
        self.ui.actionPlay.setEnabled(state)
        self.ui.actionReset.setEnabled(state)
        self.ui.actionTime.setEnabled(state)
        self.ui.timeEdit.setEnabled(state)
        self.ui.actionSeek.setEnabled(state)
        
    def enableCapture(self, screen, sound, vid):
        self.ui.actionScreenshot.setEnabled(screen)
        self.ui.actionStream.setEnabled(sound)
        self.ui.actionVideo.setEnabled(vid)
        
    def quit(self):
        saved = True
        for page in self.pages:
            self.ui.tabWidget.setCurrentWidget(page)
            saved = saved and page.close()
            if saved:
                self.ui.tabWidget.removeTab(self.ui.tabWidget.indexOf(page))
        if saved:
            self.preferences.save()
            qApp.quit()
            return
    
    def pause(self):
        self.ui.tabWidget.currentWidget().pause()
        
    def forward(self):
        self.ui.tabWidget.currentWidget().forward()
        
    def reset(self):
        self.ui.tabWidget.currentWidget().reset()

    def closeOnly(self):
        saved = self.ui.tabWidget.currentWidget().close()
        if saved:
            self.ui.tabWidget.removeTab(self.ui.tabWidget.currentWidget())
        
    def closeRequested(self, index):
        saved = self.ui.tabWidget.widget(index).close()
        if saved:
            self.ui.tabWidget.removeTab(self.ui.tabWidget.widget(index).close())
            
    def compile(self):
        self.ui.tabWidget.currentWidget().compileShader()
        
    def copy(self):
        self.ui.tabWidget.currentWidget().copy()
        
    def paste(self):
        self.ui.tabWidget.currentWidget().paste()
        
    def cut(self):
        self.ui.tabWidget.currentWidget().cut()
        
    def delete(self):
        self.ui.tabWidget.currentWidget().delete()
        
    def selectAll(self):
        self.ui.tabWidget.currentWidget().selectAll()
        
    def undo(self):
        print ("undone.")
        self.ui.tabWidget.currentWidget().undo()
    
    def redo(self):
        self.ui.tabWidget.currentWidget().redo()
        
    def openFile(self):
        filename = str(QFileDialog.getOpenFileName(self, "Open...", "", "Shaders (*.frag)")[0])
        
        if filename == "":
            return
        
        #FIXME add recent files
        #self.preferences.addRecent(filename)
        #self.preferences.openfiles += [ filename ]
        
        lines = None
        filetext = ""
        try:
            with open(filename, "rt") as f:
                filetext = f.read()
                lines = filetext.split('\n')
                f.close()
        except:
            msg = QMessageBox(QMessageBox.Error, "Could not open file...", "Could not open file " + filename + ".", QMessageBox.Ok)
            result = msg.exec_()
            return
        
        page = None
        if "mainSound" in filetext:
            page = SFXPage(self)
            self.ui.tabWidget.addTab(page, QIcon(), filename)
            self.ui.tabWidget.setCurrentWidget(page)
            self.pages += [page]
        elif "mainImage" in filetext:
            page = GFXPage(self)
            self.ui.tabWidget.addTab(page, QIcon(), filename)
            self.ui.tabWidget.setCurrentWidget(page)
            self.pages += [page]
        else:
            result = QMessageBox(QMessageBox.Error, "Shader type not known.", "File contains a shader that can not be loaded by toy210.", QMessageBox.Ok).exec_()
            return
        
        header = '\n'.join(lines[:16])
        page.license_header.fromString(header)
        
        body = filetext.replace(header, "").replace(page.prefix, "").replace(page.suffix, "")
        page.ui.textEdit_2.setPlainText(body)
        
    def saveFile(self):
        self.ui.tabWidget.currentWidget().save()
        
    def saveAs(self):
        self.ui.tabWidget.currentWidget().saveAs()
        
    def preferences(self):
        dialog = PreferencesDialog(self)
        dialog.exec()

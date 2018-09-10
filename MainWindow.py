#!/usr/bin/env python

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

from GLWidget import *
from SFXGLWidget import *
from SyntaxHighlighter import *

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
import datetime
from numpy import *

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
    
        self.splitter1 = QSplitter(self)
        self.splitter2 = QSplitter(self)
        self.splitter2.setOrientation(Qt.Vertical)
        self.visuals = glWidget(self)
        self.splitter2.addWidget(self.visuals)
        self.toolbarlayout = QHBoxLayout(self)
        self.toolbarlayout.setContentsMargins(0,0,0,0)
        self.timelabel = QLabel(self)
        self.timelabel.setText("00:00.000")
        self.toolbarlayout.addWidget(self.timelabel)
        self.playbutton = QPushButton(self)
        self.playbutton.setText(">")
        self.playbutton.clicked.connect(self.pauseTime)
        self.toolbarlayout.addWidget(self.playbutton)
        self.resetbutton = QPushButton(self)
        self.resetbutton.setText("|<")
        self.resetbutton.clicked.connect(self.resetTime)
        self.toolbarlayout.addWidget(self.resetbutton)
        self.forwardedit = QLineEdit(self)
        self.toolbarlayout.addWidget(self.forwardedit)
        self.forwardbutton = QPushButton(self)
        self.forwardbutton.setText(">>")
        self.forwardbutton.clicked.connect(self.forward)
        self.toolbarlayout.addWidget(self.forwardbutton)
        self.toolbarwidget = QWidget(self)
        self.toolbarwidget.setLayout(self.toolbarlayout)
        self.splitter2.addWidget(self.toolbarwidget)
        self.debugoutput = QTextEdit(self)
        self.splitter2.addWidget(self.debugoutput)
        self.splitter1.addWidget(self.splitter2)
        self.editor = QTextEdit(self)
        self.editor.setMinimumWidth(512)
        self.editor.textChanged.connect(self.textChanged)
        self.splitter1.addWidget(self.editor)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.menubar = QMenuBar(self)
        self.menubar.setMaximumHeight(25.)
        self.filemenu = self.menubar.addMenu("&File")
        self.filenew = self.filemenu.addAction("&New GFX")
        self.filenew.setShortcut("CTRL+N")
        self.filenewsfx = self.filemenu.addAction("New SFX")
        self.filenewsfx.setShortcut("CTRL+SHIFT+N")
        self.fileopen = self.filemenu.addAction("&Open GFX")
        self.fileopen.setShortcut("CTRL+O")
        self.fileopen.triggered.connect(self.openFile)
        self.fileopensfx = self.filemenu.addAction("Open SFX")
        self.fileopensfx.setShortcut("CTRL+SHIFT+O")
        self.filemenu.addSeparator()
        self.filesave = self.filemenu.addAction("&Save GFX")
        self.filesave.setShortcut("CTRL+S")
        self.filesave.triggered.connect(self.save)
        self.filesavesfx = self.filemenu.addAction("Save SFX")
        self.filesavesfx.setShortcut("CTRL+SHIFT+S")
        self.filesaveas = self.filemenu.addAction("Save &as...")
        self.filesaveas.triggered.connect(self.saveAs)
        self.filemenu.addSeparator()
        self.filequit = self.filemenu.addAction("&Quit")
        self.filequit.setShortcut('CTRL+Q')
        self.filequit.triggered.connect(self.quit)
        self.editmenu = self.menubar.addMenu("&Edit")
        self.viewmenu = self.menubar.addMenu("&View")
        self.shadermenu = self.menubar.addMenu("&Shader")
        self.shadercompile = self.shadermenu.addAction("&Compile GFX")
        self.shadercompile.setShortcut('F5')
        self.shadercompile.triggered.connect(self.compileShader)
        self.shadercompilesfx = self.shadermenu.addAction("&Compile SFX")
        self.shadercompilesfx.setShortcut("SHIFT+F5")
        self.shadercompilesfx.triggered.connect(self.compileShaderSFX)
        self.helpmenu = self.menubar.addMenu("&Help")
        self.helpabout = self.helpmenu.addAction("&About")
        self.mainLayout.addWidget(self.menubar)
        self.setLayout(self.mainLayout)
        
        self.tabwidget = QTabWidget(self)
        self.gfxtab = QWidget(self.tabwidget)
        self.gfxtab.setLayout(QVBoxLayout(self.gfxtab))
        self.gfxtab.layout().addWidget(self.splitter1)
        self.mainLayout.addWidget(self.tabwidget)
        self.tabwidget.addTab(self.gfxtab, QIcon(), "GFX")
        
        self.splitter3 = QSplitter(self)
        self.splitter3.setOrientation(Qt.Horizontal)
        
        self.sfxtab = QWidget(self.tabwidget)
        self.sfxtab.setLayout(QVBoxLayout(self.sfxtab))
        self.sfxtab.layout().addWidget(self.splitter3)
        self.tabwidget.addTab(self.sfxtab, QIcon(), "SFX")
        
        self.splitter4 = QSplitter(self)
        self.splitter4.setOrientation(Qt.Vertical)
        self.editorsfx = QTextEdit(self)
        self.splitter3.addWidget(self.splitter4)
        self.splitter3.addWidget(self.editorsfx)
        
        self.sfxglwidget = sfxGLWidget(self)
        self.splitter4.addWidget(self.sfxglwidget)
        
        self.customsource = "void mainImage( out vec4 fragColor, in vec2 fragCoord )\n\
{\n\
    // Normalized pixel coordinates (from 0 to 1)\n\
    vec2 uv = fragCoord/iResolution.xy;\n\
\n\
    // Time varying pixel color\n\
    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));\n\
\n\
    // Output to screen\n\
    fragColor = vec4(col,1.0);\n\
}\n\n"
        self.editor.insertPlainText(self.customsource)
        self.prefix = "\n#version 130\n\
\n\
uniform float iTime;\n\
uniform vec2 iResolution;\n\n"
        self.suffix = "void main()\n\
{\n\
    mainImage(gl_FragColor, gl_FragCoord.xy);\n\
}\n"

        self.sfxcustomsource = "vec2 mainSound( float time )\n\
{\n\
    // A 440 Hz wave that attenuates quickly overt time\n\
    return vec2( sin(6.2831*440.0*time)*exp(-3.0*time) );\n\
}\n\n"
        self.sfxprefix = "\n#version 130\n\
\n\
uniform float iBlockOffset;\n\
uniform float iSampleRate;\n\n"
        self.sfxsuffix = "\n\nvoid main()\n\
{\n\
   float t = iBlockOffset + ((gl_FragCoord.x-0.5) + (gl_FragCoord.y-0.5)*512.0)/iSampleRate;\n\
   vec2 y = mainSound( t );\n\
   vec2 v  = floor((0.5+0.5*y)*65536.0);\n\
   vec2 vl = mod(v,256.0)/255.0;\n\
   vec2 vh = floor(v/256.0)/255.0;\n\
   gl_FragColor = vec4(vl.x,vh.x,vl.y,vh.y);\n\
}\n"
        self.editorsfx.insertPlainText(self.sfxcustomsource)
        
        self.running = True
        self.startpause = datetime.datetime.now()
        
        self.clean = True
        self.filename = ""
        
        self.highlight = SyntaxHighlighter(self.editor.document())
    
    def compileShaderSFX(self) :
        log = self.sfxglwidget.newShader(self.sfxprefix + self.editorsfx.toPlainText() + self.sfxsuffix).decode('utf-8')
        print(log)

    def compileShader(self) :
        log = self.visuals.newShader(self.prefix + self.editor.toPlainText() + self.suffix).decode('utf-8')
        self.debugoutput.setPlainText(log)
        
        #TODO: Syntax highlighting here
        #for line in log.split('\n') :
            #print(line)
    
    def resetTime(self) :
        self.visuals.dst = datetime.datetime.now()
        self.visuals.starttime = self.visuals.dst.minute*60.+self.visuals.dst.second*1.+self.visuals.dst.microsecond*1.e-6
        self.visuals.time = 0.
        self.startpause = datetime.datetime.now()
        self.visuals.tick()
        self.visuals.paintGL()

    def pauseTime(self) :
        self.running = not self.running
        if self.running :
            self.visuals.timer.start(1000./30.)
            self.visuals.dst = self.visuals.dst + (datetime.datetime.now()-self.startpause)
            self.visuals.starttime = self.visuals.dst.minute*60.+self.visuals.dst.second*1.+self.visuals.dst.microsecond*1.e-6
            
        else :
            self.visuals.timer.stop()
            self.startpause = datetime.datetime.now()
        self.visuals.paintGL()
    
    def forward(self):
        if self.forwardedit.text().isnumeric():
            self.visuals.dst = datetime.datetime.now() - datetime.timedelta(0,float(self.forwardedit.text()))
            self.visuals.starttime = self.visuals.dst.minute*60.+self.visuals.dst.second*1.+self.visuals.dst.microsecond*1.e-6
            self.visuals.time = float(self.forwardedit.text())
            self.startpause = datetime.datetime.now()
            self.visuals.tick()
            self.visuals.paintGL()
        else:
            m = QMessageBox()
            m.setIcon(QMessageBox.Warning)
            m.setInformativeText("That's no number you useless piece of shit!")
            m.setStandardButtons(QMessageBox.Ok)
            m.exec_()
            return
        
    def textChanged(self) :
        text = self.editor.toPlainText()
        if '\t' in text:
            cursor = self.editor.textCursor()
            pos = cursor.position()
            text = text.replace('\t', '    ')
            self.editor.setPlainText(text)
            cursor.setPosition(pos+3)
            self.editor.setTextCursor(cursor)
            self.editor.update()
        self.clean = False
        
    def quit(self) :
        if self.clean :
            qApp.quit()
        else :
            m = QMessageBox()
            m.setIcon(QMessageBox.Warning)
            m.setText("Unsaved progress. Save before exiting?")
            m.setInformativeText("The shader contains unsaved modifications. Save before exiting?")
            m.setWindowTitle("Save changes before exiting?")
            m.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            m.buttonClicked.connect(self.quitBoxHandler)
            m.exec_()
            return
    
    def quitBoxHandler(self, i) :
        if i.text() == "&Yes" :
            self.save()
        elif i.text() == "&Cancel" :
            return
        qApp.quit()
            
    def save(self) :
        if self.filename == "" :
            self.saveAs()
            return
        if self.filename == "" :
            return
        with open(self.filename, "wt") as f :
            f.write(self.prefix + self.editor.toPlainText() + self.suffix)
            f.close()
        self.clean = True

    def saveAs(self) :
        was_running = self.running
        if self.running :
            self.pauseTime()
            
        self.filename = str(QFileDialog.getSaveFileName(self, "Save As...","","Shaders (*.frag *.glsl)")[0])
        if self.filename == "" : return
        self.save()
        
        if was_running :
            self.pauseTime()
        
    def openFile(self) :
        was_running = self.running
        if self.running :
            self.pauseTime()
            
        self.filename = str(QFileDialog.getOpenFileName(self, "Open...","","Shaders (*.frag *.glsl)")[0])
        if self.filename == "" : return
        
        shadertext = ""
        self.editor.setPlainText("")
        with open(self.filename, "rt") as f :
            shadertext = f.read()
            f.close()
        shadertext = shadertext.replace(self.prefix, "")
        shadertext = shadertext.replace(self.suffix, "")
        self.editor.setPlainText(shadertext)
        self.editor.update()
        
        self.clean = True
        
        if was_running :
            self.pauseTime()

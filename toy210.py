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

import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
import datetime
from numpy import *
from struct import *

class SyntaxHighlighter(QSyntaxHighlighter) :
    type_ids = [ 'vec2', 'vec3', 'int', 'vec4', 'mat2', 'mat3', 'mat4', 'void', 'float' ]
    flow_ids = [ 'in', 'out', 'uniform', 'const' ]
    syntax_ids = [ 'for', 'if', 'while', 'struct', 'return', 'else' ]
    operator_ids = [ '\+', '-', '\*', '/', '\+=', '-=', '*=', '/=', '==', '!=', '\,', '\.' ]
    builtin_ids = [ 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
                   'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh', 
                   'normalize', 'abs', 'length', 'dot', 'reflect', 'refract',
                   'mod', 'fract', 'ceil', 'floor', 'round', 'step', 'smoothstep', 'mix',
                   'max', 'min', 'pow', 'sqrt', 'sign', 'clamp']
    brace_ids = [ '{', '}', '(', ')', '[', ']' ]
    
    color_names = [ 'darkBlue', 'darkMagenta', 'blue', 'red', 'darkGreen', 'orange', 'black', 'lightGray', 'darkGreen', 'purple' ]
    styles_bold = [ True, True, True, True, True, True, False, False, False, False ]
    styles_italic = [ False, False, False, False, False, False, False, True, False, False ]
    formats = []
    rules = []
    
    def __init__(self, document) :
        QSyntaxHighlighter.__init__(self, document)

        for i in range(10) :
            color = QColor()
            color.setNamedColor(self.color_names[i])
            
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            if self.styles_bold[i] : fmt.setFontWeight(QFont.Bold)
            fmt.setFontItalic(self.styles_italic[i])
            
            self.formats += [ fmt ]
        
        rules = []
        rules += [ (r'//[^\n]*', 0, self.formats[8]) ] # oneline comment
        rules += [ (r'/[^\*\\]*(\\.[^*/\\]*)*"', 0, self.formats[8]) ] # multiline comment
        rules += [ (r'#[^\n]*', 0, self.formats[9]) ] # preprocessor
        rules += [ (r'\b%s\b' % idf, 0, self.formats[0]) for idf in self.type_ids ]
        rules += [ (r'\b%s\b' % idf, 0, self.formats[1]) for idf in self.flow_ids ]
        rules += [ (r'\b%s\b' % idf, 0, self.formats[2]) for idf in self.syntax_ids ]
        rules += [ (r'%s' % idf, 0, self.formats[3]) for idf in self.operator_ids ]
        rules += [ (r'\b%s\b' % idf, 0, self.formats[4]) for idf in self.builtin_ids ]
        rules += [ (r'\.[xyz]+', 0, self.formats[5]) ]
        rules += [ (r'%s' % idf, 0, self.formats[6]) for idf in self.brace_ids ]
        rules += [ (r'\b[+-]?[0-9]+[lL]?\b', 0, self.formats[9]) ]
        rules += [ (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.formats[9]) ]
        rules += [ (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.formats[9]) ]
        
        self.rules = [ (QRegExp(s), index, fmt) for (s, index, fmt) in rules ]
        
    def highlightBlock(self, text) :
        for expression, nth, format in self.rules:
            index = expression.indexIn(text, 0)
        
            while index >= 0:
                index = expression.pos(nth)
                length = len(expression.cap(nth))
                self.setFormat(index, length, format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)
        
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
        
class sfxGLWidget(QOpenGLWidget,QObject):
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.setMinimumSize(512,512)
        self.setMaximumSize(512,512)
        self.resize(512,512)
        self.program = 0
        self.iSampleRateLocation = 0
        self.iBlockOffsetLocation = 0
        self.hasShader = False
        self.parent = parent
        self.duration = 60. #1 min of sound
        self.samplerate = 44100 #TODO: add selector to code
        self.nsamples = 2*self.duration*self.samplerate
        self.nblocks = int(ceil(float(self.nsamples)/float(512*512)))
        self.blocksize = 512*512
        self.nsamples_real = 2*self.nblocks*self.blocksize
        self.duration_real = float(self.nsamples_real)/float(self.samplerate)
        self.image = [0]*self.blocksize*2
    
    def paintGL(self):
        return
    
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        
        self.framebuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 512, 512, 0, GL_RGBA, GL_BYTE, self.image)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, self.texture, 0)
        
    def newShader(self, source) :
        self.shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.shader, source)
        glCompileShader(self.shader)
        
        status = glGetShaderiv(self.shader, GL_COMPILE_STATUS)
        if status != GL_TRUE :
            log = glGetShaderInfoLog(self.shader)
            return log
        
        self.program = glCreateProgram()
        glAttachShader(self.program, self.shader)
        glLinkProgram(self.program)
        
        status = glGetProgramiv(self.program, GL_LINK_STATUS)
        if status != GL_TRUE :
            log = glGetProgramInfoLog(self.program)
            return log
        
        self.iBlockOffsetLocation = glGetUniformLocation(self.program, 'iBlockOffset')
        self.iSampleRateLocation = glGetUniformLocation(self.program, 'iSampleRate')
        
        music = []
        glUseProgram(self.program)
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffer)
        
        for i in range(self.nblocks) :
            glUniform1f(self.iBlockOffsetLocation, float(i*self.blocksize))
            glUniform1f(self.iSampleRateLocation, self.samplerate) 
            
            glViewport(0,0,512,512)
            
            glBegin(GL_QUADS);
            glVertex3f(-1,-1,0);
            glVertex3f(-1,1,0);
            glVertex3f(1,1,0);
            glVertex3f(1,-1,0);
            glEnd();

            glFlush();
            
            music_i = glReadPixels(0, 0, 512, 512, GL_RGBA, GL_BYTE)
            
            #FIXME: remove shit
            print(music_i)
            
            music += [ music_i ]
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        left = []
        right = []
        #for chunk in music :
            #print(len(chunk))
            #(l,r) = unpack("e", str(byte))
            #left += [l]
            #right += [r]
        #print left
        return b'Success.'
        
class glWidget(QOpenGLWidget,QObject):
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.program = 0
        self.iTimeLocation = 0
        self.iResolutionLocation = 0
        self.hasShader = False
        self.dst = datetime.datetime.now()
        self.starttime = self.dst.minute*60.+self.dst.second*1.+self.dst.microsecond*1.e-6
        self.time = 0.
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.setSingleShot(False)
        self.timer.start(1000./30.)
        
        self.parent = parent

    def tick(self) :
        dt = datetime.datetime.now()
        self.time = dt.minute*60.+dt.second*1.+dt.microsecond*1.e-6 - self.starttime
        self.repaint()
        self.parent.timelabel.setText(str(dt-self.dst))
        self.parent.timelabel.repaint()

    def paintGL(self):
        if self.hasShader :
            glUseProgram(self.program)
            
            glUniform1f(self.iTimeLocation, self.time)
            glUniform2f(self.iResolutionLocation, self.width(), self.height())
            
        glClearColor(0.,0.,0.,1.)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glColor3f( 1.0, 1.5, 0.0)
        glPolygonMode(GL_FRONT, GL_FILL)

        glBegin(GL_TRIANGLES)
        glVertex3f(-1.,-1.,0.)
        glVertex3f(-1.,1.,0.)
        glVertex3f(1.,1.,0.)
        
        glVertex3f(1.,1.,0.)
        glVertex3f(1.,-1.,0.)
        glVertex3f(-1.,-1.,0.)
        glEnd()

        glFlush()
        
    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        
    def newShader(self, source) :
        self.shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.shader, source)
        glCompileShader(self.shader)
        
        status = glGetShaderiv(self.shader, GL_COMPILE_STATUS)
        if status != GL_TRUE :
            log = glGetShaderInfoLog(self.shader)
            return log
        
        self.program = glCreateProgram()
        glAttachShader(self.program, self.shader)
        glLinkProgram(self.program)
        
        status = glGetProgramiv(self.program, GL_LINK_STATUS)
        if status != GL_TRUE :
            log = glGetProgramInfoLog(self.program)
            return log
        
        self.iTimeLocation = glGetUniformLocation(self.program, 'iTime')
        self.iResolutionLocation = glGetUniformLocation(self.program, 'iResolution')
        
        self.repaint()
        
        self.hasShader = True
        
        return b'Success.'



if __name__ == '__main__':
    app = QApplication(['Toy210'])
    window = MainWindow()
    window.show()
    app.exec_()

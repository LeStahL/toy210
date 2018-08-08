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
from OpenGL.GL import *
from OpenGL.GLU import *
import datetime

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
        self.toolbarlayout.addWidget(self.playbutton)
        self.resetbutton = QPushButton(self)
        self.toolbarlayout.addWidget(self.resetbutton)
        self.toolbarwidget = QWidget(self)
        self.toolbarwidget.setLayout(self.toolbarlayout)
        self.splitter2.addWidget(self.toolbarwidget)
        self.debugoutput = QTextEdit(self)
        self.splitter2.addWidget(self.debugoutput)
        self.splitter1.addWidget(self.splitter2)
        self.editor = QTextEdit(self)
        self.editor.setMinimumWidth(512)
        self.splitter1.addWidget(self.editor)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.menubar = QMenuBar(self)
        self.filemenu = self.menubar.addMenu("&File")
        self.filenew = self.filemenu.addAction("&New")
        self.fileopen = self.filemenu.addAction("&Open")
        self.filemenu.addSeparator()
        self.filesave = self.filemenu.addAction("&Save")
        self.filesaveas = self.filemenu.addAction("Save &as...")
        self.filemenu.addSeparator()
        self.filequit = self.filemenu.addAction("&Quit")
        self.filequit.setShortcut('CTRL+Q')
        self.filequit.triggered.connect(qApp.quit)
        self.editmenu = self.menubar.addMenu("&Edit")
        self.viewmenu = self.menubar.addMenu("&View")
        self.shadermenu = self.menubar.addMenu("&Shader")
        self.shadercompile = self.shadermenu.addAction("&Compile")
        self.shadercompile.setShortcut('F5')
        self.shadercompile.triggered.connect(self.compileShader)
        self.helpmenu = self.menubar.addMenu("&Help")
        self.helpabout = self.helpmenu.addAction("&About")
        self.mainLayout.addWidget(self.menubar)
        self.mainLayout.addWidget(self.splitter1)
        self.setLayout(self.mainLayout)
        
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

        self.compileShader()

    def compileShader(self) :
        print self.prefix + self.editor.toPlainText() + self.suffix
        log = self.visuals.newShader(self.prefix + self.editor.toPlainText() + self.suffix)
        self.debugoutput.setPlainText(log)

class glWidget(QOpenGLWidget):
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        self.program = 0
        self.iTimeLocation = 0
        self.iResolutionLocation = 0
        self.hasShader = False

    def paintGL(self):
        if self.hasShader :
            glUseProgram(self.program)
        
            dt = datetime.datetime.now()
            time = dt.minute*60.+dt.second*1.+dt.microsecond*1.e-6
            print time
            
            glUniform1f(self.iTimeLocation, time)
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
        
        return "Success."

if __name__ == '__main__':
    app = QApplication(['Toy210'])
    window = MainWindow()
    window.show()
    app.exec_()

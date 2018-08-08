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
        self.helpmenu = self.menubar.addMenu("&Help")
        self.helpabout = self.helpmenu.addAction("&About")
        self.mainLayout.addWidget(self.menubar)
        self.mainLayout.addWidget(self.splitter1)
        self.setLayout(self.mainLayout)

class glWidget(QOpenGLWidget):
    def __init__(self, parent):
        QOpenGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)

    def paintGL(self):
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

if __name__ == '__main__':
    app = QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()

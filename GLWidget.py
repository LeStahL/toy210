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

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from OpenGL.GL import *
from OpenGL.GLU import *
import datetime
from numpy import *
from struct import *

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

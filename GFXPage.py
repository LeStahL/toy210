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
import PreferencesDialog

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.Qt import *

from datetime import *
from LicenseHeader import *

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
        
        self.defaultshader = '''const float pi = acos(-1.);
const vec3 c = vec3(1.,0.,-1.);

// hash function
float r(vec2 a0)
{
    return fract(sin(dot(a0.xy ,vec2(12.9898,78.233)))*43758.5453);
}

// compute distance to regular star
float dstar(vec2 x, float N, vec2 R)
{
    float d = pi/N,
        p0 = acos(x.x/length(x)),
        p = mod(p0, d),
        i = mod(round((p-p0)/d),2.);
    x = length(x)*vec2(cos(p),sin(p));
    vec2 a = mix(R,R.yx,i),
    	p1 = a.x*c.xy,
        ff = a.y*vec2(cos(d),sin(d))-p1;
   	ff = ff.yx*c.zx;
    return dot(x-p1,ff)/length(ff);
}

#define A iResolution.y
#define B 3./Y
#define S(v) smoothstep(-1.5/A,1.5/A,v)
void mainImage( out vec4 fragColor, in vec2 fragCoord )
{
    float a = .1, aa = .5*a; // tile size
    vec2 uv = fragCoord/A+.5,
        x = mod(uv, a)-aa, y = uv-x; // we want many polygons
    
    //random number of edges and random rotation
    float p = 5.*r(y)*iTime,
        k = cos(p), s = sin(p),
        d = dstar(mat2(k,s,-s,k)*x, 3.+floor(8.*r(y)), vec2(.15,.45)*a); 
    
    //set random colors
    vec3 col = .5 + .5*cos(p+uv.xyx+vec3(0.,2.,4.));
    fragColor = vec4(col*mix(S(d),1.,.5)+S(-abs(d)),1.);
    
    //add borders
    vec2 v = smoothstep(-aa,-aa+1.5/A,x)*smoothstep(aa,aa-1.5/A,x);
    fragColor *= v.x*v.y;
}'''
        self.ui.textEdit_2.insertPlainText(self.defaultshader)
      
        self.prefix = '''#version 130
uniform float iTime;
uniform vec2 iResolution;'''
        self.suffix = '''void main()
{
    mainImage(gl_FragColor, gl_FragCoord.xy);
}'''

        self.filename = "Untitled GFX"
        self.license_header = LicenseHeader()
        
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
            
        self.ui.openGLWidget.time = self.elapsed*1.e-3
        self.ui.openGLWidget.repaint()

    def forward(self):
        try: 
            self.elapsed = 1.e3*float(self.parent.ui.timeEdit.text())
            self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
            self.ui.openGLWidget.time = self.elapsed*1.e-3
            self.ui.openGLWidget.repaint()
        except ValueError:
            QMessageBox(QMessageBox.Critical, "Cast failed.", "Could not convert "+self.parent.timeEdit.text()+" to float.", QMessageBox.Ok).exec_()
            
    def reset(self):
        self.elapsed = 0.
        self.parent.ui.actionTime.setText("{:.3f}".format(self.elapsed*1.e-3))
        self.ui.openGLWidget.time = self.elapsed*1.e-3
        self.ui.openGLWidget.repaint()
        
    def close(self):
        if self.ui.textEdit_2.undostack.isClean():
            self.parent.ui.tabWidget.removeTab(self.parent.ui.tabWidget.indexOf(self))

    def fullShader(self):
        return self.prefix + self.ui.textEdit_2.toPlainText() + self.suffix

    def compileShader(self):
        self.log = self.ui.openGLWidget.compileShader(self.fullShader())
        self.ui.textEdit.setPlainText(self.log)

    def save(self):
        print("saved.")
        if self.filename == "Untitled GFX":
            self.filename = str(QFileDialog.getSaveFileName(self, "Save...", "~", "Fragment shaders (*.frag)")[0])
        
        if self.filename == "":
            return
        
        savetext = self.license_header.toString() + "\n\n"
        savetext += self.prefix
        savetext += self.ui.textEdit_2.toPlainText()
        savetext += "\n\n" + self.suffix
        
        try:
            with open(self.filename, "wt") as f:
                f.write(savetext)
                f.close()
        except:
            msg = QMessageBox(QMessageBox.Error, "Could not save file...", "Could not save file " + self.filename + ".", QMessageBox.Ok)
            result = msg.exec_()
            return

    def saveAs(self):
        self.filename = str(QFileDialog.getSaveFileName(self, "Save...", "", "Fragment shaders (*.frag)")[0])
        
        if self.filename == "":
            return
        
        self.parent.ui.tabWidget.setTabText(self.parent.ui.tabWidget.currentIndex(), self.filename)

        self.save()
        
    def preferences(self):
        return

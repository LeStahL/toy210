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

class SyntaxHighlighter(QSyntaxHighlighter) :
    type_ids = [ 'vec2', 'vec3', 'int', 'vec4', 'mat2', 'mat3', 'mat4', 'void', 'float' ]
    flow_ids = [ 'in', 'out', 'uniform', 'const' ]
    syntax_ids = [ 'for', 'if', 'while', 'struct', 'return', 'else', 'break', 'continue' ]
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

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

from PyQt5.QtWidgets import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from SyntaxHighlighter import *
from UndoInsertText import *
from UndoRemoveText import *

class GLSLEditorWidget(QTextEdit):
    def __init__(self, parent):
        super(GLSLEditorWidget, self).__init__()
        
        self.setParent(parent)
        
        self.undostack = QUndoStack(self)
        self.highlighter = SyntaxHighlighter(self.document())
        
        self.nindent = 4
        self.notabs = True
        
    def insertFromMimeData(self, source):
        if source.hasText() :
            self.undostack.push(UndoInsertText(self, self.textCursor(), source.text()))
            
    def keyPressEvent(self, e):
        noinsert_keys = [ Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down, Qt.Key_End, Qt.Key_Home, Qt.Key_PageDown, Qt.Key_PageUp, Qt.Key_Backspace, Qt.Key_Delete ]
        if e.modifiers() == Qt.NoModifier and not e.key() in noinsert_keys:
                self.undostack.push(UndoInsertText(self, self.textCursor(), e.text()))
                return
        
        mode = QTextCursor.MoveAnchor
        if e.modifiers() & Qt.ShiftModifier:
            mode = QTextCursor.KeepAnchor
            
        if e.key() in [ Qt.Key_Backspace, Qt.Key_Delete ]:
            cursor = self.textCursor()
            if not cursor.hasSelection():
                cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, 1)
            self.undostack.push(UndoRemoveText(self, cursor))
            return 
        elif e.key() == Qt.Key_Left: 
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Left, mode, 1)
            self.setTextCursor(cursor)
        elif e.key() == Qt.Key_Right: 
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Right, mode, 1)
            self.setTextCursor(cursor)
        elif e.key() == Qt.Key_Up:
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Up, mode, 1)
            self.setTextCursor(cursor)
        elif e.key() == Qt.Key_Down: 
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.Down, mode, 1)
            self.setTextCursor(cursor)
            
        if e.modifiers() & Qt.ControlModifier:
            super(GLSLEditorWidget, self).keyPressEvent(e)
        
    def undo(self):
        if self.undostack.canUndo():
            self.undostack.undo()

    def redo(self):
        if self.undostack.canRedo():
            self.undostack.redo()
            

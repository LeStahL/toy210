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

class UndoRemoveText(QUndoCommand):
    def __init__(self, parent, text_cursor):
        super(UndoRemoveText, self).__init__()
        
        self.parent = parent
        self.cursor = text_cursor
        self.selected_text = self.cursor.selectedText()
        
    def redo(self):
        self.cursor.beginEditBlock()
        
        self.cursor.removeSelectedText()
        self.cursor.clearSelection()
        
        self.cursor.endEditBlock()
        
    def undo(self):
        self.cursor.beginEditBlock()
        
        self.cursor.insertText(self.selected_text)
        self.cursor.movePosition(QTextCursor.Left, QTextCursor.KeepAnchor, self.selected_text.size())
        
        self.cursor.endEditBlock()
        
        self.parent.setTextCursor(self.cursor)

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GFXPage.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_gfxPage(object):
    def setupUi(self, gfxPage):
        gfxPage.setObjectName("gfxPage")
        gfxPage.resize(609, 442)
        self.verticalLayout = QtWidgets.QVBoxLayout(gfxPage)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter_2 = QtWidgets.QSplitter(gfxPage)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.openGLWidget = glWidget(self.splitter)
        self.openGLWidget.setObjectName("openGLWidget")
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = GLSLEditorWidget(self.splitter_2)
        self.textEdit_2.setObjectName("textEdit_2")
        self.verticalLayout.addWidget(self.splitter_2)

        self.retranslateUi(gfxPage)
        QtCore.QMetaObject.connectSlotsByName(gfxPage)

    def retranslateUi(self, gfxPage):
        _translate = QtCore.QCoreApplication.translate
        gfxPage.setWindowTitle(_translate("gfxPage", "Form"))

from GLSLEditorWidget import GLSLEditorWidget
from GLWidget import glWidget

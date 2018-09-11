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
        self.verticalLayoutWidget = QtWidgets.QWidget(gfxPage)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(40, 60, 160, 122))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gfxWidget = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.gfxWidget.setObjectName("gfxWidget")
        self.verticalLayout.addWidget(self.gfxWidget)
        self.textEdit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayoutWidget = QtWidgets.QWidget(gfxPage)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(300, 220, 160, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.toolButton = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.toolButton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.toolButton)

        self.retranslateUi(gfxPage)
        QtCore.QMetaObject.connectSlotsByName(gfxPage)

    def retranslateUi(self, gfxPage):
        _translate = QtCore.QCoreApplication.translate
        gfxPage.setWindowTitle(_translate("gfxPage", "Form"))
        self.label.setText(_translate("gfxPage", "0:00:000"))
        self.toolButton.setText(_translate("gfxPage", "..."))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\IrradianceInterpolationDatafileRequirementsGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 271)
        Dialog.setMinimumSize(QtCore.QSize(511, 271))
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setMinimumSize(QtCore.QSize(75, 23))
        self.pushButton.setMaximumSize(QtCore.QSize(75, 23))
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 1, 1, 1)
        self.label_empty = QtWidgets.QLabel(Dialog)
        self.label_empty.setMinimumSize(QtCore.QSize(100, 0))
        self.label_empty.setText("")
        self.label_empty.setObjectName("label_empty")
        self.gridLayout.addWidget(self.label_empty, 1, 0, 1, 1)
        self.label_text = QtWidgets.QLabel(Dialog)
        self.label_text.setMinimumSize(QtCore.QSize(350, 160))
        self.label_text.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_text.setWordWrap(True)
        self.label_text.setObjectName("label_text")
        self.gridLayout.addWidget(self.label_text, 0, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "NIST Irradiance Interpolation - Datafile Requirements"))
        self.pushButton.setText(_translate("Dialog", "Close"))
        self.label_text.setText(_translate("Dialog", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600;\">Datafile requirements</span></p><p align=\"justify\">The datafile can be CSV, tab- or space-delimited. All types can be with or without a header. The first column must contain wavelengths with units nanometers, and the second column must contain irradiances with units W/cm<span style=\" vertical-align:super;\">3</span> or W/cm<span style=\" vertical-align:super;\">2</span> cm.</p><p align=\"justify\">No text can appear underneath the data rows--the program only strips header.</p></body></html>"))


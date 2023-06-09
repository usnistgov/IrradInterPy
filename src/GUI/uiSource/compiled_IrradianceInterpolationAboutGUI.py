# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\IrradianceInterpolationAboutGUI.ui'
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
        Dialog.setWindowTitle(_translate("Dialog", "NIST Irradiance Interpolation - About IrradInterPy"))
        self.pushButton.setText(_translate("Dialog", "Close"))
        self.label_text.setText(_translate("Dialog", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600;\">About</span></p><p align=\"justify\">This program was developed by the National Institute of Standards and Technology (NIST) to determine coefficients used in the gray body model for spectral irradiance and interpolate measurement data either using the gray body model or cubic spline interpolation.</p><p align=\"justify\">The source code for this program, including documentation, is located at <a href=\"https://github.com/usnistgov/IrradInterPy\"><span style=\" text-decoration: underline; color:#0000ff;\">https://github.com/usnistgov/IrradInterPy</span></a>.</p><p align=\"justify\">To get help or suggest feedback, send an email to <a href=\"mailto:michael.braine@nist.gov\"><span style=\" text-decoration: underline; color:#0000ff;\">michael.braine@nist.gov</span></a>.</p></body></html>"))


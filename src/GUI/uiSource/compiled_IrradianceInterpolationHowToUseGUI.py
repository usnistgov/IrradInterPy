# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\IrradianceInterpolationHowToUseGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(511, 338)
        Dialog.setMinimumSize(QtCore.QSize(511, 338))
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
        Dialog.setWindowTitle(_translate("Dialog", "NIST Irradiance Interpolation - How to Use"))
        self.pushButton.setText(_translate("Dialog", "Close"))
        self.label_text.setText(_translate("Dialog", "<html><head/><body><p align=\"justify\"><span style=\" font-weight:600;\">How to use this program</span></p><p align=\"justify\">1) Load the datafile with &quot;File&quot; &gt; &quot;Open datafile&quot;. See &quot;Help&quot; &gt; &quot;Input datafile requirements&quot; for expectations on the input datafile.</p><p align=\"justify\">2) Use the dropdown menus under the &quot;Gray body fit parameters&quot; group box to select the lower and upper wavelength bounds to apply the fit over. These values are pulled from the datafile. Use the &quot;Fit degrees of freedom&quot; to set degrees of freedom of the applied fit.</p><p align=\"justify\">3) Use the dropdown menus under &quot;Gray body interpolation parameters&quot; group box to select the region to calculate interpolated irradiances using the applied fit. Enter the wavelength step of the interpolation.</p><p align=\"justify\">4) Under the &quot;Results&quot; group box, the coefficients and interpolation results are displayed in their own tables.</p><p align=\"justify\">5) At the bottom of the main window (titled &quot;NIST Irradiance Interpolation&quot;), the &quot;Write results to file&quot; button will export the fit coefficients and interpolated data to a CSV file. By default, a filename is based on the original data filename with the date and time of the interpolation appended. The filename can be customized in the save dialog window.</p></body></html>"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\IrradianceInterpolationMainGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1169, 705)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1169, 705))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QtCore.QSize(468, 400))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButton_GBEvaluate = QtWidgets.QPushButton(self.tab)
        self.pushButton_GBEvaluate.setEnabled(False)
        self.pushButton_GBEvaluate.setObjectName("pushButton_GBEvaluate")
        self.gridLayout_3.addWidget(self.pushButton_GBEvaluate, 3, 0, 1, 1)
        self.groupBox_GBinterpolation = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_GBinterpolation.sizePolicy().hasHeightForWidth())
        self.groupBox_GBinterpolation.setSizePolicy(sizePolicy)
        self.groupBox_GBinterpolation.setMinimumSize(QtCore.QSize(449, 110))
        self.groupBox_GBinterpolation.setObjectName("groupBox_GBinterpolation")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBox_GBinterpolation)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 48))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.label_GBLowerWL = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_GBLowerWL.setMinimumSize(QtCore.QSize(120, 20))
        self.label_GBLowerWL.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBLowerWL.setObjectName("label_GBLowerWL")
        self.gridLayout.addWidget(self.label_GBLowerWL, 0, 0, 1, 1)
        self.combo_GBUpperWL = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combo_GBUpperWL.setEnabled(False)
        self.combo_GBUpperWL.setMinimumSize(QtCore.QSize(120, 20))
        self.combo_GBUpperWL.setObjectName("combo_GBUpperWL")
        self.gridLayout.addWidget(self.combo_GBUpperWL, 1, 1, 1, 1)
        self.label_GBstep = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_GBstep.setMinimumSize(QtCore.QSize(140, 20))
        self.label_GBstep.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBstep.setObjectName("label_GBstep")
        self.gridLayout.addWidget(self.label_GBstep, 0, 2, 1, 1)
        self.lineEdit_GBStep = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit_GBStep.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_GBStep.sizePolicy().hasHeightForWidth())
        self.lineEdit_GBStep.setSizePolicy(sizePolicy)
        self.lineEdit_GBStep.setMinimumSize(QtCore.QSize(140, 20))
        self.lineEdit_GBStep.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_GBStep.setObjectName("lineEdit_GBStep")
        self.gridLayout.addWidget(self.lineEdit_GBStep, 1, 2, 1, 1)
        self.combo_GBLowerWL = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.combo_GBLowerWL.setEnabled(False)
        self.combo_GBLowerWL.setMinimumSize(QtCore.QSize(120, 20))
        self.combo_GBLowerWL.setObjectName("combo_GBLowerWL")
        self.gridLayout.addWidget(self.combo_GBLowerWL, 1, 0, 1, 1)
        self.label_GBUpperWL = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_GBUpperWL.setMinimumSize(QtCore.QSize(120, 20))
        self.label_GBUpperWL.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBUpperWL.setObjectName("label_GBUpperWL")
        self.gridLayout.addWidget(self.label_GBUpperWL, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_GBinterpolation)
        self.label.setGeometry(QtCore.QRect(10, 70, 401, 31))
        self.label.setMinimumSize(QtCore.QSize(401, 0))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.groupBox_GBinterpolation, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(449, 80))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.groupBox)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 401, 48))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_GBfit = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_GBfit.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_GBfit.setHorizontalSpacing(6)
        self.gridLayout_GBfit.setObjectName("gridLayout_GBfit")
        self.combo_GBLowerWLFit = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.combo_GBLowerWLFit.setEnabled(False)
        self.combo_GBLowerWLFit.setMinimumSize(QtCore.QSize(120, 20))
        self.combo_GBLowerWLFit.setObjectName("combo_GBLowerWLFit")
        self.gridLayout_GBfit.addWidget(self.combo_GBLowerWLFit, 1, 0, 1, 1)
        self.label_GBLowerWLFit = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_GBLowerWLFit.setMinimumSize(QtCore.QSize(120, 20))
        self.label_GBLowerWLFit.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBLowerWLFit.setObjectName("label_GBLowerWLFit")
        self.gridLayout_GBfit.addWidget(self.label_GBLowerWLFit, 0, 0, 1, 1)
        self.label_GBdof = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_GBdof.setMinimumSize(QtCore.QSize(140, 20))
        self.label_GBdof.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBdof.setObjectName("label_GBdof")
        self.gridLayout_GBfit.addWidget(self.label_GBdof, 0, 2, 1, 1)
        self.label_GBUpperWLFit = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.label_GBUpperWLFit.setMinimumSize(QtCore.QSize(120, 20))
        self.label_GBUpperWLFit.setAlignment(QtCore.Qt.AlignCenter)
        self.label_GBUpperWLFit.setObjectName("label_GBUpperWLFit")
        self.gridLayout_GBfit.addWidget(self.label_GBUpperWLFit, 0, 1, 1, 1)
        self.combo_GBUpperWLFit = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.combo_GBUpperWLFit.setEnabled(False)
        self.combo_GBUpperWLFit.setMinimumSize(QtCore.QSize(120, 20))
        self.combo_GBUpperWLFit.setObjectName("combo_GBUpperWLFit")
        self.gridLayout_GBfit.addWidget(self.combo_GBUpperWLFit, 1, 1, 1, 1)
        self.combo_GBdof = QtWidgets.QComboBox(self.gridLayoutWidget_3)
        self.combo_GBdof.setEnabled(False)
        self.combo_GBdof.setObjectName("combo_GBdof")
        self.gridLayout_GBfit.addWidget(self.combo_GBdof, 1, 2, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_GBResults = QtWidgets.QGroupBox(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_GBResults.sizePolicy().hasHeightForWidth())
        self.groupBox_GBResults.setSizePolicy(sizePolicy)
        self.groupBox_GBResults.setObjectName("groupBox_GBResults")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_GBResults)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_GBcoefficients = QtWidgets.QLabel(self.groupBox_GBResults)
        self.label_GBcoefficients.setObjectName("label_GBcoefficients")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_GBcoefficients)
        self.tableWidget_GBCoefficients = QtWidgets.QTableWidget(self.groupBox_GBResults)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget_GBCoefficients.sizePolicy().hasHeightForWidth())
        self.tableWidget_GBCoefficients.setSizePolicy(sizePolicy)
        self.tableWidget_GBCoefficients.setAlternatingRowColors(True)
        self.tableWidget_GBCoefficients.setColumnCount(3)
        self.tableWidget_GBCoefficients.setObjectName("tableWidget_GBCoefficients")
        self.tableWidget_GBCoefficients.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_GBCoefficients.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_GBCoefficients.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_GBCoefficients.setHorizontalHeaderItem(2, item)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.tableWidget_GBCoefficients)
        self.label_GBinterpolation = QtWidgets.QLabel(self.groupBox_GBResults)
        self.label_GBinterpolation.setObjectName("label_GBinterpolation")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_GBinterpolation)
        self.tableWidget_GBInterpolation = QtWidgets.QTableWidget(self.groupBox_GBResults)
        self.tableWidget_GBInterpolation.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tableWidget_GBInterpolation.sizePolicy().hasHeightForWidth())
        self.tableWidget_GBInterpolation.setSizePolicy(sizePolicy)
        self.tableWidget_GBInterpolation.setAlternatingRowColors(True)
        self.tableWidget_GBInterpolation.setColumnCount(2)
        self.tableWidget_GBInterpolation.setObjectName("tableWidget_GBInterpolation")
        self.tableWidget_GBInterpolation.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_GBInterpolation.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_GBInterpolation.setHorizontalHeaderItem(1, item)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.SpanningRole, self.tableWidget_GBInterpolation)
        spacerItem = QtWidgets.QSpacerItem(40, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(3, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label_fitModel = QtWidgets.QLabel(self.groupBox_GBResults)
        self.label_fitModel.setObjectName("label_fitModel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_fitModel)
        self.gridLayout_7.addLayout(self.formLayout, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_GBResults, 2, 0, 1, 1)
        self.GBChart = QtWidgets.QWidget(self.tab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.GBChart.sizePolicy().hasHeightForWidth())
        self.GBChart.setSizePolicy(sizePolicy)
        self.GBChart.setMinimumSize(QtCore.QSize(525, 400))
        self.GBChart.setObjectName("GBChart")
        self.gridLayout_3.addWidget(self.GBChart, 0, 1, 4, 1)
        self.gridLayout_5.addLayout(self.gridLayout_3, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1169, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionOpen_datafile = QtWidgets.QAction(MainWindow)
        self.actionOpen_datafile.setObjectName("actionOpen_datafile")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionDatafileRequirements = QtWidgets.QAction(MainWindow)
        self.actionDatafileRequirements.setObjectName("actionDatafileRequirements")
        self.actionHowToUse = QtWidgets.QAction(MainWindow)
        self.actionHowToUse.setObjectName("actionHowToUse")
        self.menuFile.addAction(self.actionOpen_datafile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionHowToUse)
        self.menuHelp.addAction(self.actionDatafileRequirements)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.combo_GBLowerWLFit)
        MainWindow.setTabOrder(self.combo_GBLowerWLFit, self.combo_GBUpperWLFit)
        MainWindow.setTabOrder(self.combo_GBUpperWLFit, self.combo_GBLowerWL)
        MainWindow.setTabOrder(self.combo_GBLowerWL, self.combo_GBUpperWL)
        MainWindow.setTabOrder(self.combo_GBUpperWL, self.lineEdit_GBStep)
        MainWindow.setTabOrder(self.lineEdit_GBStep, self.pushButton_GBEvaluate)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "NIST Irradiance Interpolation (IrradInterPy)"))
        self.pushButton_GBEvaluate.setText(_translate("MainWindow", "Write interpolation to file"))
        self.groupBox_GBinterpolation.setTitle(_translate("MainWindow", "Interpolation parameters"))
        self.label_GBLowerWL.setText(_translate("MainWindow", "Lower wavelength"))
        self.label_GBstep.setText(_translate("MainWindow", "Interpolation step (nm)"))
        self.lineEdit_GBStep.setText(_translate("MainWindow", "10"))
        self.label_GBUpperWL.setText(_translate("MainWindow", "Upper wavelength"))
        self.label.setText(_translate("MainWindow", "Note: This region must be contained entirely within the region defined in the fit parameters, this program does not extrapolate."))
        self.groupBox.setTitle(_translate("MainWindow", "Fit parameters"))
        self.label_GBLowerWLFit.setText(_translate("MainWindow", "Lower wavelength"))
        self.label_GBdof.setText(_translate("MainWindow", "Fit degrees of freedom"))
        self.label_GBUpperWLFit.setText(_translate("MainWindow", "Upper wavelength"))
        self.groupBox_GBResults.setTitle(_translate("MainWindow", "Results"))
        self.label_GBcoefficients.setText(_translate("MainWindow", "Fit model coefficients"))
        item = self.tableWidget_GBCoefficients.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Coefficient"))
        item = self.tableWidget_GBCoefficients.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidget_GBCoefficients.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Uncertainty"))
        self.label_GBinterpolation.setText(_translate("MainWindow", "Fit interpolation"))
        item = self.tableWidget_GBInterpolation.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Wavelength (nm)"))
        item = self.tableWidget_GBInterpolation.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Irradiance (W/cm^3)"))
        self.label_fitModel.setText(_translate("MainWindow", "<html><head/><body><p>Irradiance from fit model:<span style=\" font-size:10pt;\"> E</span><span style=\" font-size:10pt; vertical-align:sub;\">λ</span><span style=\" font-size:10pt;\"> = (A</span><span style=\" font-size:10pt; vertical-align:sub;\">0</span><span style=\" font-size:10pt;\"> + A</span><span style=\" font-size:10pt; vertical-align:sub;\">1</span><span style=\" font-size:10pt;\">λ + A</span><span style=\" font-size:10pt; vertical-align:sub;\">2</span><span style=\" font-size:10pt;\">λ</span><span style=\" font-size:10pt; vertical-align:super;\">2</span><span style=\" font-size:10pt;\"> + ... + A</span><span style=\" font-size:10pt; vertical-align:sub;\">n</span><span style=\" font-size:10pt;\">λ</span><span style=\" font-size:10pt; vertical-align:super;\">n</span><span style=\" font-size:10pt;\">) λ</span><span style=\" font-size:10pt; vertical-align:super;\">-5</span><span style=\" font-size:10pt;\"> e</span><span style=\" font-size:10pt; vertical-align:super;\">a + b/λ</span></p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Gray Body Model"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen_datafile.setText(_translate("MainWindow", "Open datafile ..."))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionDatafileRequirements.setText(_translate("MainWindow", "Input datafile requirements"))
        self.actionHowToUse.setText(_translate("MainWindow", "How to use"))

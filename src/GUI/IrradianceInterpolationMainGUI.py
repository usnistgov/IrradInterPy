import os
import sys
from pathlib import Path
from datetime import datetime
import subprocess
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
from PyQt5 import QtWidgets, QtCore, QtGui
from GUI.uiSource import compiled_IrradianceInterpolationMainGUI
from GUI.uiSource import compiled_IrradianceInterpolationAboutGUI
from GUI.uiSource import compiled_IrradianceInterpolationDatafileRequirementsGUI
from GUI.uiSource import compiled_IrradianceInterpolationHowToUseGUI
from Functions import IrradianceInterpolationFuncs as IIF
from var import GUIvar
from var import version

class Window_IrradianceInterpolationMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = compiled_IrradianceInterpolationMainGUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.closeEvent = self.Clicked_QUIT

        # initial setup
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        iconPath = scriptDir + os.path.sep + "\..\\icon_64.png"
        self.setWindowIcon(QtGui.QIcon(iconPath))
        self.statusBar_version = QtWidgets.QLabel()
        self.statusBar_version.setText("IrradInterPy " + version.version + " (" + version.versionDate+")")
        self.ui.statusBar.addPermanentWidget(self.statusBar_version)
        self.ui.lineEdit_GBStep.setText(str(GUIvar.defaultGBInterpStep))
        self.ui.combo_GBdof.clear()
        for dof in GUIvar.GBfitdof:
            self.ui.combo_GBdof.addItem(str(dof))
        self.ui.combo_GBdof.setCurrentIndex(GUIvar.defaultGBdofIndex)
        self.ui.tableWidget_GBCoefficients.resizeColumnsToContents()
        self.ui.tableWidget_GBInterpolation.resizeColumnsToContents()
        self.GBcoeffTableHeaders = ["Coefficient", "Value", "Uncertainty (k=1)"]
        self.GBinterpTableHeaders = ["Wavelength (nm)", "Interpolated Irradiance (W/cm^3)"]
        matplotlib.rcParams.update({"figure.autolayout": True})

        # variable initialization
        self.InputFilename = ""
        self.wavelengths = []
        self.irradiances = []
        self.GBcoefficients = []
        self.GBuncertainty = []
        self.GBa = ""
        self.GBb = ""
        self.abUncertainty = ""
        self.GBBBtemperature = ""
        self.GBinterpWavelengths = []
        self.GBinterpIrradiances = []
        self.residuals = []
        self.GBinterpfile = ""
        if GUIvar.defaultDatafilePath == "":
            self.defaultDatafilePath = os.path.expanduser(os.getenv("USERPROFILE"))
        else:
            self.defaultDatafilePath = GUIvar.defaultDatafilePath

        # chart setups
        self.ui.GBChart.Figure = Figure()
        self.ui.GBChart.Canvas = FigureCanvas(self.ui.GBChart.Figure)
        chartlayout = QtWidgets.QVBoxLayout()
        chartlayout.addWidget(self.ui.GBChart.Canvas)
        self.ui.GBChart.setLayout(chartlayout)
        self.ResetGBChart()

        # attach additional windows
        self.ui.about = Window_About()
        self.ui.datafileRequirements = Window_DatafileRequirements()
        self.ui.howToUse = Window_HowToUse()

        self.IssuesMsgBox = QtWidgets.QMessageBox()
        self.IssuesMsgBox.setIcon(QtWidgets.QMessageBox.Critical)
        self.IssuesMsgBox.setWindowTitle("Interpolation cannot proceed")
        self.IssuesMsgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)

        self.EvalComplete = QtWidgets.QMessageBox()
        self.EvalComplete.setIcon(QtWidgets.QMessageBox.Information)
        self.EvalComplete.setWindowTitle("Interpolation complete!")
        self.EvalComplete.setStandardButtons(QtWidgets.QMessageBox.Ok)

        # connect widgets
        self.ui.actionOpen_datafile.triggered.connect(self.Clicked_OpenDatafile)
        self.ui.actionAbout.triggered.connect(self.ui.about.exec_)
        self.ui.actionDatafileRequirements.triggered.connect(self.ui.datafileRequirements.exec_)
        self.ui.actionHowToUse.triggered.connect(self.ui.howToUse.exec_)
        self.ui.pushButton_GBEvaluate.clicked.connect(self.Clicked_GBEvaluate)
        self.ConnectGBDropdowns()
        self.ui.combo_GBdof.currentIndexChanged.connect(self.ChangedGBEvaluation)
        self.ui.lineEdit_GBStep.textChanged.connect(self.ChangedGBEvaluation)
        self.ui.actionExit.triggered.connect(self.Clicked_QUIT)

    def ChangedGBEvaluation(self):
        if self.CheckGBInputs() == 0:
            self.GBEvaluate()
        else:
            self.ClearGBCoeffTable()
            self.ClearGBInterpTable()
            self.ResetGBChart()
            self.IssuesMsgBox.show()

    def ChangedGBLowerWLFit(self):
        try:
            if float(self.ui.combo_GBLowerWLFit.currentText()) > float(self.ui.combo_GBLowerWL.currentText()):
                self.ui.combo_GBLowerWL.setCurrentIndex(self.ui.combo_GBLowerWLFit.currentIndex())
            self.ChangedGBEvaluation()
        except Exception as err:
            raise err

    def ChangedGBLowerWL(self):
        try:
            if float(self.ui.combo_GBLowerWL.currentText()) < float(self.ui.combo_GBLowerWLFit.currentText()):
                self.ui.combo_GBLowerWLFit.setCurrentIndex(self.ui.combo_GBLowerWL.currentIndex())
            self.ChangedGBEvaluation()
        except Exception as err:
            raise err

    def ChangedGBUpperWLFit(self):
        try:
            if float(self.ui.combo_GBUpperWLFit.currentText()) < float(self.ui.combo_GBUpperWL.currentText()):
                self.ui.combo_GBUpperWL.setCurrentIndex(self.ui.combo_GBUpperWLFit.currentIndex())
            self.ChangedGBEvaluation()
        except Exception as err:
            raise err

    def ChangedGBUpperWL(self):
        try:
            if float(self.ui.combo_GBUpperWL.currentText()) > float(self.ui.combo_GBUpperWLFit.currentText()):
                self.ui.combo_GBUpperWLFit.setCurrentIndex(self.ui.combo_GBUpperWL.currentIndex())
            self.ChangedGBEvaluation()
        except Exception as err:
            raise err

    def DisconnectGBDropdowns(self):
        self.ui.combo_GBLowerWLFit.currentIndexChanged.disconnect(self.ChangedGBLowerWLFit)
        self.ui.combo_GBUpperWLFit.currentIndexChanged.disconnect(self.ChangedGBUpperWLFit)
        self.ui.combo_GBLowerWL.currentIndexChanged.disconnect(self.ChangedGBLowerWL)
        self.ui.combo_GBUpperWL.currentIndexChanged.disconnect(self.ChangedGBUpperWL)

    def ConnectGBDropdowns(self):
        self.ui.combo_GBLowerWLFit.currentIndexChanged.connect(self.ChangedGBLowerWLFit)
        self.ui.combo_GBUpperWLFit.currentIndexChanged.connect(self.ChangedGBUpperWLFit)
        self.ui.combo_GBLowerWL.currentIndexChanged.connect(self.ChangedGBLowerWL)
        self.ui.combo_GBUpperWL.currentIndexChanged.connect(self.ChangedGBUpperWL)

    def Clicked_OpenDatafile(self):
        try:
            tempstr, _ = QtWidgets.QFileDialog.getOpenFileName(directory=self.defaultDatafilePath)
            if tempstr != "":
                self.InputFilename = Path(tempstr)
                self.wavelengths, self.irradiances = IIF.ParseDatafile(self.InputFilename)
                self.DisconnectGBDropdowns()
                self.PopulateWLBoundCombos()
                self.ui.combo_GBLowerWLFit.setCurrentIndex(0)
                self.ui.combo_GBLowerWL.setCurrentIndex(0)
                self.ui.combo_GBUpperWL.setCurrentIndex(self.ui.combo_GBUpperWL.count()-1)
                self.ui.combo_GBUpperWLFit.setCurrentIndex(self.ui.combo_GBUpperWLFit.count()-1)
                self.ConnectGBDropdowns()
                self.ToggleGBGUI(True)
                if self.CheckGBInputs() == 0:
                    self.GBEvaluate()
            else:
                self.InputFilename = ""
                self.DisconnectGBDropdowns()
                self.ClearWLBoundCombos()
                self.ToggleGBGUI(False)
                self.ConnectGBDropdowns()
                self.ResetGBChart()
                self.ClearGBCoeffTable()
                self.ClearGBInterpTable()
        except Exception as err:
            raise err

    def ToggleGBGUI(self, state):
        self.ui.combo_GBLowerWL.setEnabled(state)
        self.ui.combo_GBUpperWL.setEnabled(state)
        self.ui.combo_GBdof.setEnabled(state)
        self.ui.lineEdit_GBStep.setEnabled(state)
        self.ui.pushButton_GBEvaluate.setEnabled(state)
        self.ui.combo_GBLowerWLFit.setEnabled(state)
        self.ui.combo_GBUpperWLFit.setEnabled(state)

    def ClearWLBoundCombos(self):
        try:
            self.ui.combo_GBLowerWL.clear()
            self.ui.combo_GBUpperWL.clear()
            self.ui.combo_GBLowerWLFit.clear()
            self.ui.combo_GBUpperWLFit.clear()
        except Exception as err:
            raise err

    def PopulateWLBoundCombos(self):
        try:
            for wavelength in self.wavelengths:
                self.ui.combo_GBLowerWLFit.addItem(str(wavelength))
                self.ui.combo_GBUpperWLFit.addItem(str(wavelength))
                self.ui.combo_GBLowerWL.addItem(str(wavelength))
                self.ui.combo_GBUpperWL.addItem(str(wavelength))
        except Exception as err:
            raise err

    def ClearGBCoeffTable(self):
        try:
            self.ui.tableWidget_GBCoefficients.clear()
            self.ui.tableWidget_GBCoefficients.setHorizontalHeaderLabels(self.GBcoeffTableHeaders)
            self.ui.tableWidget_GBCoefficients.resizeColumnsToContents()
        except Exception as err:
            raise err

    def ClearGBInterpTable(self):
        try:
            self.ui.tableWidget_GBInterpolation.clear()
            self.ui.tableWidget_GBInterpolation.setHorizontalHeaderLabels(self.GBinterpTableHeaders)
            self.ui.tableWidget_GBInterpolation.resizeColumnsToContents()
        except Exception as err:
            raise err

    def PopulateGBCoeffTable(self):
        try:
            self.ClearGBCoeffTable()
            self.ui.tableWidget_GBCoefficients.setRowCount(len(self.GBcoefficients)+2)
            self.ui.tableWidget_GBCoefficients.setColumnCount(3)
            self.ui.tableWidget_GBCoefficients.setHorizontalHeaderLabels(self.GBcoeffTableHeaders)
            for row, (val, U) in enumerate(zip(self.GBcoefficients, self.GBuncertainty)):
                coeffLabelItem = QtWidgets.QTableWidgetItem("A_%d" % (row))
                coeffLabelItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                coeffLabelItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_GBCoefficients.setItem(row, 0, coeffLabelItem)

                coeffValueItem = QtWidgets.QTableWidgetItem("%.12e" % (val))
                coeffValueItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                coeffValueItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_GBCoefficients.setItem(row, 1, coeffValueItem)

                coeffUncItem = QtWidgets.QTableWidgetItem("%.12e" % (U))
                coeffUncItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                coeffUncItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_GBCoefficients.setItem(row, 2, coeffUncItem)
            coeffaLabelItem = QtWidgets.QTableWidgetItem("a")
            coeffaLabelItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffaLabelItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+1, 0, coeffaLabelItem)

            coeffaItem = QtWidgets.QTableWidgetItem("%.12e" % (self.GBa))
            coeffaItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffaItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+1, 1, coeffaItem)

            coeffaUItem = QtWidgets.QTableWidgetItem("%.12e" % (self.abUncertainty[0]))
            coeffaUItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffaUItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+1, 2, coeffaUItem)

            coeffbLabelItem = QtWidgets.QTableWidgetItem("b")
            coeffbLabelItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffbLabelItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+2, 0, coeffbLabelItem)

            coeffbItem = QtWidgets.QTableWidgetItem("%.12e" % (self.GBb))
            coeffbItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffbItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+2, 1, coeffbItem)

            coeffbUItem = QtWidgets.QTableWidgetItem("%.12e" % (self.abUncertainty[1]))
            coeffbUItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            coeffbUItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            self.ui.tableWidget_GBCoefficients.setItem(row+2, 2, coeffbUItem)

            self.ui.tableWidget_GBCoefficients.resizeColumnsToContents()
        except Exception as err:
            raise err

    def PopulateGBInterpTable(self):
        try:
            self.ClearGBInterpTable()
            self.ui.tableWidget_GBInterpolation.setRowCount(len(self.GBinterpWavelengths))
            self.ui.tableWidget_GBInterpolation.setColumnCount(2)
            self.ui.tableWidget_GBInterpolation.setHorizontalHeaderLabels(self.GBinterpTableHeaders)
            for row, (wavelength, irradiance) in enumerate(zip(self.GBinterpWavelengths, self.GBinterpIrradiances)):
                interpWLItem = QtWidgets.QTableWidgetItem("%.2f" % (wavelength))
                interpWLItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                interpWLItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_GBInterpolation.setItem(row, 0, interpWLItem)

                InterpIrItem = QtWidgets.QTableWidgetItem("%.6e" % (irradiance))
                InterpIrItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                InterpIrItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_GBInterpolation.setItem(row, 1, InterpIrItem)
            self.ui.tableWidget_GBInterpolation.resizeColumnsToContents()
        except Exception as err:
            raise err

    def Clicked_GBEvaluate(self):
        try:
            fileTimeStr = "%d-%d-%d_%d-%d-%d" % (
                datetime.today().day,
                datetime.today().month,
                datetime.today().year,
                datetime.today().hour,
                datetime.today().minute,
                datetime.today().second,
            )
            self.GBinterpfile = ".".join(str(self.InputFilename).split(".")[:-1]) + "-Gray_Body_Interpolation-%s.csv" % (fileTimeStr)
            nIssues = self.CheckGBInputs()
            if nIssues != 0:
                self.ClearGBCoeffTable()
                self.ClearGBInterpTable()
                self.ResetGBChart()
                self.IssuesMsgBox.show()
            else:
                self.GBinterpfile, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Write gray body interpolation to file", self.GBinterpfile, filter="CSV (*.csv)")
                if self.GBinterpfile == "":
                    self.IssuesMsgBox.setText(self.IssuesMsgBox.text() + "  - Write to file cancelled. Results not yet saved!")
                    self.IssuesMsgBox.show()
                else:
                    if self.CheckGBOutputFileExists() == 0:
                        self.GBEvaluate()
                        self.WriteGBInterpolationToFile()
                    else:
                        self.IssuesMsgBox.show()
        except Exception as err:
            raise err

    def GBEvaluate(self):
        self.GBcoefficients, self.GBuncertainty, self.GBinterpWavelengths, self.GBinterpIrradiances = [], [], [], []
        self.GBa, self.GBb, self.GBBBtemperature, self.abUncertainty = "", "", "", ""
        self.GBcoefficients, self.GBuncertainty, self.GBa, self.GBb, self.abUncertainty = IIF.GrayBodyCoefficients(
            self.wavelengths,
            self.irradiances,
            (float(self.ui.combo_GBLowerWLFit.currentText()), float(self.ui.combo_GBUpperWLFit.currentText())),
            int(self.ui.combo_GBdof.currentText()),
        )
        self.GBinterpWavelengths, self.GBinterpIrradiances = IIF.GrayBodyInterpolation(
            (float(self.ui.combo_GBLowerWL.currentText()), float(self.ui.combo_GBUpperWL.currentText())),
            self.GBcoefficients,
            self.GBa,
            self.GBb,
            float(self.ui.lineEdit_GBStep.text()),
        )
        self.GBBBtemperature = IIF.ApparentBBTemp(self.GBinterpWavelengths, self.GBinterpIrradiances)
        self.PopulateGBCoeffTable()
        self.PopulateGBInterpTable()
        self.UpdateGBChart()

    def CheckGBInputs(self):
        try:
            nIssues = 0
            errMsg = "The following issues need corrected:\n"
            # check if lower wavelength is smaller than upper wavelength for interpolation parameters
            if float(self.ui.combo_GBLowerWLFit.currentText()) >= float(self.ui.combo_GBUpperWLFit.currentText()):
                errMsg = errMsg + "  - the lower wavelength must be less than the upper wavelength in gray body fit parameters\n"
                nIssues += 1

            # check if lower wavelength is smaller than upper wavelength for GB fit parameters
            if float(self.ui.combo_GBLowerWL.currentText()) >= float(self.ui.combo_GBUpperWL.currentText()):
                errMsg = errMsg + "  - the lower wavelength must be less than the upper wavelength in gray body interpolation parameters\n"
                nIssues += 1

            # check if GB dof is integer
            try:
                int(self.ui.combo_GBdof.currentText())
                if int(self.ui.combo_GBdof.currentText()) - float(self.ui.combo_GBdof.currentText()) != 0:
                    errMsg = errMsg + "  - the gray body fit degrees of freedom must be an integer\n"
                    nIssues += 1
            except Exception as dofIntErr:
                if "invalid literal for int() with base 10" in str(dofIntErr):
                    errMsg = errMsg + "  - the gray body fit degrees of freedom must be an integer\n"
                    nIssues += 1
                else:
                    raise dofIntErr

            # check if GB step is float and greater than zero
            try:
                if float(self.ui.lineEdit_GBStep.text()) <= 0:
                    errMsg = errMsg + "  - the gray body interpolation step must be a float greater than zero\n"
                    nIssues += 1
            except Exception as dofIntErr:
                if "could not convert string to float" in str(dofIntErr):
                    errMsg = errMsg + "  - the gray body interpolation step must be a float greater than zero\n"
                    nIssues += 1
                else:
                    raise dofIntErr

            # check if GB step is float or integer
            try:
                int(self.ui.combo_GBdof.currentText())
            except Exception as dofIntErr:
                if "could not convert string to float" in str(dofIntErr):
                    errMsg = errMsg + "  - the gray body fit degrees of freedom must be a float\n"
                    nIssues += 1
                else:
                    raise dofIntErr
        except Exception as err:
            raise err
        self.IssuesMsgBox.setText(errMsg)
        return nIssues

    def CheckGBOutputFileExists(self):
        try:
            with open(self.GBinterpfile, "w") as openedfile:
                openedfile.write("")
                return 0
        except Exception as openFileErr:
            if "Permission denied" in str(openFileErr):
                errMsg = self.IssuesMsgBox.text() + "  - close the file %s to write evaluations to it.\n" % (self.GBinterpfile)
                self.IssuesMsgBox.setText(errMsg)
                return 1
            else:
                raise openFileErr

    def WriteGBInterpolationToFile(self):
        try:
            with open(self.GBinterpfile, "w") as openedfile:
                # program version number
                openedfile.write("This file was created with IrradInterPy " + version.version + " (" + version.versionDate.replace(",", "") + ")\n")
                openedfile.write("IrradInterPy is available on Github from the NIST group usnistgov: https://github.com/usnistgov/IrradInterPy\n\n")

                # coefficients
                openedfile.write("Gray body interpolation coefficients\n")
                openedfile.write("A_n, Coefficient, Uncertainty (k=1)\n")
                for i, (coefficient, uncertainty) in enumerate(zip(self.GBcoefficients, self.GBuncertainty)):
                    openedfile.write("A%d, %.20e, %.20e\n" % (i, coefficient, uncertainty))
                openedfile.write("a, %.20e, %.20e\n" % (self.GBa, self.abUncertainty[0]))
                openedfile.write("b, %.20e, %.20e\n" % (self.GBb, self.abUncertainty[1]))
                openedfile.write("\n")

                #openedfile.write("Peak wavelength = %.1f\n" % (IIF.PeakWavelength(self.GBinterpWavelengths, self.GBinterpIrradiances)))
                #openedfile.write("Apparent blackbody temperature = %.1f\n\n" % (self.GBBBtemperature))

                # interpolated data
                openedfile.write("Gray body interpolated data\n")
                openedfile.write("Interpolated wavelength, Interpolated irradiance\n")
                for i, (wavelength, irradiance) in enumerate(zip(self.GBinterpWavelengths, self.GBinterpIrradiances)):
                    openedfile.write("%.2f, %.6e\n" % (wavelength, irradiance))
                openedfile.write("\n")

                # measurement data used in interpolation
                openedfile.write("Measured data\n")
                openedfile.write("Wavelength, Irradiance, Fit residual (%)\n")
                j = 0
                for i, (wavelength, irradiance) in enumerate(zip(self.wavelengths, self.irradiances)):
                    openedfile.write("%.2f, %.6e," % (wavelength, irradiance))
                    if wavelength >= float(self.ui.combo_GBLowerWLFit.currentText()) and wavelength <= float(self.ui.combo_GBUpperWLFit.currentText()):
                        openedfile.write("%.4f" % self.residuals[j])
                        j += 1
                    else:
                        openedfile.write("-")
                    openedfile.write("\n")
                self.EvalComplete.setText("Interpolation complete! Results are stored at: %s" % (self.GBinterpfile))
                self.EvalComplete.show()
                subprocess.Popen(r"explorer /select,%s" % (Path(self.GBinterpfile)))
        except Exception as err:
            raise err

    def ResetGBChart(self):
        self.ui.GBChart.Figure.clear()
        self.ax_GBResiduals = self.ui.GBChart.Figure.add_subplot(2, 1, 2)
        self.ax_GBIrradiance = self.ui.GBChart.Figure.add_subplot(2, 1, 1, sharex=self.ax_GBResiduals)
        self.ax_GBIrradiance.measLine, = self.ax_GBIrradiance.plot([], [])
        self.ax_GBIrradiance.fitLine, = self.ax_GBIrradiance.plot([], [])
        self.ax_GBResiduals.line, = self.ax_GBResiduals.plot([], [])
        self.ax_GBIrradiance.set_ylabel(r"Irradiance ($\frac{W}{cm^{3}})$")
        # self.ax_GBIrradiance.set_xticklabels([])
        self.ax_GBIrradiance.grid()
        self.ax_GBResiduals.set_ylabel(r"Relative residual (%)")
        self.ax_GBResiduals.set_xlabel("Wavelength (nm)")
        self.ax_GBResiduals.grid()
        self.ui.GBChart.Figure.subplots_adjust(hspace=0.1, left=0.185, right=0.95, bottom=0.13, top=0.99)
        self.ui.GBChart.Canvas.draw()

    def UpdateGBChart(self):
        self.ResetGBChart()
        i_lowerBound, i_upperBound = IIF.WavelengthRegionIndex(
            self.wavelengths,
            (float(self.ui.combo_GBLowerWLFit.currentText()), float(self.ui.combo_GBUpperWLFit.currentText())),
        )
        self.residuals = (IIF.GrayBody(self.wavelengths[i_lowerBound:i_upperBound], self.GBa, self.GBb, self.GBcoefficients) - self.irradiances[i_lowerBound:i_upperBound])/self.irradiances[i_lowerBound:i_upperBound]*100
        self.ax_GBIrradiance.measLine, = self.ax_GBIrradiance.plot(
            self.wavelengths[i_lowerBound:i_upperBound],
            self.irradiances[i_lowerBound:i_upperBound],
            label="Measurements",
            marker=GUIvar.markerType,
            markersize=GUIvar.markerSize,
            markeredgecolor=GUIvar.markerEdgeColor,
            markerfacecolor=GUIvar.markerFaceColor,
            linestyle="None",
        )
        self.ax_GBIrradiance.fitLine, = self.ax_GBIrradiance.plot(
            self.GBinterpWavelengths,
            self.GBinterpIrradiances,
            label="Interpolated fit",
            color=GUIvar.fitLineColor,
            linewidth=GUIvar.fitLinewidth,
        )
        self.ax_GBIrradiance.set_ylabel(r"Irradiance ($\frac{W}{cm^{3}})$")
        self.ax_GBIrradiance.legend()

        self.ax_GBResiduals.line, = self.ax_GBResiduals.plot(
            self.wavelengths[i_lowerBound:i_upperBound],
            self.residuals,
            marker=GUIvar.markerType,
            markersize=GUIvar.markerSize,
            markeredgecolor=GUIvar.markerEdgeColor,
            markerfacecolor=GUIvar.markerFaceColor,
            linestyle="None",
        )
        self.ax_GBResiduals.set_ylabel(r"Relative residual (%)")

        self.ui.GBChart.Canvas.draw()

    def Clicked_QUIT(self):
        self.close()

class Window_About(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = compiled_IrradianceInterpolationAboutGUI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.Clicked_OK)

    def Clicked_OK(self):
        self.hide()

class Window_DatafileRequirements(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = compiled_IrradianceInterpolationDatafileRequirementsGUI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.Clicked_OK)

    def Clicked_OK(self):
        self.hide()

class Window_HowToUse(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = compiled_IrradianceInterpolationHowToUseGUI.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.Clicked_OK)

    def Clicked_OK(self):
        self.hide()
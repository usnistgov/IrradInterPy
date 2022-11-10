from pathlib import Path
from datetime import datetime
import subprocess
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets, QtCore
from GUI.uiSource import compiled_IrradianceInterpolationMainGUI
from GUI.uiSource import compiled_IrradianceInterpolationAboutGUI
from GUI.uiSource import compiled_IrradianceInterpolationDatafileRequirementsGUI
from GUI.uiSource import compiled_IrradianceInterpolationHowToUseGUI
import version
from Functions import IrradianceInterpolationFuncs as IIF
from var import GUIvar

class Window_IrradianceInterpolationMain(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = compiled_IrradianceInterpolationMainGUI.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.closeEvent = self.Clicked_QUIT

        # initial setup
        self.ui.statusBar.showMessage(version.version)
        self.ui.lineEdit_GBStep.setText(str(GUIvar.defaultGBInterpStep))
        self.ui.lineEdit_CSStep.setText(str(GUIvar.defaultCSInterpStep))
        self.ui.combo_GBdof.clear()
        for dof in GUIvar.GBfitdof:
            self.ui.combo_GBdof.addItem(str(dof))
        self.ui.combo_GBdof.setCurrentIndex(GUIvar.defaultGBdofIndex)
        self.ui.tableWidget_GBCoefficients.resizeColumnsToContents()
        self.ui.tableWidget_GBInterpolation.resizeColumnsToContents()
        self.ui.tableWidget_CSCoefficients.resizeColumnsToContents()
        self.ui.tableWidget_CSInterpolation.resizeColumnsToContents()
        self.GBcoeffTableHeaders = ["Coefficient", "Value", "Uncertainty (k=1)"]
        self.GBinterpTableHeaders = ["Wavelength (nm)", "Interpolated Irradiance (W/cm^3)"]
        self.CScoeffTableHeaders = ["i", "Segment", "a_i", "b_i", "c_i", "d_i"]
        self.CSinterpTableHeaders = ["Wavelength (nm)", "Interpolated Irradiance (W/cm^3)"]

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
        self.GBinterpfile = ""
        self.CSinterpWavelengths = []
        self.CSinterpIrradiances = []
        self.CScoefficients = []
        self.CSfit = ""
        self.CSinterpfile = ""

        # chart setups
        self.ui.GBChart.Figure = Figure()
        self.ui.GBChart.Canvas = FigureCanvas(self.ui.GBChart.Figure)
        chartlayout = QtWidgets.QVBoxLayout()
        chartlayout.addWidget(self.ui.GBChart.Canvas)
        self.ui.GBChart.setLayout(chartlayout)
        self.ResetGBChart()

        self.ui.CSChart.Figure = Figure()
        self.ui.CSChart.Canvas = FigureCanvas(self.ui.CSChart.Figure)
        chartlayout = QtWidgets.QVBoxLayout()
        chartlayout.addWidget(self.ui.CSChart.Canvas)
        self.ui.CSChart.setLayout(chartlayout)
        self.ResetCSChart()

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
        self.ui.pushButton_CSEvaluate.clicked.connect(self.Clicked_CSEvaluate)
        self.ConnectGBDropdowns()
        self.ConnectCSDropdowns()
        self.ui.combo_GBdof.currentIndexChanged.connect(self.ChangedGBEvaluation)
        self.ui.lineEdit_GBStep.textChanged.connect(self.ChangedGBEvaluation)
        self.ui.lineEdit_CSStep.textChanged.connect(self.ChangedCSEvaluation)
        self.ui.actionExit.triggered.connect(self.Clicked_QUIT)

    def ChangedGBEvaluation(self):
        if self.CheckGBInputs() == 0:
            self.GBEvaluate()
        else:
            self.ClearGBCoeffTable()
            self.ClearGBInterpTable()
            self.ResetGBChart()
            self.IssuesMsgBox.show()
            
    def ChangedCSEvaluation(self):
        if self.CheckCSInputs() == 0:
            self.CSEvaluate()
        else:
            self.ClearCSCoeffTable()
            self.ClearCSInterpTable()
            self.ResetCSChart()
            self.IssuesMsgBox.show()

    def DisconnectGBDropdowns(self):
        self.ui.combo_GBLowerWLFit.currentIndexChanged.disconnect(self.ChangedGBEvaluation)
        self.ui.combo_GBUpperWLFit.currentIndexChanged.disconnect(self.ChangedGBEvaluation)
        self.ui.combo_GBLowerWL.currentIndexChanged.disconnect(self.ChangedGBEvaluation)
        self.ui.combo_GBUpperWL.currentIndexChanged.disconnect(self.ChangedGBEvaluation)

    def ConnectGBDropdowns(self):
        self.ui.combo_GBLowerWLFit.currentIndexChanged.connect(self.ChangedGBEvaluation)
        self.ui.combo_GBUpperWLFit.currentIndexChanged.connect(self.ChangedGBEvaluation)
        self.ui.combo_GBLowerWL.currentIndexChanged.connect(self.ChangedGBEvaluation)
        self.ui.combo_GBUpperWL.currentIndexChanged.connect(self.ChangedGBEvaluation)

    def DisconnectCSDropdowns(self):
        self.ui.combo_CSLowerWL.currentIndexChanged.disconnect(self.ChangedCSEvaluation)
        self.ui.combo_CSUpperWL.currentIndexChanged.disconnect(self.ChangedCSEvaluation)

    def ConnectCSDropdowns(self):
        self.ui.combo_CSLowerWL.currentIndexChanged.connect(self.ChangedCSEvaluation)
        self.ui.combo_CSUpperWL.currentIndexChanged.connect(self.ChangedCSEvaluation)

    def Clicked_OpenDatafile(self):
        try:
            tempstr, _ = QtWidgets.QFileDialog.getOpenFileName()
            if tempstr != "":
                self.InputFilename = Path(tempstr)
                self.wavelengths, self.irradiances = IIF.ParseDatafile(self.InputFilename)
                self.DisconnectGBDropdowns()
                self.DisconnectCSDropdowns()
                self.PopulateWLBoundCombos()
                self.ui.combo_GBLowerWLFit.setCurrentIndex(0)
                self.ui.combo_GBLowerWL.setCurrentIndex(0)
                self.ui.combo_GBUpperWL.setCurrentIndex(self.ui.combo_GBUpperWL.count()-1)
                self.ui.combo_GBUpperWLFit.setCurrentIndex(self.ui.combo_GBUpperWLFit.count()-1)
                self.ui.combo_CSLowerWL.setCurrentIndex(0)
                self.ui.combo_CSUpperWL.setCurrentIndex(self.ui.combo_CSUpperWL.count()-1)
                self.ConnectGBDropdowns()
                self.ConnectCSDropdowns()
                self.ToggleGBGUI(True)
                self.ToggleCSGUI(True)
                if self.CheckGBInputs() == 0:
                    self.GBEvaluate()
                if self.CheckCSInputs() == 0:
                    self.CSEvaluate()
            else:
                self.InputFilename = ""
                self.DisconnectGBDropdowns()
                self.DisconnectCSDropdowns()
                self.ClearWLBoundCombos()
                self.ToggleGBGUI(False)
                self.ToggleCSGUI(False)
                self.ConnectGBDropdowns()
                self.ConnectCSDropdowns()
                self.ResetGBChart()
                self.ResetCSChart()
                self.ClearGBCoeffTable()
                self.ClearGBInterpTable()
                self.ClearCSCoeffTable()
                self.ClearCSInterpTable()
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

    def ToggleCSGUI(self, state):
        self.ui.combo_CSLowerWL.setEnabled(state)
        self.ui.combo_CSUpperWL.setEnabled(state)
        self.ui.lineEdit_CSStep.setEnabled(state)
        self.ui.pushButton_CSEvaluate.setEnabled(state)

    def ClearWLBoundCombos(self):
        try:
            self.ui.combo_GBLowerWL.clear()
            self.ui.combo_GBUpperWL.clear()
            self.ui.combo_GBLowerWLFit.clear()
            self.ui.combo_GBUpperWLFit.clear()
            self.ui.combo_CSLowerWL.clear()
            self.ui.combo_CSUpperWL.clear()
        except Exception as err:
            raise err

    def PopulateWLBoundCombos(self):
        try:
            for wavelength in self.wavelengths:
                self.ui.combo_GBLowerWLFit.addItem(str(wavelength))
                self.ui.combo_GBUpperWLFit.addItem(str(wavelength))
                self.ui.combo_GBLowerWL.addItem(str(wavelength))
                self.ui.combo_GBUpperWL.addItem(str(wavelength))
                self.ui.combo_CSLowerWL.addItem(str(wavelength))
                self.ui.combo_CSUpperWL.addItem(str(wavelength))
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

    def ClearCSCoeffTable(self):
        try:
            self.ui.tableWidget_CSCoefficients.clear()
            self.ui.tableWidget_CSCoefficients.setHorizontalHeaderLabels(self.CScoeffTableHeaders)
            self.ui.tableWidget_CSCoefficients.resizeColumnsToContents()
        except Exception as err:
            raise err

    def ClearCSInterpTable(self):
        try:
            self.ui.tableWidget_CSInterpolation.clear()
            self.ui.tableWidget_CSInterpolation.setHorizontalHeaderLabels(self.CSinterpTableHeaders)
            self.ui.tableWidget_CSInterpolation.resizeColumnsToContents()
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

    def PopulateCSCoeffTable(self):
        try:
            self.ClearCSCoeffTable()
            nSegments = len(self.CScoefficients[0])
            self.ui.tableWidget_CSCoefficients.setRowCount(nSegments)
            self.ui.tableWidget_CSCoefficients.setColumnCount(6)
            self.ui.tableWidget_CSCoefficients.setHorizontalHeaderLabels(self.CScoeffTableHeaders)
            for i in range(nSegments):
                iItem = QtWidgets.QTableWidgetItem(str(i))
                iItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                iItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 0, iItem)

                segmentItem = QtWidgets.QTableWidgetItem("%.2f nm to %.2f nm" % (self.CSfit.x[i], self.CSfit.x[i+1]))
                segmentItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                segmentItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 1, segmentItem)

                a_iItem = QtWidgets.QTableWidgetItem("%.6e" % (self.CScoefficients[3, i]))
                a_iItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                a_iItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 2, a_iItem)

                b_iItem = QtWidgets.QTableWidgetItem("%.6e" % (self.CScoefficients[2, i]))
                b_iItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                b_iItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 3, b_iItem)

                c_iItem = QtWidgets.QTableWidgetItem("%.6e" % (self.CScoefficients[1, i]))
                c_iItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                c_iItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 4, c_iItem)

                d_iItem = QtWidgets.QTableWidgetItem("%.6e" % (self.CScoefficients[0, i]))
                d_iItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                d_iItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSCoefficients.setItem(i, 5, d_iItem)

            self.ui.tableWidget_CSCoefficients.resizeColumnsToContents()
        except Exception as err:
            raise err

    def PopulateCSInterpTable(self):
        try:
            self.ClearCSInterpTable()
            self.ui.tableWidget_CSInterpolation.setRowCount(len(self.CSinterpWavelengths))
            self.ui.tableWidget_CSInterpolation.setColumnCount(2)
            self.ui.tableWidget_CSInterpolation.setHorizontalHeaderLabels(self.CSinterpTableHeaders)
            for row, (wavelength, irradiance) in enumerate(zip(self.CSinterpWavelengths, self.CSinterpIrradiances)):
                interpWLItem = QtWidgets.QTableWidgetItem("%.2f" % (wavelength))
                interpWLItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                interpWLItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSInterpolation.setItem(row, 0, interpWLItem)

                InterpIrItem = QtWidgets.QTableWidgetItem("%.6e" % (irradiance))
                InterpIrItem.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                InterpIrItem.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.ui.tableWidget_CSInterpolation.setItem(row, 1, InterpIrItem)
            self.ui.tableWidget_CSInterpolation.resizeColumnsToContents()
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

    def Clicked_CSEvaluate(self):
        try:
            fileTimeStr = "%d-%d-%d_%d-%d-%d" % (
                datetime.today().day, 
                datetime.today().month, 
                datetime.today().year, 
                datetime.today().hour, 
                datetime.today().minute, 
                datetime.today().second,
            )
            self.CSinterpfile = ".".join(str(self.InputFilename).split(".")[:-1]) + "-Cubic_Spline_Interpolation-%s.csv" % (fileTimeStr)
            nIssues = self.CheckCSInputs()
            if nIssues != 0:
                self.ClearCSCoeffTable()
                self.ClearCSInterpTable()
                self.ResetCSChart()
                self.IssuesMsgBox.show()
            else:
                self.CSinterpfile, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Write cubic spline interpolation to file", self.CSinterpfile, filter="CSV (*.csv)")
                if self.CSinterpfile == "":
                    self.IssuesMsgBox.setText(self.IssuesMsgBox.text() + "  - Write to file cancelled. Results not yet saved!")
                    self.IssuesMsgBox.show()
                else:
                    if self.CheckCSOutputFileExists() == 0:
                        self.CSEvaluate()
                        self.WriteCSInterpolationToFile()
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
            self.GBa,
            self.GBb,
            self.GBcoefficients,
            float(self.ui.lineEdit_GBStep.text()),
        )
        self.GBBBtemperature = IIF.ApparentBBTemp(self.GBinterpWavelengths, self.GBinterpIrradiances)
        self.PopulateGBCoeffTable()
        self.PopulateGBInterpTable()
        self.UpdateGBChart()

    def CSEvaluate(self):
        self.CSinterpWavelengths, self.CSinterpIrradiances, self.CScoefficients = [], [], []
        self.CSinterpWavelengths, self.CSinterpIrradiances, self.CScoefficients, self.CSfit = IIF.CubicSplineInterpolation(
            self.wavelengths,
            self.irradiances,
            (float(self.ui.combo_CSLowerWL.currentText()), float(self.ui.combo_CSUpperWL.currentText())),
            int(self.ui.lineEdit_CSStep.text()),
        )
        self.PopulateCSCoeffTable()
        self.PopulateCSInterpTable()
        self.UpdateCSChart()

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

    def CheckCSInputs(self):
        try:
            nIssues = 0
            errMsg = "The following issues need corrected:\n"
            # check if lower wavelength is smaller than upper wavelength for CS fit parameters
            if float(self.ui.combo_CSLowerWL.currentText()) >= float(self.ui.combo_CSUpperWL.currentText()):
                errMsg = errMsg + "  - the lower wavelength must be less than the upper wavelength in cubic spline interpolation parameters\n"
                nIssues += 1

            # check if CS step is float and greater than zero
            try:
                if float(self.ui.lineEdit_CSStep.text()) <= 0:
                    errMsg = errMsg + "  - the cubic spline interpolation step must be a float greater than zero\n"
                    nIssues += 1
            except Exception as dofIntErr:
                if "could not convert string to float" in str(dofIntErr):
                    errMsg = errMsg + "  - the cubic spline interpolation step must be a float greater than zero\n"
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

    def CheckCSOutputFileExists(self):
        try:
            with open(self.CSinterpfile, "w") as openedfile:
                openedfile.write("")
                return 0
        except Exception as openFileErr:
            if "Permission denied" in str(openFileErr):
                errMsg = self.IssuesMsgBox.text() + "  - close the file %s to write evaluations to it.\n" % (self.CSinterpfile)
                self.IssuesMsgBox.setText(errMsg)
                return 1
            else:
                raise openFileErr

    def WriteGBInterpolationToFile(self):
        try:
            with open(self.GBinterpfile, "w") as openedfile:
                openedfile.write("Gray body interpolation coefficients\n")
                openedfile.write("A_n, Coefficient, Uncertainty (k=1)\n")
                for i, (coefficient, uncertainty) in enumerate(zip(self.GBcoefficients, self.GBuncertainty)):
                    openedfile.write("A%d, %.12e, %.12e\n" % (i, coefficient, uncertainty))
                openedfile.write("a, %.12e, %.12e\n" % (self.GBa, self.abUncertainty[0]))
                openedfile.write("b, %.12e, %.12e\n" % (self.GBb, self.abUncertainty[1]))
                openedfile.write("\n")

                openedfile.write("Peak wavelength = %.1f\n" % (IIF.PeakWavelength(self.GBinterpWavelengths, self.GBinterpIrradiances)))
                openedfile.write("Apparent blackbody temperature = %.1f\n\n" % (self.GBBBtemperature))

                openedfile.write("Gray body interpolated data\n")
                openedfile.write("Interpolated wavelength, Interpolated irradiance\n")
                for i, (wavelength, irradiance) in enumerate(zip(self.GBinterpWavelengths, self.GBinterpIrradiances)):
                    openedfile.write("%.2f, %.6e\n" % (wavelength, irradiance))
                openedfile.write("\n")

                openedfile.write("Measured data\n")
                openedfile.write("Wavelength, Irradiance\n")
                for i, (wavelength, irradiance) in enumerate(zip(self.wavelengths, self.irradiances)):
                    openedfile.write("%.2f, %.6e\n" % (wavelength, irradiance))
                self.EvalComplete.setText("Interpolation complete! Results are stored at: %s" % (self.GBinterpfile))
                self.EvalComplete.show()
                subprocess.Popen(r"explorer /select,%s" % (Path(self.GBinterpfile)))
        except Exception as err:
            raise err

    def WriteCSInterpolationToFile(self):
        try:
            nSegments = len(self.CScoefficients[0])
            with open(self.CSinterpfile, "w") as openedfile:
                openedfile.write("Cubic spline interpolation coefficients\n")
                openedfile.write("i, Segment, a_i, b_i, c_i, d_i\n")
                for i in range(nSegments):
                    openedfile.write("%d, %.2f to %.2f, %.6e, %.6e, %.6e, %.6e\n" % (i, self.CSfit.x[i], self.CSfit.x[i+1], self.CScoefficients[3, i], self.CScoefficients[2, i], self.CScoefficients[1, i], self.CScoefficients[0, i]))
                openedfile.write("\n")

                openedfile.write("Cubic spline interpolated data\n")
                openedfile.write("Interpolated wavelength, Interpolated irradiance\n")
                for i, (wavelength, irradiance) in enumerate(zip(self.CSinterpWavelengths, self.CSinterpIrradiances)):
                    openedfile.write("%.2f, %.6e\n" % (wavelength, irradiance))
                openedfile.write("\n")

                openedfile.write("Measured data\n")
                openedfile.write("Wavelength, Irradiance\n")
                for i, (wavelength, irradiance) in enumerate(zip(self.wavelengths, self.irradiances)):
                    openedfile.write("%.2f, %.6e\n" % (wavelength, irradiance))
                self.EvalComplete.setText("Interpolation complete! Results are stored at: %s" % (self.CSinterpfile))
                self.EvalComplete.show()
                subprocess.Popen(r"explorer /select,%s" % (Path(self.CSinterpfile)))
        except Exception as err:
            raise err
        pass

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
        self.ax_GBResiduals.set_ylabel(r"Residuals ($\frac{W}{cm^{3}}$)")
        self.ax_GBResiduals.set_xlabel("Wavelength (nm)")
        self.ax_GBResiduals.grid()
        self.ui.GBChart.Figure.subplots_adjust(hspace=0.1, left=0.185, right=0.95, bottom=0.13, top=0.99)
        self.ui.GBChart.Canvas.draw()

    def ResetCSChart(self):
        self.ui.CSChart.Figure.clear()
        # self.ax_CSResiduals = self.ui.CSChart.Figure.add_subplot(2, 1, 2)
        # self.ax_CSIrradiance = self.ui.CSChart.Figure.add_subplot(2, 1, 1, sharex=self.ax_CSResiduals)
        self.ax_CSIrradiance = self.ui.CSChart.Figure.add_subplot(1, 1, 1)
        self.ax_CSIrradiance.measLine, = self.ax_CSIrradiance.plot([], [])
        self.ax_CSIrradiance.fitLine, = self.ax_CSIrradiance.plot([], [])
        # self.ax_CSResiduals.line, = self.ax_CSResiduals.plot([], [])
        self.ax_CSIrradiance.set_ylabel(r"Irradiance ($\frac{W}{cm^{3}})$")
        # self.ax_CSIrradiance.set_xticklabels([])
        self.ax_CSIrradiance.set_xlabel("Wavelength (nm)")
        self.ax_CSIrradiance.grid()
        # self.ax_CSResiduals.set_ylabel(r"Residuals ($\frac{W}{cm^{3}}$)")
        # self.ax_CSResiduals.set_xlabel("Wavelength (nm)")
        # self.ax_CSResiduals.grid()
        self.ui.CSChart.Figure.subplots_adjust(hspace=0.05, left=0.185, right=0.95, bottom=0.13, top=0.99)
        self.ui.CSChart.Canvas.draw()

    def UpdateGBChart(self):
        self.ResetGBChart()
        i_lowerBound, i_upperBound = IIF.WavelengthRegionIndex(
            self.wavelengths,
            (float(self.ui.combo_GBLowerWLFit.currentText()), float(self.ui.combo_GBUpperWLFit.currentText())),
        )
        residuals = IIF.GrayBody(self.wavelengths[i_lowerBound:i_upperBound], self.GBa, self.GBb, self.GBcoefficients) - self.irradiances[i_lowerBound:i_upperBound]
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
            residuals,
            marker=GUIvar.markerType,
            markersize=GUIvar.markerSize,
            markeredgecolor=GUIvar.markerEdgeColor,
            markerfacecolor=GUIvar.markerFaceColor,
            linestyle="None",
        )
        self.ax_GBResiduals.set_ylabel(r"Fit residuals ($\frac{W}{cm^{3}}$)")

        self.ui.GBChart.Canvas.draw()

    def UpdateCSChart(self):
        self.ResetCSChart()
        i_lowerBound, i_upperBound = IIF.WavelengthRegionIndex(
            self.wavelengths,
            (float(self.ui.combo_CSLowerWL.currentText()), float(self.ui.combo_CSUpperWL.currentText())),
        )
        residuals = self.CSfit(self.wavelengths[i_lowerBound:i_upperBound]) - self.irradiances[i_lowerBound:i_upperBound]
        self.ax_CSIrradiance.measLine, = self.ax_CSIrradiance.plot(
            self.wavelengths[i_lowerBound:i_upperBound],
            self.irradiances[i_lowerBound:i_upperBound],
            label="Measurements",
            marker=GUIvar.markerType,
            markersize=GUIvar.markerSize,
            markeredgecolor=GUIvar.markerEdgeColor,
            markerfacecolor=GUIvar.markerFaceColor,
            linestyle="None",
        )
        self.ax_CSIrradiance.fitLine, = self.ax_CSIrradiance.plot(
            self.CSinterpWavelengths,
            self.CSinterpIrradiances,
            label="Interpolated fit",
            color=GUIvar.fitLineColor,
            linewidth=GUIvar.fitLinewidth,
        )
        self.ax_CSIrradiance.set_ylabel(r"Irradiance ($\frac{W}{cm^{3}})$")
        self.ax_CSIrradiance.legend()

        self.ui.CSChart.Canvas.draw()

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
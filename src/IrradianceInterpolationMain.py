import sys
from PyQt5 import QtWidgets
from GUI.IrradianceInterpolationMainGUI import Window_IrradianceInterpolationMain

print("\nLaunching Irradiance Interpolation ...\n")
IrradianceInterpolationApp = QtWidgets.QApplication(sys.argv)
IrradianceInterpolationWindow = Window_IrradianceInterpolationMain()
IrradianceInterpolationWindow.show()
IrradianceInterpolationApp.exec()

print("\nQuitting Irradiance Interpolation ...\n")

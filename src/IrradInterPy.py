import sys
from PyQt5 import QtWidgets
from GUI.IrradianceInterpolationMainGUI import Window_IrradianceInterpolationMain

if getattr(sys, "frozen", False):
    import pyi_splash

print("\nLaunching Irradiance Interpolation ...\n")
IrradianceInterpolationApp = QtWidgets.QApplication(sys.argv)
IrradianceInterpolationWindow = Window_IrradianceInterpolationMain()

if getattr(sys, "frozen", False):
    pyi_splash.close()

IrradianceInterpolationWindow.show()
IrradianceInterpolationApp.exec()

print("\nQuitting Irradiance Interpolation ...\n")

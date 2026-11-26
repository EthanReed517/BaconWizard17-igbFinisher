import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QComboBox
import configparser
import os

import info
from ui.func_Main import MainWindow

app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
window.show()
app.exec()
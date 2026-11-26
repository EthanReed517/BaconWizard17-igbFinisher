# ########### #
# INFORMATION #
# ########### #
# This module is the main function for igbFinisher that the rest of the program runs on.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
from ui.func_Main import MainWindow
# External modules
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt


# ############## #
# MAIN EXECUTION #
# ############## #
# Run it!
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
    window.show()
    app.exec()
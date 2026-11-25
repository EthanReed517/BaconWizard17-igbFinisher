import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from ui_About import Ui_Dialog
from ui_Main import Ui_MainWindow


class AboutWindow(QWidget, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.about_win = None
        
        self.actionAbout.triggered.connect(self.OpenAbout)
    
    def OpenAbout(self):
        if self.about_win is None:
            self.about_win = AboutWindow()
        self.about_win.show()
        self.about_win.raise_()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
window.show()
app.exec()
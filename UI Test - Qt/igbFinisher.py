import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QComboBox

from ui_About import Ui_Dialog
from ui_Main import Ui_MainWindow

APP_NAME = 'igbFinisher'
APP_VERSION = '5.0.0'
APP_AUTHOR = 'BaconWizard17'
APP_DESCRIPTION = 'A program to process igb files after exporting from 3ds Max.'
APP_URL = 'https://marvelmods.com/forum/index.php/topic,11440.0.html'
APP_GITHUB = 'https://github.com/EthanReed517/BaconWizard17-igbFinisher'
ASSET_TYPES = ['Skin', 'Mannequin', '3D Head', 'Conversation Portrait', 'Character Select Portrait', 'Comic Cover', 'Concept Art', 'Loading Screen', 'Other']

class AboutWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.label_name.setText(APP_NAME)
        self.label_version.setText(f'Version v{APP_VERSION}')
        self.label_desc.setText(APP_DESCRIPTION)
        self.label_url.setText(f'<a href="{APP_URL}">Marvel Mods Release Post</a>')
        self.label_url_github.setText(f'<a href="{APP_GITHUB}">GitHub Page</a>')
        
        self.setFixedSize(self.sizeHint())


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.about_win = None
        
        self.actionAbout.triggered.connect(self.OpenAbout)
        self.actionExit.triggered.connect(self.close)
        
        self.comboBox_forced_assets.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.RefreshForcedAssets()
    
    def RefreshForcedAssets(self):
        self.comboBox_forced_assets.blockSignals(True)
        self.comboBox_forced_assets.clear()
        self.comboBox_forced_assets.addItems(['None', *ASSET_TYPES])
        self.comboBox_forced_assets.setCurrentIndex(0)
        self.comboBox_forced_assets.blockSignals(False)
    
    def OpenAbout(self):
        if self.about_win is None:
            self.about_win = AboutWindow(self)
        self.about_win.show()
        self.about_win.raise_()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips, True)
window.show()
app.exec()
from PySide6.QtWidgets import QDialog
import info
from .ui_About import Ui_Dialog

class AboutWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        self.label_name.setText(info.APP_NAME)
        self.label_version.setText(f'Version v{info.APP_VERSION}')
        self.label_desc.setText(info.APP_DESCRIPTION)
        self.label_url.setText(f'<a href="{info.APP_URL}">Marvel Mods Release Post</a>')
        self.label_url_github.setText(f'<a href="{info.APP_GITHUB}">GitHub Page</a>')
        
        self.setFixedSize(self.sizeHint())
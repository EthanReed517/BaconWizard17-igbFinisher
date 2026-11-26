# ########### #
# INFORMATION #
# ########### #
# This module sets up the functionality of the about window.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
from .ui_About import Ui_Dialog
import info
# External modules
from PySide6.QtWidgets import QDialog


# ####### #
# CLASSES #
# ####### #
# This is the about window.
class AboutWindow(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # Dynamically set the information from the version file.
        self.label_name.setText(info.APP_NAME)
        self.label_version.setText(f'Version v{info.APP_VERSION}')
        self.label_desc.setText(info.APP_DESCRIPTION)
        self.label_url.setText(f'<a href="{info.APP_URL}">Marvel Mods Release Post</a>')
        self.label_url_github.setText(f'<a href="{info.APP_GITHUB}">GitHub Page</a>')
        # Prevent resizing.
        self.setFixedSize(self.sizeHint())
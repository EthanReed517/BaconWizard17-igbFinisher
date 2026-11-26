# ########### #
# INFORMATION #
# ########### #
# This module sets up the functionality of the about window.


# ####### #
# IMPORTS #
# ####### #
# Internal modules
from .func_About import AboutWindow
from .ui_Main import Ui_MainWindow
import info
# External modules
from PySide6 import QtWidgets, QtCore
import configparser
import os


# ################ #
# GLOBAL VARIABLES #
# ################ #
INI_PATH = 'settings.ini'
CONFIG = configparser.ConfigParser()
CONFIG.optionxform = str


# ####### #
# CLASSES #
# ####### #
# This is the main window.
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.about_win = None
        # Prevent recursive popups on focus loss.
        self._validating = False
        # Add menubar functions.
        self.actionAbout.triggered.connect(self.OpenAbout)
        self.actionExit.triggered.connect(self.close)
        # Load the options for the forced asset type.
        self.comboBox_forced_assets.setSizeAdjustPolicy(
            QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.RefreshForcedAssets()
        # Map settings values to their controls.
        self.num_controls = {
            'XML1_num': (self.radioButton_xml1_num_none, self.radioButton_xml1_num, self.lineEdit_xml1_num),
            'XML2_num': (self.radioButton_xml2_num_none, self.radioButton_xml2_num, self.lineEdit_xml2_num),
            'MUA1_num': (self.radioButton_mua1_num_none, self.radioButton_mua1_num, self.lineEdit_mua1_num),
            'MUA2_num': (self.radioButton_mua2_num_none, self.radioButton_mua2_num, self.lineEdit_mua2_num)
        }
        self.path_controls = {
            'XML1_path': (self.radioButton_xml1_path_none, self.radioButton_xml1_path_detect, self.radioButton_xml1_path, self.lineEdit_xml1_path, self.toolButton_xml1_path),
            'XML2_path': (self.radioButton_xml2_path_none, self.radioButton_xml2_path_detect, self.radioButton_xml2_path, self.lineEdit_xml2_path, self.toolButton_xml2_path),
            'MUA1_path': (self.radioButton_mua1_path_none, self.radioButton_mua1_path_detect, self.radioButton_mua1_path, self.lineEdit_mua1_path, self.toolButton_mua1_path),
            'MUA2_path': (self.radioButton_mua2_path_none, self.radioButton_mua2_path_detect, self.radioButton_mua2_path, self.lineEdit_mua2_path, self.toolButton_mua2_path)
        }
        # Settings functions.
        self.load_settings()
        self.connect_signals()
    
    # ################## #
    # SETTINGS FUNCTIONS #
    # ################## #
    
    def is_number(self, value: str) -> bool:
        """Evaluates if a string is a valid integer or float."""
        try:
            int(value)
            return ((len(value) >= 4) and (len(value) <= 5))
        except ValueError:
            return False
            
    def save_ini(self):
        """Writes the current config state back to settings.ini."""
        with open(INI_PATH, "w", encoding="utf-8") as f:
            CONFIG.write(f)

    def load_settings(self):
        """Reads settings.ini on startup and initializes widget states."""
        if os.path.exists(INI_PATH):
            CONFIG.read(INI_PATH, encoding="utf-8")

        if "ASSET" not in CONFIG:
            CONFIG["ASSET"] = {}

        for key, (rb_none, rb_num, line_edit) in self.num_controls.items():
            # Default to "None" if the key is missing from the file
            val = CONFIG["ASSET"].get(key, "None").strip()

            if val == "None":
                rb_none.setChecked(True)
                line_edit.clear()
                line_edit.setEnabled(False)

            elif val == "Ask":
                rb_num.setChecked(True)
                line_edit.clear()
                line_edit.setEnabled(True)
                
            else:
                rb_num.setChecked(True)
                line_edit.setEnabled(True)
                if self.is_number(val):
                    line_edit.setText(val)
                else:
                    line_edit.clear()
                    QtWidgets.QMessageBox.warning(
                        self,
                        "Invalid Setting",
                        f"The value '{val}' for {key} in settings.ini is not a valid number."
                    )

        for key, (rb_none, rb_detect, rb_path, line_edit, tool_button) in self.path_controls.items():
            # Default to "None" if the key is missing from the file
            val = CONFIG["ASSET"].get(key, "None").strip()

            if val == "None":
                rb_none.setChecked(True)
                line_edit.clear()
                line_edit.setEnabled(False)
                tool_button.setEnabled(False)

            elif val == "Detect":
                rb_detect.setChecked(True)
                line_edit.clear()
                line_edit.setEnabled(False)
                tool_button.setEnabled(False)

            elif val == "Ask":
                rb_path.setChecked(True)
                line_edit.clear()
                line_edit.setEnabled(True)
                tool_button.setEnabled(True)
                
            else:
                rb_path.setChecked(True)
                line_edit.setEnabled(True)
                tool_button.setEnabled(True)
                line_edit.setText(val)
                

    def connect_signals(self):
        """Connects radio buttons and line edits using default arguments to capture loop variables."""
        for key, (rb_none, rb_num, line_edit) in self.num_controls.items():
            # toggled fires when checked state changes; we only act when checked == True
            rb_none.toggled.connect(
                lambda checked, k=key: self.on_none_selected_num(k) if checked else None
            )
            rb_num.toggled.connect(
                lambda checked, k=key: self.on_number_selected(k) if checked else None
            )
            # editingFinished triggers when the user presses Enter or tabs/clicks away
            line_edit.editingFinished.connect(
                lambda k=key: self.on_line_edit_finished(k)
            )
        for key, (rb_none, rb_detect, rb_path, line_edit, tool_button) in self.path_controls.items():
            # toggled fires when checked state changes; we only act when checked == True
            rb_none.toggled.connect(
                lambda checked, k=key: self.on_none_selected_path(k) if checked else None
            )
            rb_detect.toggled.connect(
                lambda checked, k=key: self.on_detect_selected(k) if checked else None
            )
            rb_path.toggled.connect(
                lambda checked, k=key: self.on_path_selected(k) if checked else None
            )
            # editingFinished triggers when the user presses Enter or tabs/clicks away
            #line_edit.editingFinished.connect(
                #lambda k=key: self.on_line_edit_finished(k)
            #)

    def on_none_selected_num(self, key: str):
        """Handles switching to the 'None' radio button."""
        _, _, line_edit = self.num_controls[key]
        line_edit.clear()
        line_edit.setEnabled(False)

        CONFIG["ASSET"][key] = "None"
        self.save_ini()

    def on_none_selected_path(self, key: str):
        """Handles switching to the 'None' radio button."""
        _, _, _, line_edit, tool_button = self.num_controls[key]
        line_edit.clear()
        line_edit.setEnabled(False)
        tool_button.setEnabled(False)

        CONFIG["ASSET"][key] = "None"
        self.save_ini()

    def on_detect_selected(self, key: str):
        """Handles switching to the 'Detect' radio button."""
        _, _, _, line_edit, tool_button = self.num_controls[key]
        line_edit.clear()
        line_edit.setEnabled(False)
        tool_button.setEnabled(False)

        CONFIG["ASSET"][key] = "Detect"
        self.save_ini()

    def on_number_selected(self, key: str):
        """Handles switching to the 'Number' radio button."""
        _, _, line_edit = self.num_controls[key]
        line_edit.setEnabled(True)

        # If currently empty, immediately set to "Ask"
        if not line_edit.text().strip():
            CONFIG["ASSET"][key] = "Ask"
            self.save_ini()

    def on_path_selected(self, key: str):
        """Handles switching to the 'Path' radio button."""
        _, _, _, line_edit, tool_button = self.num_controls[key]
        line_edit.setEnabled(True)
        tool_button.setEnabled(True)

        # If currently empty, immediately set to "Ask"
        if not line_edit.text().strip():
            CONFIG["ASSET"][key] = "Ask"
            self.save_ini()

    def on_line_edit_finished(self, key: str):
        """Validates line edit input when focus leaves or Enter is pressed."""
        if self._validating:
            return

        _, rb_num, line_edit = self.num_controls[key]

        # Ignore if 'Number' isn't selected (e.g., if disabled programmatically)
        if not rb_num.isChecked():
            return

        text = line_edit.text().strip()

        if text == "":
            # Empty box writes "Ask"
            CONFIG["ASSET"][key] = "Ask"
            self.save_ini()
        elif self.is_number(text):
            # Valid number writes the number
            CONFIG["ASSET"][key] = text
            self.save_ini()
        else:
            # Invalid entry: show popup, do NOT update ini, refocus line edit
            self._validating = True
            QtWidgets.QMessageBox.warning(
                self,
                "Invalid Number",
                f"'{text}' is not a valid number for {key}. Please enter a valid numeric value."
            )
            # QTimer.singleShot ensures focus returns cleanly after the modal dialog closes
            QtCore.QTimer.singleShot(0, lambda: self._refocus_edit(line_edit))

    def _refocus_edit(self, line_edit: QtWidgets.QLineEdit):
        line_edit.setFocus()
        line_edit.selectAll()
        self._validating = False
    
    # ###################### #
    # END SETTINGS FUNCTIONS #
    # ###################### #
    
    def RefreshForcedAssets(self):
        self.comboBox_forced_assets.blockSignals(True)
        self.comboBox_forced_assets.clear()
        self.comboBox_forced_assets.addItems(['None', *info.ASSET_TYPES])
        self.comboBox_forced_assets.setCurrentIndex(0)
        self.comboBox_forced_assets.blockSignals(False)
    
    def OpenAbout(self):
        if self.about_win is None:
            self.about_win = AboutWindow(self)
        self.about_win.show()
        self.about_win.raise_()
@echo off
pyside6-uic ui_Main.ui -o ui_Main.py
pyside6-uic ui_About.ui -o ui_About.py
pyside6-rcc ui_resources.qrc -o ui_resources_rc.py
py igbFinisher.py
pause
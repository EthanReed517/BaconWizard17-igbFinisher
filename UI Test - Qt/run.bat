@echo off
pyside6-uic --from-imports designer/ui_Main.ui -o ui/ui_Main.py
pyside6-uic --from-imports designer/ui_About.ui -o ui/ui_About.py
pyside6-rcc designer/ui_resources.qrc -o ui/ui_resources_rc.py
py igbFinisher.py
pause
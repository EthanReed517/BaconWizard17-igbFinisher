@echo off
echo Clearing existing folder...
if exist dist del /q dist
echo Copying resources...
robocopy >nul Scripts dist\Scripts
if exist XVI32 robocopy >nul XVI32 dist\XVI32
copy >nul settings.ini dist
echo Running pyInstaller...
pyinstaller igbFinisher.py --onefile --additional-hooks-dir=. --icon=icon.ico --add-data "icon.ico:." --add-data "images/dropZone.png:images"
echo Installation complete.
pause
@echo off
echo Clearing existing folder...
if exist dist del /q dist
echo Copying resources...
robocopy >nul Scripts dist\Scripts
echo 1) Personal Build
echo 2) Release Build
choice /c 12 /m "Which build are you doing?"
if %errorlevel% equ 2 robocopy >nul "Folder Detection" "dist\Folder Detection"
if %errorlevel% equ 1 robocopy >nul "Folder Detection (Personal)" "dist\Folder Detection"
copy >nul settings.ini dist
echo Running pyInstaller...
pyinstaller igbFinisher.py --onefile --additional-hooks-dir=. --icon=icon.ico --add-data "icon.ico:." --add-data "images/dropZone.png:images"
echo Installation complete.
pause
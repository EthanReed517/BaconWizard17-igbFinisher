@echo off
echo Clearing existing folder...
if exist dist del /q dist
echo 1) Personal Build
echo 2) Release Build
choice /c 12 /m "Which build are you doing?"
if %errorlevel% equ 2 robocopy >nul "Folder Detection" "dist\Folder Detection"
if %errorlevel% equ 1 (
	robocopy >nul "Folder Detection (Personal)" "dist\Folder Detection"
	robocopy >nul "Animation Producer" "dist\Animation Producer"
)
echo Copying resources...
robocopy >nul Scripts dist\Scripts
copy >nul settings.ini dist
echo Running pyInstaller...
pyinstaller igbFinisher.py --onefile --icon=icon.ico --add-data "icon.ico:."
echo Installation complete.
pause
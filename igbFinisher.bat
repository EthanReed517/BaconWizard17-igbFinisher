@echo off
REM set the title
title igbFinisher
REM verify that XVI32 exists
if exist "XVI32" (
	REM XVI32 folder exists
	REM verify that XVI32.exe exists
	if exist "XVI32\XVI32.exe" (
		REM exe exists
		REM call the python file
		py igbFinisher.py
	) else (
		REM exe does not exist
		REM warn the user
		echo XVI32.exe was not found in the XVI32 folder. Please ensure that XVI32 is installed
	)
) else (
	REM folder does not exist
	REM warn the user
	echo XVI32 folder not found. Please ensure that XVI32 is installed.
)
REM pause to allow the program to stay open
pause
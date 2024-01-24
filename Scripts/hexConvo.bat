@echo off

REM Perform the hex editing
REM 	%1 = file name
REM 	%2 = hex code for 12301_conversation.png
REM 	%3 = (skin number)_conversation.png to overwrite 12301_conversation.png
START /W XVI32\xvi32.exe %1 /S=Scripts\hexConvo.xsc %2 %3
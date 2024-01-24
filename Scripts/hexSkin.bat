@echo off

REM Perform the hex editing
REM 	%1 = file name
REM 	%2 = hex code for igActor01_Appearance
REM 	%3 = (skin number) to overwrite igActor01_Appearance
REM 	%4 = hex code for 12301_outline
REM 	%5 = (skin number)_outline to overwrite 12301_outline
REM 	%6 = hex code for 12301_
REM 	%7 = (skin number)_ to overwrite 12301_
REM 	%8 = hex code for 12301
REM 	%9 = (skin number) to overwrite 12301
START /W XVI32\xvi32.exe %1 /S=Scripts\hexSkin.xsc %2 %3 %4 %5 %6 %7 %8 %9
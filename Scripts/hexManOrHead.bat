@echo off

REM Perform the hex editing
REM 	%1 = file name
REM 	%2 = hex code for 12301_
REM 	%3 = (skin number)_ to overwrite 12301_
REM 	%4 = hex code for 12301
REM 	%5 = (skin number) to overwrite 12301
START /W XVI32\xvi32.exe %1 /S=Scripts\hexManOrHead.xsc %2 %3 %4 %5
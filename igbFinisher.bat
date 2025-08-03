@echo off
set "cmdpath=%~dp0"
setlocal enableDelayedExpansion
set "cmd=!cmdcmdline!"
set "cmd2=!cmd:*%~f0=!"
if "!cmd2!" == "!cmd!" goto isbatch
endlocal
for %%p in (%*) do 2>nul pushd "%~1" && goto isfolder || goto isfiles

:isbatch
endlocal
for /R %%f in (*.igb) do (
    py "%cmdpath%\igbFinisher.py" "%%~f"
)
pause
goto eof

:isfolder
if (%1) == () goto eof
for %%f in ("%~1\*.igb") do (
    py "%cmdpath%\igbFinisher.py" "%%~f"
)
pause
shift
goto isfolder

:isfiles
for %%f in (%*) do (
    py "%cmdpath%\igbFinisher.py" "%%~f"
)
pause
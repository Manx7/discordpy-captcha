@echo off
title Manx7 - Prebuilt Captcha Bot
WHERE pip>nul
IF %ERRORLEVEL% NEQ 0 goto no_pip
echo Checking for and installing requirements... (Requests)
echo.
pip install requests
cls
echo Checking for and installing requirements... (Discord)
echo.
pip install discord
cls

WHERE python>nul
IF %ERRORLEVEL% NEQ 0 goto no_python

:python_start
python captcha.py
pause
exit

:no_pip
echo Unable to find "pip", the python package manager.
echo PIP is needed to check and install the requirements for this bot!
pause
exit

:no_python
echo Unable to find python, please make sure you've properly installed it.
pause
exit
@echo off
title Manx7 - Prebuilt Captcha Bot
WHERE npm>nul
IF %ERRORLEVEL% NEQ 0 goto no_npm
npm start
pause
exit

:no_npm
echo Node Package Manager (NPM) is not installed, don't worry though, it's not required in the slightest!
echo Just use the "run.cmd" instead, NPM is a node.js based system and I only kept it for the
echo ability to give credit to the person who helped me design the Python version, AnticcX.
pause
exit
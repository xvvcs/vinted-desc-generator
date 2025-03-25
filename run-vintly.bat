@echo off
echo Starting Vintly...

REM Create a temporary batch file to monitor Flask output
echo @echo off > monitor.bat
echo :loop >> monitor.bat
echo timeout /t 1 /nobreak ^> nul >> monitor.bat
echo findstr /C:"Running on" temp_output.txt >> monitor.bat
echo if errorlevel 1 goto loop >> monitor.bat
echo for /f "tokens=4 delims= " %%%%a in ('findstr /C:"Running on" temp_output.txt') do set URL=%%%%a >> monitor.bat
echo set URL=%%URL:~0,-1%% >> monitor.bat
echo start %%URL%% >> monitor.bat
echo exit >> monitor.bat

REM Start Flask in the background and redirect output
start /B cmd /c "python app.py > temp_output.txt 2>&1"

REM Run the monitor to detect when Flask is ready and open browser
start /wait monitor.bat

REM Clean up temporary files
del monitor.bat
del temp_output.txt

echo Vintly is running!
echo When you're done, close this window to shut down the server.
pause

REM When user presses a key, kill the Flask process
taskkill /F /IM python.exe /T
echo Vintly has been shut down.
timeout /t 2 > nul
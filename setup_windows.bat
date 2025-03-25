@echo off
setlocal EnableDelayedExpansion
title Vintly Installation

echo.
echo ========================================
echo         Vintly Setup Assistant
echo ========================================
echo.

REM Check if Python is installed
echo Checking for Python...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo [ERROR] Python is not installed or not in PATH.
  echo Please install Python 3.12.9 from https://www.python.org/downloads/
  echo IMPORTANT: Check "Add Python to PATH" during installation.
  echo.
  pause
  exit /b 1
)

echo [SUCCESS] Python is installed.
echo.

REM Install dependencies
echo Installing required packages...
pip install flask==3.0.2 Werkzeug==3.0.1 python-dotenv==1.0.1 google-generativeai==0.3.2 Pillow==9.5.0 flask-sqlalchemy==3.1.1 flask-migrate==4.0.5
if %ERRORLEVEL% NEQ 0 (
  echo [WARNING] Some packages may not have installed correctly.
  echo We'll continue anyway, but you might encounter issues.
  echo.
)

echo [SUCCESS] Packages installed.
echo.

REM Prompt for API key
echo ========================================
echo Now let's set up your Google API key:
echo ========================================
echo.
echo You can get an API key from: https://makersuite.google.com/app/apikey
echo.
set /p API_KEY="Enter your Google API key: "

REM Validate input
if "!API_KEY!"=="" (
  echo [ERROR] API key cannot be empty.
  echo Please run the setup again and provide a valid key.
  pause
  exit /b 1
)

REM Create .env file
echo Creating .env file with your API key...
echo GOOGLE_API_KEY=!API_KEY!> .env
echo.
echo [SUCCESS] API key saved to .env file.
echo.

REM Offer to start the application
echo ========================================
echo        Installation Complete!
echo ========================================
echo.
echo Vintly has been successfully set up on your computer.
echo.
set /p START_APP="Would you like to start Vintly now? (Y/N): "

if /i "!START_APP!"=="Y" (
  echo.
  echo Starting Vintly...
  start cmd /k "python app.py"
  echo.
  echo If a new command window opened, Vintly is running!
  echo Open your web browser and go to: http://localhost:5001
) else (
  echo.
  echo To start Vintly later, run: python app.py
  echo Then open your web browser and go to: http://localhost:5001
)

echo.
echo Thank you for installing Vintly!
echo.
pause
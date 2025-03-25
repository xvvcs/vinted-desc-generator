<!-- filepath: /Users/maciej/vinDesc/setup_windows.bat -->
@echo off
echo Setting up Vintly application...

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
  echo Python is not installed or not in PATH. Please install Python 3.8+ and try again.
  pause
  exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Update pip
echo Updating pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
  echo Creating .env file...
  echo GOOGLE_API_KEY=your_api_key_here> .env
  echo Please edit the .env file and add your Google API key.
)

echo Setup complete! Run 'run_windows.bat' to start the application.
pause
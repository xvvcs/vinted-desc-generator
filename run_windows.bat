<!-- filepath: /Users/maciej/vinDesc/run_windows.bat -->
@echo off
echo Starting Vintly application...

REM Activate virtual environment
call .venv\Scripts\activate

REM Run the Flask app
python app.py

pause
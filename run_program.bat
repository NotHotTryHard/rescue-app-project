@echo off
setlocal enabledelayedexpansion

REM Setting title for the command window
title Rescue App Runner

echo.
echo === Rescue Application Launcher ===
echo.

REM Navigate to the project directory
cd /d %~dp0

REM Output current path for debugging
echo Current path: %cd%
echo.

REM Check if requirements.txt exists
if not exist requirements.txt (
    echo [ERROR] File requirements.txt not found!
    echo Please ensure you're running this script from the project root directory.
    pause
    exit /b 1
)

REM Check for Python installation
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install required packages
echo Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [WARNING] Some dependencies might have failed to install.
)

echo.
echo === Starting Rescue Application ===
echo.

REM Run the application
echo Running application...
python run.py
set APP_EXIT_CODE=%ERRORLEVEL%

REM Deactivate virtual environment
echo.
echo Cleaning up...
call venv\Scripts\deactivate

if %APP_EXIT_CODE% neq 0 (
    echo.
    echo [WARNING] Application exited with code %APP_EXIT_CODE%
)

echo.
echo === Application closed ===
pause
endlocal
exit /b %APP_EXIT_CODE%
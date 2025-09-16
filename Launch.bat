@echo off
chcp 65001 >nul
title GD Loadout Randomizer
echo ===============================
echo   GD Loadout Randomizer
echo ===============================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo Error: Tkinter is not available
    echo This usually means you need to install Python with Tkinter support
    echo or install it separately for your system.
    pause
    exit /b 1
)

python -c "import PIL" 2>nul
if errorlevel 1 (
    echo PIL/Pillow package is not installed
    echo Installing Pillow package...
    pip install Pillow
    if errorlevel 1 (
        echo Error: Failed to install Pillow
        echo Please install it manually with: pip install Pillow
        pause
        exit /b 1
    )
    echo.
)

REM Run the application
echo Starting GD Loadout Randomizer...
echo.
python GDLoadoutRandomizerGUI.py

if errorlevel 1 (
    echo.
    echo The application exited with an error
    pause
)
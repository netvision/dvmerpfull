@echo off
echo ============================================
echo  Excel to CSV Converter Setup & Run
echo  For Dalmia Vidya Mandir Book Lists
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 📦 Checking required packages...
python -c "import pandas, openpyxl" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installing required packages...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
) else (
    echo ✅ Required packages already installed
)

echo.
echo 🚀 Running Excel to CSV converter...
echo.
python xlsx_to_csv_converter.py

echo.
echo 🏁 Process completed!
pause

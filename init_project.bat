@echo off
echo ===========================================
echo SMC Road Damage Management Platform Setup
echo ===========================================

REM Check if Python 3.11+ is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.11 or higher.
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo Python version: %PYTHON_VERSION%

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip
    pause
    exit /b 1
)
echo Pip upgraded

REM Install dependencies
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed

REM Create media directory
echo Creating media directory...
if not exist "media" mkdir media
echo Media directory created

REM Create staticfiles directory
echo Creating staticfiles directory...
if not exist "staticfiles" mkdir staticfiles
echo Staticfiles directory created

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Copying .env.example to .env...
    copy .env.example .env
    echo Environment file copied
    echo IMPORTANT: Please edit .env file with your database credentials
)

echo.
echo ===========================================
echo Initial Setup Complete!
echo ===========================================
echo.
echo Next steps:
echo 1. Edit .env file with your database settings
echo 2. Start PostgreSQL service if not running
echo 3. Run: python manage.py migrate
echo 4. Run: python manage.py load_initial_data
echo 5. Run: python manage.py createsuperuser
echo 6. Run: python manage.py runserver
echo.
echo For Docker setup: docker-compose up --build
echo.
echo Project is ready for development!
echo ===========================================
pause
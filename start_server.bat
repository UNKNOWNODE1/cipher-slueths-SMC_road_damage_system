@echo off
echo ===========================================
echo Starting SMC Road Damage Management Platform
echo ===========================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Please run init_project.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Redis Server (WSL)
echo Starting Redis server...
wsl sudo service redis-server start
echo Redis server started.

REM Check for database migrations
echo Checking for pending migrations...
python manage.py showmigrations | findstr "\[ \]" >nul
if not errorlevel 1 (
    echo Applying pending migrations...
    python manage.py migrate
) else (
    echo Database is up to date.
)

REM Start Celery Worker (in a new window)
echo Starting AI Engine (Celery Worker)...
start "SMC AI Engine" cmd /k "venv\Scripts\activate.bat && celery -A smc_platform worker --loglevel=info -P solo"

REM Start Django Development Server
echo Starting Web Server...
echo Access the dashboard at http://127.0.0.1:8000/
echo.
python manage.py runserver

pause

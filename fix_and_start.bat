@echo off
echo ========================================================
echo SMC Road Damage System - Comprehensive Fix and Start
echo ========================================================
echo.

REM Step 1: Kill any existing Python processes
echo [1/7] Stopping any existing servers...
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Found running Python processes. Stopping them...
    taskkill /F /IM python.exe >NUL 2>&1
    timeout /t 2 /nobreak >NUL
    echo Stopped.
) else (
    echo No existing servers found.
)
echo.

REM Step 2: Start Redis
echo [2/7] Starting Redis server in WSL...
wsl sudo service redis-server start
timeout /t 2 /nobreak >NUL
wsl redis-cli ping >NUL 2>&1
if %errorlevel% equ 0 (
    echo Redis is running.
) else (
    echo WARNING: Redis may not be running properly.
)
echo.

REM Step 3: Activate virtual environment
echo [3/7] Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run init_project.bat first.
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
echo Virtual environment activated.
echo.

REM Step 4: Make migrations
echo [4/7] Creating new migrations...
python manage.py makemigrations
echo.

REM Step 5: Apply migrations
echo [5/7] Applying database migrations...
python manage.py migrate
echo.

REM Step 6: Run health check
echo [6/7] Running system health check...
python health_check.py
echo.

REM Step 7: Start services
echo [7/7] Starting application services...
echo.
echo Starting Celery Worker in new window...
start "SMC AI Engine" cmd /k "cd /d "%CD%" && venv\Scripts\activate.bat && celery -A smc_platform worker --loglevel=info -P solo"
timeout /t 3 /nobreak >NUL

echo Starting Django Web Server...
echo.
echo ========================================================
echo Application is starting!
echo ========================================================
echo.
echo Access the dashboard at: http://127.0.0.1:8000/
echo.
echo Press Ctrl+C to stop the server
echo ========================================================
echo.

python manage.py runserver

pause

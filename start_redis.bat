@echo off
REM =====================================================
REM Start Redis Server (WSL)
REM =====================================================

echo Starting Redis server in WSL...
wsl sudo service redis-server start

REM Wait a moment for Redis to start
timeout /t 2 /nobreak >nul

REM Test Redis connection
echo Testing Redis connection...
wsl redis-cli ping

if %errorlevel% equ 0 (
    echo.
    echo [OK] Redis is running successfully!
    echo.
) else (
    echo.
    echo [ERROR] Redis failed to start
    echo.
)

pause

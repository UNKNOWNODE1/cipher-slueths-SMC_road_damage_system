@echo off
echo ============================================================
echo SMC Road Damage Management Platform - Quick Access Guide
echo ============================================================
echo.
echo Server Status: RUNNING at http://localhost:8000/
echo.
echo ============================================================
echo Access Points:
echo ============================================================
echo.
echo Homepage:
echo   http://localhost:8000/
echo.
echo Login Page:
echo   http://localhost:8000/accounts/login/
echo.
echo Admin Dashboard:
echo   http://localhost:8000/dashboard/admin/
echo.
echo Create New Report:
echo   http://localhost:8000/reports/create/
echo.
echo Django Admin:
echo   http://localhost:8000/admin/
echo.
echo API Documentation:
echo   http://localhost:8000/api/
echo.
echo ============================================================
echo Test Accounts:
echo ============================================================
echo.
echo Citizen Account:
echo   Username: test_citizen
echo   Password: testpass123
echo   Access: Create and track reports
echo.
echo Official Account:
echo   Username: test_official
echo   Password: testpass123
echo   Access: Manage assigned reports
echo.
echo Admin Account:
echo   Username: test_admin
echo   Password: testpass123
echo   Access: Full system control
echo.
echo ============================================================
echo Opening homepage in your default browser...
echo ============================================================
echo.
start http://localhost:8000/
echo.
echo Browser should open automatically. If not, copy this URL:
echo http://localhost:8000/
echo.
pause

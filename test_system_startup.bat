@echo off
REM System startup validation for SMC Road Damage Management Platform
REM Run from project root. Ensure venv is activated and USE_SQLITE=true for no-PostgreSQL dev.

echo ============================================================
echo SMC PLATFORM - SYSTEM STARTUP VALIDATION
echo ============================================================

echo.
echo [1/5] Checking Python syntax (key files)...
python -m py_compile smc_platform\settings.py 2>nul && echo   OK smc_platform/settings.py || echo   FAIL smc_platform/settings.py
python -m py_compile smc_platform\urls.py 2>nul && echo   OK smc_platform/urls.py || echo   FAIL smc_platform/urls.py
python -m py_compile reports\models.py 2>nul && echo   OK reports/models.py || echo   FAIL reports/models.py
python -m py_compile reports\views.py 2>nul && echo   OK reports/views.py || echo   FAIL reports/views.py
python -m py_compile api\views.py 2>nul && echo   OK api/views.py || echo   FAIL api/views.py
python -m py_compile manage.py 2>nul && echo   OK manage.py || echo   FAIL manage.py

echo.
echo [2/5] Django system check...
set USE_SQLITE=true
python manage.py check 2>nul && echo   OK Django check passed || echo   FAIL Run: pip install -r requirements.txt, then activate venv

echo.
echo [3/5] Database migration check...
python manage.py migrate --check 2>nul && echo   OK Migrations up to date || echo   INFO Run: python manage.py migrate

echo.
echo [4/5] Resolving URL routes...
python -c "import django; django.setup(); from django.urls import get_resolver; r=get_resolver(); print('   OK URL config loads'); list(r.url_patterns)" 2>nul || echo   FAIL URL check failed

echo.
echo [5/5] Static/media paths...
if exist "templates" (echo   OK templates/) else (echo   MISSING templates/)
if exist "static" (echo   OK static/) else (echo   MISSING static/)

echo.
echo ============================================================
echo Validation complete. Fix any FAIL items above.
echo To run server: set USE_SQLITE=true ^& python manage.py runserver
echo ============================================================

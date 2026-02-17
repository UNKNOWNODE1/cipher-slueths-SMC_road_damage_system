@echo off
echo ========================================
echo SMC Platform - Apply New Features
echo ========================================
echo.

echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 2: Creating database migrations...
python manage.py makemigrations contractors
python manage.py makemigrations reports
python manage.py makemigrations

echo.
echo Step 3: Applying migrations...
python manage.py migrate

echo.
echo Step 4: Creating static files...
python manage.py collectstatic --no-input

echo.
echo ========================================
echo Migration Complete!
echo ========================================
echo.
echo New Features Added:
echo  - Contractor Management System
echo  - AI-Based Repair Verification
echo  - Public Complaint Tracking
echo  - Email Notification System
echo  - SLA and Escalation Management
echo  - Advanced Severity Assessment
echo  - After-Repair Workflow
echo  - Ward-Based Auto-Routing
echo  - Background Task Automation
echo.
echo Next Steps:
echo  1. Configure email in .env file (optional)
echo  2. Start Celery worker: celery -A smc_platform worker -l info -P solo
echo  3. Start Celery beat: celery -A smc_platform beat -l info
echo  4. Start Django: python manage.py runserver
echo.
echo Public Tracking URL: http://127.0.0.1:8000/track/
echo.
pause

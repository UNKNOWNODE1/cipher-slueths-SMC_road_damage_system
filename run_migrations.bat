@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Creating migrations for contractors app...
python manage.py makemigrations contractors

echo.
echo Creating migrations for reports app...
python manage.py makemigrations reports

echo.
echo Creating all migrations...
python manage.py makemigrations

echo.
echo Applying migrations...
python manage.py migrate

echo.
echo Migrations complete!
pause

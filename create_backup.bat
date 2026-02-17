@echo off
call venv\Scripts\activate.bat
python manage.py dumpdata --indent 2 -o backup_before_features.json
echo Backup created successfully!

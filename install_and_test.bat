@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing AI dependencies (OpenCV, Pillow)...
pip install opencv-python pillow

echo.
echo Running migrations...
call run_migrations.bat

echo.
echo Setup Complete!
pause

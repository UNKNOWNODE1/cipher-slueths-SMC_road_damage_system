@echo off
echo Activating environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
python -m pip install requests opencv-python pillow

echo.
echo Setting up test image...
python setup_test_data.py

echo.
echo Running AI Analysis Verification...
python verify_pothole_analysis.py

echo.
echo Test Complete!
pause

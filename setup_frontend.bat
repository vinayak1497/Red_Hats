@echo off
echo Installing Attendance Anomaly System Dependencies...
echo.

echo Step 1: Installing Python packages...
pip install -r requirements.txt

echo.
echo Step 2: Installing additional frontend dependencies...
pip install streamlit plotly

echo.
echo Step 3: Creating outputs directory...
if not exist outputs mkdir outputs

echo.
echo Setup complete! Now you can run the frontend.
echo.
echo To start the web dashboard, run:
echo streamlit run dashboard.py
echo.
echo Then open your browser to: http://localhost:8501
echo.
pause

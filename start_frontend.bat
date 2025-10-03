@echo off
echo Starting Attendance Anomaly System Frontend...
echo.

echo Starting Streamlit web dashboard...
streamlit run dashboard.py

echo.
echo If the browser doesn't open automatically, go to:
echo http://localhost:8505
echo.
pause

@echo off
echo Starting Simplified Attendance Anomaly System...
echo.

& "C:\Users\manal\AppData\Local\Programs\Python\Python313\python.exe" -m streamlit run simple_dashboard.py --server.port 8506

echo.
echo If the browser doesn't open automatically, go to:
echo http://localhost:8506
echo.
pause

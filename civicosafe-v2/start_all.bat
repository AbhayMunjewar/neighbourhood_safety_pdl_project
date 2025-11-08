@echo off
echo Starting Civicosafe Application...
echo.
echo Starting Flask Backend (Terminal 1)...
start "Flask Backend" cmd /k "cd backend && python app.py"
timeout /t 3
echo.
echo Starting Frontend Server (Terminal 2)...
start "Frontend Server" cmd /k "cd civicosafe\civicosafe && python -m http.server 5500"
timeout /t 2
echo.
echo Both servers are starting!
echo.
echo Open your browser to: http://localhost:5500/login.html
echo.
pause


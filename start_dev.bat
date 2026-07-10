@echo off
echo ==========================================
echo   STARTING JOBHUNTERAI V12 DEV STACK
echo ==========================================
echo.

:: Start the Python FastAPI backend server in a new window
echo Starting FastAPI Backend on port 8000...
start "JobHunterAI Backend API" cmd /k "cd JobHunterAI && python api.py"

:: Start the Next.js Frontend dev server in a new window
echo Starting Next.js Frontend on port 3000...
start "JobHunterAI Frontend App" cmd /k "cd frontend && npm run dev"

echo.
echo ==========================================
echo   Services triggered successfully!
echo   - Backend: http://localhost:8000
echo   - Frontend: http://localhost:3000
echo ==========================================
pause

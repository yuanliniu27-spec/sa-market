@echo off
echo Starting SA Market...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Copy .env.example to .env if not exists
if not exist backend\.env (
    echo Creating backend\.env from backend\.env.example...
    copy backend\.env.example backend\.env
    echo Please edit backend\.env with your configuration before continuing.
    pause
)

REM Start services
echo Starting Docker containers...
docker-compose up -d

echo.
echo SA Market is starting!
echo.
echo Services:
echo   - Frontend:        http://localhost:3000
echo   - Backend API:     http://localhost:8000
echo   - API Docs:        http://localhost:8000/docs
echo   - MinIO Console:   http://localhost:9001
echo   - PostgreSQL:      localhost:5432
echo   - Redis:           localhost:6379
echo.
echo View logs:
echo   docker-compose logs -f
echo.
echo Stop services:
echo   docker-compose down
echo.
pause

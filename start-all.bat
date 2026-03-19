@echo off
echo ================================================
echo SA Market - 一键启动（无需 Docker）
echo ================================================
echo.
echo 正在启动后端和前端服务...
echo 请等待几秒钟...
echo.

REM 启动后端（在新窗口）
start "SA Market Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM 等待 3 秒
timeout /t 3 /nobreak >nul

REM 启动前端（在新窗口）
start "SA Market Frontend" cmd /k "cd /d %~dp0frontend && npm start"

echo.
echo ================================================
echo 服务正在启动...
echo.
echo 前端: http://localhost:3000
echo 后端: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 两个窗口会自动打开，请不要关闭
echo ================================================
echo.
pause

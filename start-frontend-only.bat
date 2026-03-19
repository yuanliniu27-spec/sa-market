@echo off
echo ========================================
echo SA Market - 前端启动脚本（无 Docker）
echo ========================================
echo.

REM 检查 Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Node.js 未安装！
    echo 请访问 https://nodejs.org/ 下载安装
    pause
    exit /b 1
)

echo [1/3] 检查环境...
cd /d "%~dp0frontend"

REM 安装依赖
if not exist node_modules (
    echo [2/3] 安装依赖（首次运行需要几分钟）...
    call npm install
) else (
    echo [2/3] 依赖已安装
)

REM 启动前端
echo [3/3] 启动前端服务...
echo.
echo ========================================
echo 前端服务启动中...
echo 访问地址: http://localhost:3000
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

call npm start

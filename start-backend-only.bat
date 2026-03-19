@echo off
echo ========================================
echo SA Market - 手动启动脚本（无 Docker）
echo ========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Python 未安装！请先安装 Python 3.11+
    pause
    exit /b 1
)

echo [1/5] 检查环境...
cd /d "%~dp0backend"

REM 创建虚拟环境
if not exist venv (
    echo [2/5] 创建虚拟环境...
    python -m venv venv
) else (
    echo [2/5] 虚拟环境已存在
)

REM 激活虚拟环境并安装依赖
echo [3/5] 安装依赖...
call venv\Scripts\activate.bat
pip install -q -r requirements.txt

REM 创建 .env 文件（如果不存在）
if not exist .env (
    echo [4/5] 创建配置文件...
    copy .env.example .env
    echo.
    echo [警告] 请编辑 backend\.env 文件，配置数据库连接
    echo DATABASE_URL=sqlite:///./samarket.db  (使用 SQLite 简化)
    echo.
    pause
)

REM 启动后端服务
echo [5/5] 启动后端服务...
echo.
echo ========================================
echo 后端服务启动中...
echo 访问地址: http://localhost:8000
echo API 文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

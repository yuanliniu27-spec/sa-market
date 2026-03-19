# SA Market 无 Docker 启动指南

## 问题：Docker 未安装

您的系统上没有安装 Docker，但没关系！我已经为您创建了无需 Docker 的启动方案。

---

## ✅ 快速启动方案（推荐）

### 步骤 1：启动后端服务

打开 **命令提示符** 或 **PowerShell**，执行：

```cmd
cd C:\Users\niuyuanli\sa-market
start-backend-only.bat
```

**首次运行会：**
- 创建 Python 虚拟环境
- 安装所有依赖（需要 2-3 分钟）
- 使用 SQLite 数据库（无需安装 PostgreSQL）
- 启动后端服务

**成功后会显示：**
```
后端服务启动中...
访问地址: http://localhost:8000
API 文档: http://localhost:8000/docs
```

### 步骤 2：启动前端服务

**打开新的命令提示符窗口**，执行：

```cmd
cd C:\Users\niuyuanli\sa-market
start-frontend-only.bat
```

**首次运行会：**
- 安装 Node.js 依赖（需要 3-5 分钟）
- 启动前端开发服务器

**成功后会自动打开浏览器：**
- 前端地址：http://localhost:3000

---

## 🎯 访问地址

| 服务 | 地址 |
|------|------|
| **前端应用** | http://localhost:3000 |
| **后端 API** | http://localhost:8000 |
| **API 文档** | http://localhost:8000/docs |

---

## ⚠️ 可能遇到的问题

### 问题 1：后端启动失败

**症状：** 提示 "ModuleNotFoundError" 或 "No module named..."

**解决：**
```cmd
cd C:\Users\niuyuanli\sa-market\backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 问题 2：前端启动失败

**症状：** 提示 "Node.js 未安装"

**解决：**
1. 下载 Node.js：https://nodejs.org/
2. 安装 LTS 版本（推荐 18.x 或 20.x）
3. 重新运行 `start-frontend-only.bat`

### 问题 3：端口被占用

**症状：** "Error: Port 8000 is already in use"

**解决：**
```cmd
# 查找占用端口的进程
netstat -ano | findstr :8000

# 结束进程
taskkill /PID <进程ID> /F
```

### 问题 4：数据库未初始化

**症状：** 访问 API 时报错 "no such table"

**解决：**
```cmd
cd C:\Users\niuyuanli\sa-market\backend
venv\Scripts\activate

# 初始化 Alembic
alembic init alembic

# 编辑 alembic/env.py，添加：
# from app.core.database import Base
# from app.models import *
# target_metadata = Base.metadata

# 创建迁移
alembic revision --autogenerate -m "Initial schema"

# 应用迁移
alembic upgrade head
```

---

## 🔧 配置说明

### 后端配置

文件：`backend/.env`

已使用 SQLite 简化配置：
```env
DATABASE_URL=sqlite:///./samarket.db
```

**如果您有 PostgreSQL**，可以改为：
```env
DATABASE_URL=postgresql://用户名:密码@localhost:5432/samarket
```

### 前端配置

文件：`frontend/.env`（可选，默认配置已够用）

```env
REACT_APP_API_URL=http://localhost:8000
```

---

## 📝 简化版功能说明

由于没有使用 Docker，以下功能受限：

| 功能 | 状态 | 说明 |
|------|------|------|
| **应用浏览** | ✅ 完全可用 | |
| **应用创建** | ✅ 完全可用 | |
| **API 文档** | ✅ 完全可用 | |
| **文件上传** | ⚠️ 受限 | 需要配置 MinIO 或使用本地存储 |
| **自动审核** | ✅ 部分可用 | 代码扫描功能正常 |
| **Redis 缓存** | ❌ 不可用 | 不影响核心功能 |

---

## 🚀 下一步

启动成功后，您可以：

1. **访问前端**：http://localhost:3000
2. **查看 API 文档**：http://localhost:8000/docs
3. **测试创建应用**：使用 Swagger UI 测试 API

---

## 💡 建议

**如果您经常需要使用：**
- 建议安装 Docker Desktop（一次安装，终身受益）
- 可以获得完整功能体验
- 更接近生产环境

**如果只是临时测试：**
- 当前的手动启动方式完全够用
- SQLite 数据库足够满足开发需求

---

## 🆘 需要帮助？

如果启动过程中遇到任何问题：

1. 查看错误信息
2. 检查端口是否被占用
3. 确认 Python 和 Node.js 已正确安装
4. 告诉我具体的错误信息，我会帮您解决！

---

**现在可以尝试启动了！** 🎉

```cmd
# 打开两个命令提示符窗口

# 窗口1：启动后端
cd C:\Users\niuyuanli\sa-market
start-backend-only.bat

# 窗口2：启动前端
cd C:\Users\niuyuanli\sa-market
start-frontend-only.bat
```

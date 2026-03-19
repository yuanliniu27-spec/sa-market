# SA Market 快速启动指南

## ⚡ 5 分钟快速体验

### 前置要求

- ✅ Docker Desktop 已安装并运行
- ✅ 有网络连接（用于下载镜像）

### 步骤

#### 1. 进入项目目录

```bash
cd C:\Users\niuyuanli\sa-market
```

#### 2. 启动服务

**Windows 用户：**
```cmd
start.bat
```

**Linux/Mac 用户：**
```bash
chmod +x start.sh
./start.sh
```

#### 3. 等待服务启动（约 2-3 分钟）

查看日志：
```bash
docker-compose logs -f
```

看到以下输出表示启动成功：
```
backend_1   | INFO: Uvicorn running on http://0.0.0.0:8000
frontend_1  | Compiled successfully!
```

#### 4. 访问应用

打开浏览器访问：
- **前端**: http://localhost:3000
- **API 文档**: http://localhost:8000/docs

---

## 🎯 完整体验流程

### Step 1: 初始化数据库

```bash
cd backend

# 创建虚拟环境（首次运行）
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 初始化 Alembic
alembic init alembic
```

**编辑 `alembic/env.py`**，在文件顶部添加：
```python
from app.core.database import Base
from app.models import *

target_metadata = Base.metadata
```

**创建并应用迁移：**
```bash
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### Step 2: 创建演示数据

使用 API 文档创建测试应用：

1. 访问 http://localhost:8000/docs
2. 找到 `POST /api/v1/applications/` 端点
3. 点击 "Try it out"
4. 填入测试数据：

```json
{
  "name": "test-skill",
  "display_name": "测试 Skill",
  "description": "这是一个测试应用",
  "category": "客户管理",
  "type": "skill"
}
```

5. 点击 "Execute"

### Step 3: 上传应用包

#### 准备测试包

```bash
cd C:\Users\niuyuanli\sa-market\examples\demo-skill

# 创建 zip 包
# Windows: 右键 → 发送到 → 压缩文件夹
# Linux/Mac: zip -r demo-skill.zip .
```

#### 上传

1. 访问 http://localhost:3000/publish
2. 填写基本信息
3. 上传 `demo-skill.zip`
4. 查看审核进度

### Step 4: 浏览和安装

1. 返回首页 http://localhost:3000
2. 查看应用列表
3. 点击应用卡片进入详情
4. 点击"一键安装"

---

## 🔍 常见问题排查

### 问题1：端口被占用

**症状：** `Error: Port 3000 is already in use`

**解决：**
```bash
# 查找占用端口的进程
# Windows
netstat -ano | findstr :3000
taskkill /PID <进程ID> /F

# Linux/Mac
lsof -i :3000
kill -9 <进程ID>
```

### 问题2：Docker 服务未启动

**症状：** `Cannot connect to the Docker daemon`

**解决：**
- Windows: 启动 Docker Desktop
- Linux: `sudo systemctl start docker`

### 问题3：数据库连接失败

**症状：** `Connection refused` 或 `Could not connect to database`

**检查：**
```bash
# 确认 PostgreSQL 容器运行中
docker-compose ps

# 查看 PostgreSQL 日志
docker-compose logs postgres

# 重启服务
docker-compose restart postgres backend
```

### 问题4：MinIO 上传失败

**症状：** `Failed to upload file`

**解决：**
```bash
# 访问 MinIO 控制台
# http://localhost:9001
# 用户名: minioadmin
# 密码: minioadmin

# 确认 bucket 存在
# 如果不存在，创建名为 "sa-market" 的 bucket
```

### 问题5：前端显示空白

**症状：** 页面加载但无内容

**检查：**
```bash
# 检查后端 API 是否可访问
curl http://localhost:8000/health

# 查看浏览器控制台错误
# F12 → Console 标签

# 检查 API 地址配置
# frontend/.env 中的 REACT_APP_API_URL
```

---

## 🛑 停止服务

```bash
docker-compose down
```

**清理所有数据（包括数据库）：**
```bash
docker-compose down -v
```

---

## 🔄 重启服务

```bash
docker-compose restart
```

**仅重启特定服务：**
```bash
docker-compose restart backend
docker-compose restart frontend
```

---

## 📊 查看日志

**所有服务：**
```bash
docker-compose logs -f
```

**特定服务：**
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

---

## 🔧 开发模式

### 后端开发

```bash
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 前端开发

```bash
cd frontend
npm start
```

**特点：**
- ✅ 热重载（代码修改自动生效）
- ✅ 详细错误提示
- ✅ 源码映射（方便调试）

---

## 📝 配置说明

### 环境变量（backend/.env）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | `postgresql://...` |
| `REDIS_URL` | Redis 连接字符串 | `redis://localhost:6379/0` |
| `MINIO_ENDPOINT` | MinIO 地址 | `localhost:9000` |
| `MINIO_ACCESS_KEY` | MinIO 访问密钥 | `minioadmin` |
| `MINIO_SECRET_KEY` | MinIO 密钥 | `minioadmin` |
| `FEISHU_APP_ID` | 飞书应用 ID | (需配置) |
| `FEISHU_APP_SECRET` | 飞书应用密钥 | (需配置) |

---

## ✅ 验证安装

运行以下命令验证所有服务正常：

```bash
# 健康检查
curl http://localhost:8000/health

# 前端访问
curl http://localhost:3000

# 数据库连接
docker-compose exec postgres psql -U postgres -d samarket -c "SELECT 1;"

# Redis 连接
docker-compose exec redis redis-cli PING
```

**预期输出：**
```json
{"status":"ok"}           # 后端健康
<!DOCTYPE html>           # 前端页面
 ?column?
----------
        1               # 数据库正常
PONG                    # Redis 正常
```

---

## 🎓 学习资源

- **FastAPI 文档**: https://fastapi.tiangolo.com/
- **React 文档**: https://react.dev/
- **Ant Design**: https://ant.design/
- **Docker Compose**: https://docs.docker.com/compose/

---

## 🆘 获取帮助

遇到问题？

1. 查看 `PROJECT_SUMMARY.md` 中的常见问题
2. 检查 Docker 日志：`docker-compose logs -f`
3. 访问 API 文档：http://localhost:8000/docs
4. 联系团队：飞书群「市场营销-营销系统」

---

**祝使用愉快！🎉**

# SA Market - SalesAgent 应用市场

零售门店汽车销售专家的内部应用市场，支持团队成员发布、审核、下载并安装 Agent/Skill 到 SalesAgent 系统中使用。

## 功能特性

✅ **应用管理**
- Agent/Skill 发布与审核
- 版本管理
- 分类与搜索

✅ **自动审核引擎**
- 安全代码扫描
- 元数据完整性校验
- 依赖关系检查
- 功能测试

✅ **一键安装**
- 与 SalesAgent 系统深度集成
- 自动注册到 Skill 注册中心
- 使用统计同步

✅ **用户体验**
- 响应式界面设计
- 实时审核进度追踪
- 评分与评价系统

## 技术栈

**后端：**
- FastAPI (Python 3.11+)
- PostgreSQL 15+
- Redis 7.0+
- MinIO (对象存储)
- SQLAlchemy ORM

**前端：**
- React 18 + TypeScript
- Ant Design 5
- Zustand (状态管理)
- ECharts (数据可视化)

## 快速开始

### 前置要求

- Docker & Docker Compose
- Node.js 18+ (前端开发)
- Python 3.11+ (后端开发)

### 使用 Docker Compose（推荐）

1. **克隆项目**

```bash
cd sa-market
```

2. **配置环境变量**

```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env 文件，配置必要的参数
```

3. **启动所有服务**

```bash
docker-compose up -d
```

服务启动后：
- 前端：http://localhost:3000
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs
- MinIO 控制台：http://localhost:9001

### 本地开发

#### 后端开发

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动数据库（使用 docker-compose 中的服务）
docker-compose up -d postgres redis minio

# 运行数据库迁移
alembic upgrade head

# 启动开发服务器
uvicorn app.main:app --reload
```

#### 前端开发

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm start
```

## 项目结构

```
sa-market/
├── backend/                 # 后端服务
│   ├── app/
│   │   ├── api/            # API 路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # 业务逻辑
│   │   │   └── audit/      # 审核引擎
│   │   └── main.py         # FastAPI 应用入口
│   ├── tests/              # 测试
│   └── requirements.txt    # Python 依赖
├── frontend/                # 前端应用
│   ├── src/
│   │   ├── api/            # API 客户端
│   │   ├── components/     # React 组件
│   │   ├── pages/          # 页面组件
│   │   ├── store/          # Zustand 状态管理
│   │   └── App.tsx         # 应用入口
│   └── package.json        # Node.js 依赖
├── docker-compose.yml      # Docker Compose 配置
└── README.md               # 项目文档
```

## API 文档

启动后端服务后，访问：http://localhost:8000/docs

自动生成的 Swagger UI 文档，包含所有 API 端点的详细说明。

## 核心功能

### 1. 应用发布流程

```
上传 .zip 代码包
    ↓
自动审核（4 项检查）
    ↓
人工审批
    ↓
发布上线
```

### 2. 审核引擎

- **安全扫描**：检测危险函数、硬编码密钥
- **元数据校验**：验证 manifest.json 完整性
- **依赖检查**：验证依赖项版本兼容性
- **功能测试**：Docker 沙箱环境测试

### 3. 一键安装

点击"一键安装"后，系统自动：
1. 调用 SalesAgent API 注册 Skill
2. 更新安装统计
3. 用户的 SalesAgent 自动启用

## 数据库迁移

```bash
cd backend

# 创建新的迁移
alembic revision --autogenerate -m "描述变更"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 测试

```bash
# 后端测试
cd backend
pytest

# 前端测试
cd frontend
npm test
```

## 部署

### 生产环境部署

1. **配置环境变量**

编辑 `backend/.env`，设置生产环境配置：
- 数据库连接字符串
- Redis URL
- MinIO 配置
- 飞书 App ID 和 Secret
- SalesAgent API Token

2. **构建镜像**

```bash
docker-compose build
```

3. **启动服务**

```bash
docker-compose up -d
```

4. **Nginx 反向代理**

配置 Nginx 作为反向代理，处理 HTTPS 和负载均衡。

## 故障排查

### 后端服务无法启动

- 检查数据库连接：`docker-compose logs postgres`
- 检查 Redis 连接：`docker-compose logs redis`
- 查看后端日志：`docker-compose logs backend`

### 前端无法连接后端

- 检查 `frontend/.env` 中的 `REACT_APP_API_URL` 配置
- 确认后端服务正常运行：http://localhost:8000/health

### MinIO 上传失败

- 检查 MinIO 服务状态：`docker-compose logs minio`
- 确认 bucket 已创建
- 检查访问密钥配置

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交变更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

Copyright © 2026 Li Xiang Auto. All rights reserved.

## 联系方式

- 项目负责人：[您的姓名]
- 邮箱：[您的邮箱]
- 飞书群：市场营销-营销系统

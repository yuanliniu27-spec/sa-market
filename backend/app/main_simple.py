from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="SA Market API",
    version="1.0.0",
    debug=True
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://samarket.lixiang.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {
        "message": "SA Market API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/api/v1/applications/")
async def list_applications():
    """临时演示数据"""
    return {
        "data": [
            {
                "id": "1",
                "name": "customer-intent-demo",
                "display_name": "客户意向分析演示",
                "description": "这是一个演示用的客户意向分析 Skill",
                "type": "skill",
                "category": "客户管理",
                "icon_url": None,
                "publisher_name": "Demo User",
                "rating_avg": 4.8,
                "install_count": 125,
                "created_at": "2026-03-18T10:00:00"
            },
            {
                "id": "2",
                "name": "inventory-agent",
                "display_name": "库存管理助手",
                "description": "自动化库存查询、预测和预警",
                "type": "agent",
                "category": "供应链",
                "icon_url": None,
                "publisher_name": "Admin",
                "rating_avg": 4.9,
                "install_count": 89,
                "created_at": "2026-03-17T14:30:00"
            },
            {
                "id": "3",
                "name": "quote-calculator",
                "display_name": "智能报价计算",
                "description": "综合考虑多种因素生成最优报价方案",
                "type": "skill",
                "category": "营销工具",
                "icon_url": None,
                "publisher_name": "Marketing Team",
                "rating_avg": 4.7,
                "install_count": 201,
                "created_at": "2026-03-16T09:15:00"
            }
        ],
        "total": 3,
        "page": 1,
        "page_size": 20
    }


@app.get("/api/v1/applications/{app_id}")
async def get_application(app_id: str):
    """临时演示数据"""
    return {
        "id": app_id,
        "name": "customer-intent-demo",
        "display_name": "客户意向分析演示",
        "description": "这是一个演示用的客户意向分析 Skill，用于展示 SA Market 的完整功能。基于客户沟通记录、行为数据，自动评估客户购车意向度。",
        "type": "skill",
        "category": "客户管理",
        "tags": ["Demo", "CRM", "AI"],
        "icon_url": None,
        "publisher_id": "user1",
        "publisher_name": "Demo User",
        "publisher_dept": "市场营销-营销系统",
        "status": "approved",
        "current_version_id": "v1",
        "install_count": 125,
        "download_count": 230,
        "rating_avg": 4.8,
        "rating_count": 45,
        "created_at": "2026-03-18T10:00:00",
        "updated_at": "2026-03-18T10:00:00"
    }


@app.post("/api/v1/installations/install")
async def install_application(app_id: str):
    """临时演示功能"""
    return {
        "status": "success",
        "installation_id": "inst_001",
        "installed_at": "2026-03-18T15:00:00",
        "message": "安装成功！（演示版）"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

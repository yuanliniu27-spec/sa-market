from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import applications, versions, installations

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://samarket.lixiang.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(applications.router, prefix=f"{settings.API_V1_PREFIX}/applications", tags=["applications"])
app.include_router(versions.router, prefix=f"{settings.API_V1_PREFIX}/versions", tags=["versions"])
app.include_router(installations.router, prefix=f"{settings.API_V1_PREFIX}/installations", tags=["installations"])


@app.get("/")
async def root():
    return {
        "message": "SA Market API",
        "version": settings.APP_VERSION
    }


@app.get("/health")
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

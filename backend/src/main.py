"""
FastAPI 主程式
Jira Dashboard MVP v1.0 Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .api.routes import router
from .config import settings

# 建立 FastAPI 應用程式
app = FastAPI(
    title="Jira Dashboard API",
    description="Jira Dashboard MVP v1.0 - 提供 Dashboard 指標、狀態分布和 Sprint 篩選 API",
    version="1.0.0",
)

# 設定 CORS（允許前端存取）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Next.js 開發伺服器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """根路徑 - 健康檢查"""
    return {
        "message": "Jira Dashboard API v1.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy"}


if __name__ == "__main__":
    # 啟動伺服器
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,  # 開發模式自動重載
        log_level=settings.LOG_LEVEL.lower(),
    )

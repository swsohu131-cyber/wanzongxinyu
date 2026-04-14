"""
万宗心悟AI疗愈智能体 - FastAPI主应用
遵循白皮书六大核心原则设计
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from app.core.config import settings
from app.api.user.auth import router as user_auth_router
from app.api.user.dialogue import router as user_dialogue_router
from app.api.user.voice import router as user_voice_router
from app.api.admin.auth import router as admin_auth_router
from app.api.admin.management import router as admin_router
from app.api.admin.knowledge import router as knowledge_router

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
万宗心悟AI疗愈智能体 - 后端API服务

遵循白皮书六大核心原则：
1. 非传教原则
2. 文化尊重与逻辑一致原则
3. 正向疗愈原则
4. 隐私独立与跨时长记忆原则
5. 通俗适配与多模态一致原则
6. 三元融合原则

## API分层
- /user-api/* - 用户端API（需Token认证）
- /admin-api/* - 管理端API（需管理员Token认证）
    """
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_auth_router)
app.include_router(user_dialogue_router)
app.include_router(user_voice_router)
app.include_router(admin_auth_router)
app.include_router(admin_router)
app.include_router(knowledge_router)

# 静态文件服务（语音文件）
voices_dir = "/app/data/voices"
os.makedirs(voices_dir, exist_ok=True)
app.mount("/voices", StaticFiles(directory=voices_dir), name="voices")


@app.get("/", tags=["健康检查"])
async def root():
    """根路径 - 健康检查"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "六大原则": [
            "非传教原则",
            "文化尊重与逻辑一致原则",
            "正向疗愈原则",
            "隐私独立与跨时长记忆原则",
            "通俗适配与多模态一致原则",
            "三元融合原则"
        ]
    }


@app.get("/health", tags=["健康检查"])
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}


# 启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时执行"""
    from app.models.database import init_db
    init_db()
    print(f"{settings.APP_NAME} v{settings.APP_VERSION} 已启动")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )

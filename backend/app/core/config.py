"""
万宗心悟AI疗愈智能体 - 后端核心配置
"""
from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """应用配置"""

    # 应用信息
    APP_NAME: str = "万宗心悟AI疗愈智能体"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://wanzongxinyu:wanzongxinyu_secret_2024@localhost:5432/wanzongxinyu"
    )

    # Redis配置
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", "redis_secret_2024")

    # Qdrant向量数据库配置
    QDRANT_URL: str = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_COLLECTION_NAME: str = "knowledge_base"

    # MinIO对象存储配置
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minio_admin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minio_secret_2024")
    MINIO_BUCKET_VOICES: str = "voices"
    MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "False").lower() == "true"

    # JWT认证配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "wanzongxinyu_secret_key_change_in_production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # LLM配置
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")  # ollama / openai
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gemma3:4b")

    # Whisper语音识别配置
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "base")

    # Edge-TTS语音合成配置
    EDGE_TTS_VOICE: str = os.getenv("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural")

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

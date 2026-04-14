"""
万宗心悟AI疗愈智能体 - 记忆模块
管理用户短期记忆(Redis)和情节记忆(PostgreSQL)
"""
from typing import Any, Dict, List, Optional
from datetime import datetime
import json
import redis
import uuid

from sqlalchemy.orm import Session
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, JSONB, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

from app.models.database import User, UserProfile
from app.core.config import settings


# 记忆模块独立的Base（避免与主数据库模型冲突）
MemoryBase = declarative_base()


class EpisodicMemory(MemoryBase):
    """情节记忆表 - 永久存储重要事件"""
    __tablename__ = "episodic_memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_type = Column(String(50), nullable=False)  # conversation, insight, milestone, etc.
    content = Column(JSONB, default={})  # 记忆内容
    importance = Column(Integer, default=5)  # 重要性 1-10
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 索引
    __table_args__ = (
        UniqueConstraint("user_id", "event_type", "created_at", name="uq_episodic_event"),
    )


class MemoryService:
    """记忆服务 - Redis短期记忆 + PostgreSQL情节记忆"""

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
        self._redis_client = None

    @property
    def redis_client(self) -> redis.Redis:
        """懒加载Redis客户端"""
        if self._redis_client is None:
            # 解析REDIS_URL
            redis_url = settings.REDIS_URL
            if "://" in redis_url:
                # redis://host:port/db
                parts = redis_url.replace("redis://", "").split("/")
                host_port = parts[0].split(":")
                host = host_port[0]
                port = int(host_port[1]) if len(host_port) > 1 else 6379
                db = int(parts[1]) if len(parts) > 1 else 0
            else:
                host, port, db = "localhost", 6379, 0
            
            password = settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None
            
            self._redis_client = redis.Redis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True
            )
        return self._redis_client

    def _get_redis_key(self, key: str) -> str:
        """生成用户专属Redis键"""
        return f"wanzong:memory:{self.user.id}:{key}"

    async def store_short_term(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """
        短期记忆存储到Redis
        TTL默认1小时
        """
        try:
            redis_key = self._get_redis_key(key)
            # 序列化值
            json_value = json.dumps(value, ensure_ascii=False, default=str)
            self.redis_client.setex(redis_key, ttl, json_value)
            return True
        except Exception as e:
            print(f"Redis存储失败: {e}")
            return False

    async def get_short_term(self, key: str) -> Optional[Any]:
        """
        从Redis获取短期记忆
        """
        try:
            redis_key = self._get_redis_key(key)
            value = self.redis_client.get(redis_key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis获取失败: {e}")
            return None

    async def delete_short_term(self, key: str) -> bool:
        """删除短期记忆"""
        try:
            redis_key = self._get_redis_key(key)
            self.redis_client.delete(redis_key)
            return True
        except Exception as e:
            print(f"Redis删除失败: {e}")
            return False

    async def store_episodic(self, event_type: str, content: Dict, importance: int = 5) -> bool:
        """
        情节记忆永久存储到PostgreSQL
        """
        try:
            episodic = EpisodicMemory(
                user_id=self.user.id,
                event_type=event_type,
                content=content,
                importance=importance
            )
            self.db.add(episodic)
            self.db.commit()
            return True
        except Exception as e:
            print(f"情节记忆存储失败: {e}")
            self.db.rollback()
            return False

    async def get_episodic_memories(
        self, 
        event_type: Optional[str] = None, 
        limit: int = 50,
        min_importance: int = 1
    ) -> List[Dict]:
        """
        获取情节记忆
        """
        try:
            query = self.db.query(EpisodicMemory).filter(
                EpisodicMemory.user_id == self.user.id,
                EpisodicMemory.importance >= min_importance
            )
            
            if event_type:
                query = query.filter(EpisodicMemory.event_type == event_type)
            
            memories = query.order_by(
                EpisodicMemory.created_at.desc()
            ).limit(limit).all()
            
            return [
                {
                    "id": str(m.id),
                    "event_type": m.event_type,
                    "content": m.content,
                    "importance": m.importance,
                    "created_at": m.created_at.isoformat()
                }
                for m in memories
            ]
        except Exception as e:
            print(f"情节记忆获取失败: {e}")
            return []

    async def get_full_context(self) -> Dict[str, Any]:
        """
        获取用户完整上下文(短期+情节+用户画像)
        用于dialogue service构建LLM上下文
        """
        context = {
            "user_id": str(self.user.id),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # 获取用户画像
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == self.user.id
        ).first()
        
        if profile:
            context["profile"] = {
                "cultural_background": profile.cultural_background or {},
                "psychological_states": profile.psychological_states or [],
                "chat_patterns": profile.chat_patterns or {},
                "knowledge_weights": profile.knowledge_weights or {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
            }
        else:
            context["profile"] = {
                "cultural_background": {},
                "psychological_states": [],
                "chat_patterns": {},
                "knowledge_weights": {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
            }
        
        # 获取最近情节记忆
        context["episodic_memories"] = await self.get_episodic_memories(limit=20)
        
        # 获取短期记忆
        short_term_keys = [
            "current_topic", "recent_emotions", "active_concerns",
            "last_insight", "healing_progress"
        ]
        context["short_term"] = {}
        for key in short_term_keys:
            value = await self.get_short_term(key)
            if value is not None:
                context["short_term"][key] = value
        
        return context

    async def get_recent_memories(self, limit: int = 10) -> List[Dict]:
        """
        获取最近记忆片段（用于上下文构建）
        """
        # 获取最近的对话记忆
        episodic = await self.get_episodic_memories(
            event_type="conversation", 
            limit=limit
        )
        
        # 获取最新的短期记忆
        short_term_context = await self.get_short_term("recent_context")
        
        memories = []
        for mem in episodic:
            memories.append({
                "type": "episodic",
                "event_type": mem["event_type"],
                "content": mem["content"],
                "created_at": mem["created_at"]
            })
        
        if short_term_context:
            memories.append({
                "type": "short_term",
                "content": short_term_context,
                "created_at": datetime.utcnow().isoformat()
            })
        
        return memories[:limit]

    async def consolidate_memories(self) -> bool:
        """
        定期将短期记忆固化为情节记忆
        由定时任务调用
        """
        try:
            # 获取所有短期记忆键
            pattern = f"wanzong:memory:{self.user.id}:*"
            keys = self.redis_client.keys(pattern)
            
            for key in keys:
                # 提取原始键名
                original_key = key.replace(f"wanzong:memory:{self.user.id}:", "")
                
                # 跳过已标记为需要固化的键
                consolidate_key = f"{original_key}_to_consolidate"
                if self.redis_client.exists(f"wanzong:memory:{self.user.id}:{consolidate_key}"):
                    value = self.redis_client.get(key)
                    if value:
                        content = json.loads(value)
                        
                        # 存储为情节记忆
                        await self.store_episodic(
                            event_type=f"short_term_{original_key}",
                            content={original_key: content},
                            importance=5
                        )
                        
                        # 删除短期记忆
                        await self.delete_short_term(original_key)
                        self.redis_client.delete(f"wanzong:memory:{self.user.id}:{consolidate_key}")
            
            return True
        except Exception as e:
            print(f"记忆固化失败: {e}")
            return False

    async def update_healing_progress(self, insight: str, stage: str) -> bool:
        """
        更新疗愈进度
        """
        try:
            # 存储到情节记忆
            await self.store_episodic(
                event_type="healing_progress",
                content={"insight": insight, "stage": stage},
                importance=7
            )
            
            # 同时更新Redis中的进度
            current_progress = await self.get_short_term("healing_progress") or {}
            current_progress[stage] = {
                "insight": insight,
                "timestamp": datetime.utcnow().isoformat()
            }
            await self.store_short_term("healing_progress", current_progress, ttl=86400 * 30)  # 30天
            
            return True
        except Exception as e:
            print(f"疗愈进度更新失败: {e}")
            return False


def get_memory_service(db: Session, user: User) -> MemoryService:
    """获取记忆服务实例"""
    return MemoryService(db, user)

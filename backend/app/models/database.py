"""
万宗心悟AI疗愈智能体 - 数据库模型
遵循白皮书六大核心原则设计
"""
from sqlalchemy import create_engine, Column, String, Boolean, DateTime, Integer, Text, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import uuid

from app.core.config import settings

Base = declarative_base()

# 数据库引擎
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==================== 用户相关表 ====================

class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), unique=True, nullable=True, index=True)  # 手机号（唯一）
    email = Column(String(255), unique=True, nullable=True, index=True)  # 邮箱（唯一）
    nickname = Column(String(50), nullable=False)  # 自定义姓名/昵称
    created_at = Column(DateTime, default=datetime.utcnow)  # 注册时间
    last_login_at = Column(DateTime, nullable=True)  # 最后登录时间
    status = Column(String(20), default="active")  # 账号状态: active/suspended

    # 关系
    devices = relationship("UserDevice", back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.nickname}>"


class UserDevice(Base):
    """设备表 - 同源设备免密登录核心"""
    __tablename__ = "user_devices"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    device_fingerprint = Column(String(255), nullable=False)  # 设备指纹
    device_name = Column(String(100), nullable=True)  # 设备名称
    bound_at = Column(DateTime, default=datetime.utcnow)  # 绑定时间
    last_used_at = Column(DateTime, default=datetime.utcnow)  # 最后使用
    is_active = Column(Boolean, default=True)  # 是否激活

    # 同一用户同一设备唯一
    __table_args__ = (
        UniqueConstraint("user_id", "device_fingerprint", name="uq_user_device"),
        Index("idx_device_fingerprint", "device_fingerprint"),
    )

    # 关系
    user = relationship("User", back_populates="devices")

    def __repr__(self):
        return f"<UserDevice {self.device_name or self.device_fingerprint[:8]}>"


class AuthCode(Base):
    """验证码表 - 临时存储"""
    __tablename__ = "auth_codes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(20), nullable=True, index=True)
    email = Column(String(255), nullable=True, index=True)
    code = Column(String(6), nullable=False)  # 6位验证码
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)  # 过期时间
    used = Column(Boolean, default=False)  # 是否已使用

    def __repr__(self):
        return f"<AuthCode {self.code} to {self.phone or self.email}>"


# ==================== 对话相关表 ====================

class ChatSession(Base):
    """对话会话表"""
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    session_type = Column(String(20), default="text")  # text / voice
    started_at = Column(DateTime, default=datetime.utcnow)
    last_message_at = Column(DateTime, default=datetime.utcnow)
    message_count = Column(Integer, default=0)  # 消息数量
    is_archived = Column(Boolean, default=False)  # 是否归档

    # 关系
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_session_user_time", "user_id", "last_message_at"),
    )

    def __repr__(self):
        return f"<ChatSession {self.id}>"


class Message(Base):
    """消息表 - 永久存储核心"""
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 冗余但保证查询速度
    role = Column(String(10), nullable=False)  # user / assistant
    content = Column(Text, nullable=False)  # 文字内容
    content_type = Column(String(20), default="text")  # text / voice
    voice_url = Column(Text, nullable=True)  # 语音文件路径
    voice_duration = Column(Integer, nullable=True)  # 语音时长（秒）
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSONB, default={})  # 感知洞察数据 {情绪, 文化属性, 心理状态...}

    # 关系
    session = relationship("ChatSession", back_populates="messages")
    user = relationship("User", back_populates="messages")
    feedback = relationship("UserFeedback", back_populates="message", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_messages_session_time", "session_id", "created_at"),
        Index("idx_messages_user_time", "user_id", "created_at"),
    )

    def __repr__(self):
        return f"<Message {self.role} at {self.created_at}>"


class UserProfile(Base):
    """用户画像表 - 跨时长记忆核心"""
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    # 感知洞察结果
    cultural_background = Column(JSONB, default={})  # {国家, 民族, 语言, 文化倾向}
    cognitive_preferences = Column(JSONB, default={})  # {知识接受度, 表达习惯}
    psychological_states = Column(JSONB, default=[])  # [{时间, 状态, 症结类型}]
    chat_patterns = Column(JSONB, default={})  # {对话逻辑, 表达风格}
    healing_progress = Column(JSONB, default={})  # {疗愈进度, 关键节点}

    # 三元知识偏好权重
    knowledge_weights = Column(
        JSONB,
        default={"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
    )

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<UserProfile for {self.user_id}>"


class UserFeedback(Base):
    """用户反馈表 - 用于知识库学习"""
    __tablename__ = "user_feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_id = Column(UUID(as_uuid=True), ForeignKey("messages.id", ondelete="CASCADE"), nullable=False)
    feedback_type = Column(String(20))  # positive / negative / correction
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    user = relationship("User")
    message = relationship("Message", back_populates="feedback")

    def __repr__(self):
        return f"<UserFeedback {self.feedback_type}>"


# ==================== 管理端表 ====================

class Admin(Base):
    """公司管理员表"""
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="operator")  # super_admin / admin / operator
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Admin {self.username}>"


class DataAccessLog(Base):
    """数据访问日志 - 审计追踪"""
    __tablename__ = "data_access_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("admins.id", ondelete="SET NULL"), nullable=True)
    target_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    action = Column(String(50))  # view / export / delete
    details = Column(JSONB, default={})
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_access_log_time", "created_at"),
    )

    def __repr__(self):
        return f"<DataAccessLog {self.action}>"


class AuditLog(Base):
    """操作日志 - 不可删除"""
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    admin_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(50), nullable=False)
    details = Column(JSONB, default={})
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("idx_audit_log_time", "created_at"),
    )

    def __repr__(self):
        return f"<AuditLog {self.action}>"


# ==================== 初始化数据库 ====================

def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)

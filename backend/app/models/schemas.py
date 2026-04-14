"""
万宗心悟AI疗愈智能体 - Pydantic模型
用于API请求/响应数据验证
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# ==================== 用户相关 ====================

class UserBase(BaseModel):
    """用户基础模型"""
    nickname: str = Field(..., min_length=1, max_length=50)


class UserCreate(UserBase):
    """用户创建模型"""
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: UUID
    phone: Optional[str] = None
    email: Optional[str] = None
    created_at: datetime
    last_login_at: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """用户画像响应模型"""
    id: UUID
    user_id: UUID
    cultural_background: Dict[str, Any] = {}
    cognitive_preferences: Dict[str, Any] = {}
    psychological_states: List[Dict[str, Any]] = []
    chat_patterns: Dict[str, Any] = {}
    healing_progress: Dict[str, Any] = {}
    knowledge_weights: Dict[str, float] = {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 认证相关 ====================

class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None


class VerifyCodeRequest(BaseModel):
    """验证验证码请求"""
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    code: str = Field(..., min_length=6, max_length=6)
    nickname: str = Field(..., min_length=1, max_length=50)
    device_fingerprint: str


class DeviceLoginRequest(BaseModel):
    """设备免密登录请求"""
    device_fingerprint: str


class AuthResponse(BaseModel):
    """认证响应"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenPayload(BaseModel):
    """Token载荷"""
    sub: str  # user_id
    exp: datetime


# ==================== 消息相关 ====================

class MessageCreate(BaseModel):
    """消息创建模型"""
    content: str
    content_type: str = "text"  # text / voice
    voice_url: Optional[str] = None
    voice_duration: Optional[int] = None
    metadata: Dict[str, Any] = {}


class MessageResponse(BaseModel):
    """消息响应模型"""
    id: UUID
    session_id: UUID
    role: str
    content: str
    content_type: str
    voice_url: Optional[str] = None
    voice_duration: Optional[int] = None
    created_at: datetime
    metadata: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    """对话会话响应模型"""
    id: UUID
    user_id: UUID
    session_type: str
    started_at: datetime
    last_message_at: datetime
    message_count: int
    is_archived: bool
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True


class ConversationRequest(BaseModel):
    """对话请求模型"""
    content: str
    content_type: str = "text"
    voice_url: Optional[str] = None


class ConversationResponse(BaseModel):
    """对话响应模型"""
    message: MessageResponse
    updated_profile: Optional[UserProfileResponse] = None


# ==================== 反馈相关 ====================

class FeedbackCreate(BaseModel):
    """反馈创建模型"""
    message_id: UUID
    feedback_type: str  # positive / negative / correction
    content: Optional[str] = None


# ==================== 管理端相关 ====================

class AdminLoginRequest(BaseModel):
    """管理员登录请求"""
    username: str
    password: str


class AdminResponse(BaseModel):
    """管理员响应模型"""
    id: UUID
    username: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """用户列表响应"""
    users: List[UserResponse]
    total: int
    page: int
    page_size: int


class UserDetailResponse(BaseModel):
    """用户详情响应"""
    user: UserResponse
    profile: UserProfileResponse
    sessions: List[ChatSessionResponse]


class StatsResponse(BaseModel):
    """统计数据响应"""
    total_users: int
    active_users_today: int
    total_messages: int
    total_sessions: int
    avg_messages_per_user: float

"""
万宗心悟AI疗愈智能体 - 用户端对话API
遵循白皮书六大核心原则：
- 正向疗愈原则
- 通俗适配与多模态一致原则
- 三元融合原则
"""
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, User
from app.models.schemas import (
    ConversationRequest, ConversationResponse,
    MessageResponse, ChatSessionResponse,
    FeedbackCreate, UserProfileResponse
)
from app.services.dialogue import get_dialogue_service
from app.api.user.auth import get_current_user_from_token

router = APIRouter(prefix="/user-api", tags=["用户对话"])


@router.post("/conversation", response_model=ConversationResponse, summary="发送对话")
async def api_conversation(
    request: ConversationRequest,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    用户发送对话
    遵循白皮书：
    - 语音入语音出、文字入文字出
    - 全程逻辑连贯、文化适配
    """
    dialogue_service = get_dialogue_service(db, current_user)
    return dialogue_service.process_conversation(request)


@router.get("/history", response_model=List[MessageResponse], summary="获取对话历史")
async def api_get_history(
    session_id: Optional[UUID] = None,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    获取对话历史
    遵循白皮书：跨时长永久记忆，用户间隔多年登录后仍完整保留
    """
    dialogue_service = get_dialogue_service(db, current_user)
    return dialogue_service.get_conversation_history(session_id)


@router.get("/sessions", response_model=List[ChatSessionResponse], summary="获取会话列表")
async def api_get_sessions(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """获取用户所有会话列表"""
    from app.models.database import ChatSession

    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id,
        ChatSession.is_archived == False
    ).order_by(ChatSession.last_message_at.desc()).all()

    return [ChatSessionResponse.model_validate(s) for s in sessions]


@router.get("/profile", response_model=UserProfileResponse, summary="获取用户画像")
async def api_get_profile(
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    获取用户画像
    包含文化背景、心理状态、知识偏好等全部历史信息
    """
    from app.models.database import UserProfile

    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(status_code=404, detail="用户画像不存在")

    return UserProfileResponse.model_validate(profile)


@router.post("/feedback", summary="提交对话反馈")
async def api_submit_feedback(
    request: FeedbackCreate,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    提交对话反馈
    用于知识库学习和迭代优化
    """
    dialogue_service = get_dialogue_service(db, current_user)
    success = dialogue_service.submit_feedback(
        request.feedback_type,
        request.message_id,
        request.content
    )

    if not success:
        raise HTTPException(status_code=404, detail="消息不存在或无权反馈")

    return {"message": "反馈已提交"}

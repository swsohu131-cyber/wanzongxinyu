"""
万宗心悟AI疗愈智能体 - 管理端API
遵循白皮书：数据完全由公司掌控，用户端仅对话
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.database import (
    get_db, Admin, User, UserProfile, ChatSession, Message,
    DataAccessLog, AuditLog
)
from app.models.schemas import (
    UserListResponse, UserDetailResponse, UserResponse,
    ChatSessionResponse, UserProfileResponse, StatsResponse
)
from app.api.admin.auth import get_current_admin_from_token

router = APIRouter(prefix="/admin-api", tags=["管理端"])


def log_data_access(
    db: Session,
    admin: Admin,
    target_user_id: UUID,
    action: str,
    details: dict = None
):
    """记录数据访问日志"""
    access_log = DataAccessLog(
        admin_id=admin.id,
        target_user_id=target_user_id,
        action=action,
        details=details or {}
    )
    db.add(access_log)
    db.commit()


@router.get("/stats", response_model=StatsResponse, summary="获取统计数据")
async def get_stats(
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """获取全局统计数据"""
    # 总用户数
    total_users = db.query(func.count(User.id)).scalar()

    # 今日活跃用户
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    active_users_today = db.query(func.count(func.distinct(User.id))).filter(
        User.last_login_at >= today_start
    ).scalar()

    # 总消息数
    total_messages = db.query(func.count(Message.id)).scalar()

    # 总会话数
    total_sessions = db.query(func.count(ChatSession.id)).scalar()

    # 平均每用户消息数
    avg_messages_per_user = total_messages / total_users if total_users > 0 else 0

    return StatsResponse(
        total_users=total_users or 0,
        active_users_today=active_users_today or 0,
        total_messages=total_messages or 0,
        total_sessions=total_sessions or 0,
        avg_messages_per_user=round(avg_messages_per_user, 2)
    )


@router.get("/users", response_model=UserListResponse, summary="获取用户列表")
async def get_users(
    page: int = 1,
    page_size: int = 20,
    keyword: Optional[str] = None,
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """获取用户列表（分页）"""
    query = db.query(User)

    if keyword:
        query = query.filter(
            User.nickname.ilike(f"%{keyword}%") |
            User.phone.ilike(f"%{keyword}%") |
            User.email.ilike(f"%{keyword}%")
        )

    total = query.count()
    users = query.order_by(User.last_login_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    return UserListResponse(
        users=[UserResponse.model_validate(u) for u in users],
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/users/{user_id}", response_model=UserDetailResponse, summary="获取用户详情")
async def get_user_detail(
    user_id: UUID,
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """
    获取用户详细信息
    包含用户信息、用户画像、全部会话和消息
    """
    # 获取用户
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 记录数据访问
    log_data_access(db, current_admin, user_id, "view", {"action": "view_user_detail"})

    # 获取用户画像
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    # 获取所有会话
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == user_id
    ).order_by(ChatSession.last_message_at.desc()).all()

    return UserDetailResponse(
        user=UserResponse.model_validate(user),
        profile=UserProfileResponse.model_validate(profile) if profile else None,
        sessions=[ChatSessionResponse.model_validate(s) for s in sessions]
    )


@router.get("/users/{user_id}/messages", summary="获取用户消息历史")
async def get_user_messages(
    user_id: UUID,
    session_id: Optional[UUID] = None,
    limit: int = 100,
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """获取用户消息历史"""
    # 验证用户存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 记录数据访问
    log_data_access(db, current_admin, user_id, "export", {"action": "export_messages"})

    # 查询消息
    query = db.query(Message).filter(Message.user_id == user_id)

    if session_id:
        query = query.filter(Message.session_id == session_id)

    messages = query.order_by(Message.created_at.desc()).limit(limit).all()

    return {
        "user_id": str(user_id),
        "session_id": str(session_id) if session_id else None,
        "messages": messages,
        "total": len(messages)
    }


@router.post("/users/{user_id}/ban", summary="封禁用户")
async def ban_user(
    user_id: UUID,
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """封禁用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.status = "suspended"

    # 记录审计日志
    audit_log = AuditLog(
        admin_id=current_admin.id,
        target_user_id=user_id,
        action="ban_user",
        details={"admin_username": current_admin.username}
    )
    db.add(audit_log)
    db.commit()

    # 记录数据访问
    log_data_access(db, current_admin, user_id, "ban", {"action": "ban_user"})

    return {"message": "用户已封禁"}


@router.post("/users/{user_id}/unban", summary="解封用户")
async def unban_user(
    user_id: UUID,
    current_admin: Admin = Depends(get_current_admin_from_token),
    db: Session = Depends(get_db)
):
    """解封用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.status = "active"

    # 记录审计日志
    audit_log = AuditLog(
        admin_id=current_admin.id,
        target_user_id=user_id,
        action="unban_user",
        details={"admin_username": current_admin.username}
    )
    db.add(audit_log)
    db.commit()

    # 记录数据访问
    log_data_access(db, current_admin, user_id, "unban", {"action": "unban_user"})

    return {"message": "用户已解封"}

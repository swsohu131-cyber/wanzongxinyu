"""
万宗心悟AI疗愈智能体 - 用户端认证API
遵循白皮书：同源设备终身免密登录 + 跨时长永久记忆
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from app.models.database import get_db, User
from app.models.schemas import (
    SendCodeRequest, VerifyCodeRequest, DeviceLoginRequest,
    AuthResponse, UserResponse
)
from app.services.auth import send_verification_code, verify_and_login, device_auto_login, get_current_user

router = APIRouter(prefix="/user-api/auth", tags=["用户认证"])


def get_current_user_from_token(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """从Token获取当前用户"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")

    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)

    if not user:
        raise HTTPException(status_code=401, detail="令牌无效或已过期")

    return user


@router.post("/send-code", summary="发送验证码")
async def api_send_code(
    request: SendCodeRequest,
    db: Session = Depends(get_db)
):
    """发送验证码到手机或邮箱"""
    if not request.phone and not request.email:
        raise HTTPException(status_code=400, detail="请提供手机号或邮箱")

    code = send_verification_code(db, request)
    return {"message": "验证码已发送", "code": code}  # TODO: 生产环境移除code返回


@router.post("/verify", summary="验证验证码并登录")
async def api_verify_code(
    request: VerifyCodeRequest,
    db: Session = Depends(get_db)
):
    """验证验证码，完成注册或登录"""
    if not request.phone and not request.email:
        raise HTTPException(status_code=400, detail="请提供手机号或邮箱")

    if len(request.code) != 6:
        raise HTTPException(status_code=400, detail="验证码必须为6位")

    result = verify_and_login(db, request)

    if not result:
        raise HTTPException(status_code=400, detail="验证码无效或已过期")

    return result


@router.post("/device-login", summary="设备免密登录")
async def api_device_login(
    request: DeviceLoginRequest,
    db: Session = Depends(get_db)
):
    """
    设备免密登录
    遵循白皮书：同源设备终身免密登录
    无论间隔多久，使用同一台设备，无需任何验证
    """
    result = device_auto_login(db, request.device_fingerprint)

    if not result:
        raise HTTPException(status_code=404, detail="设备未绑定，请先注册登录")

    return result


@router.get("/me", summary="获取当前用户信息")
async def api_get_current_user(
    current_user: User = Depends(get_current_user_from_token)
):
    """获取当前登录用户信息"""
    return UserResponse.model_validate(current_user)

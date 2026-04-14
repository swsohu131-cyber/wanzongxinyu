"""
万宗心悟AI疗愈智能体 - 认证服务
遵循白皮书六大核心原则：隐私独立与跨时长记忆原则
"""
from datetime import datetime, timedelta
from typing import Optional
import random
import string

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.database import User, UserDevice, AuthCode, UserProfile, AuditLog
from app.models.schemas import SendCodeRequest, VerifyCodeRequest, DeviceLoginRequest, AuthResponse, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_code(length: int = 6) -> str:
    """生成随机验证码"""
    return "".join(random.choices(string.digits, k=length))


def hash_password(password: str) -> str:
    """哈希密码"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Optional[str]:
    """解码令牌，返回user_id"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def send_verification_code(db: Session, request: SendCodeRequest) -> str:
    """
    发送验证码
    遵循白皮书：用户数据绝对独立、永久存储
    """
    # 生成6位验证码
    code = generate_code()

    # 验证码30分钟有效
    expires_at = datetime.utcnow() + timedelta(minutes=30)

    # 存储验证码
    auth_code = AuthCode(
        phone=request.phone,
        email=request.email,
        code=code,
        expires_at=expires_at
    )
    db.add(auth_code)
    db.commit()

    # 实际发送验证码（这里仅为模拟，实际需要对接短信/邮件服务）
    # TODO: 对接真实短信/邮件服务
    print(f"[模拟] 验证码 {code} 已发送至 {request.phone or request.email}")

    return code


def verify_and_login(db: Session, request: VerifyCodeRequest) -> Optional[AuthResponse]:
    """
    验证验证码并登录
    遵循白皮书：
    - 首次注册：姓名+验证码
    - 同源设备：自动免密登录
    """
    # 查找有效验证码
    query = db.query(AuthCode).filter(
        AuthCode.used == False,
        AuthCode.expires_at > datetime.utcnow()
    )

    if request.phone:
        query = query.filter(AuthCode.phone == request.phone)
    else:
        query = query.filter(AuthCode.email == request.email)

    auth_code = query.order_by(AuthCode.created_at.desc()).first()

    if not auth_code or auth_code.code != request.code:
        return None

    # 标记验证码已使用
    auth_code.used = True

    # 查找或创建用户
    user = None
    if request.phone:
        user = db.query(User).filter(User.phone == request.phone).first()
    elif request.email:
        user = db.query(User).filter(User.email == request.email).first()

    is_new_user = False
    if not user:
        # 新用户注册
        is_new_user = True
        user = User(
            phone=request.phone,
            email=request.email,
            nickname=request.nickname,
            last_login_at=datetime.utcnow()
        )
        db.add(user)
        db.flush()

        # 创建用户画像
        profile = UserProfile(user_id=user.id)
        db.add(profile)
    else:
        # 老用户登录
        user.last_login_at = datetime.utcnow()
        user.nickname = request.nickname  # 更新昵称

    # 绑定设备
    device = db.query(UserDevice).filter(
        UserDevice.user_id == user.id,
        UserDevice.device_fingerprint == request.device_fingerprint
    ).first()

    if not device:
        device = UserDevice(
            user_id=user.id,
            device_fingerprint=request.device_fingerprint,
            last_used_at=datetime.utcnow()
        )
        db.add(device)
    else:
        device.last_used_at = datetime.utcnow()
        device.is_active = True

    # 记录审计日志
    audit_log = AuditLog(
        user_id=user.id,
        action="login" if not is_new_user else "register",
        details={"is_new_user": is_new_user, "device_fingerprint": request.device_fingerprint}
    )
    db.add(audit_log)

    db.commit()

    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


def device_auto_login(db: Session, device_fingerprint: str) -> Optional[AuthResponse]:
    """
    设备免密登录
    遵循白皮书：同源设备终身免密登录
    无论间隔1年、5年、10年甚至更久，使用同一台设备打开智能体，无需任何验证
    """
    # 查找已绑定的设备
    device = db.query(UserDevice).filter(
        UserDevice.device_fingerprint == device_fingerprint,
        UserDevice.is_active == True
    ).first()

    if not device:
        return None

    # 获取用户
    user = db.query(User).filter(User.id == device.user_id).first()
    if not user or user.status != "active":
        return None

    # 更新最后使用时间
    device.last_used_at = datetime.utcnow()
    user.last_login_at = datetime.utcnow()

    # 记录审计日志
    audit_log = AuditLog(
        user_id=user.id,
        action="device_auto_login",
        details={"device_fingerprint": device_fingerprint}
    )
    db.add(audit_log)

    db.commit()

    # 生成令牌
    access_token = create_access_token(data={"sub": str(user.id)})

    return AuthResponse(
        access_token=access_token,
        user=UserResponse.model_validate(user)
    )


def get_current_user(db: Session, token: str) -> Optional[User]:
    """获取当前用户"""
    user_id = decode_token(token)
    if not user_id:
        return None

    try:
        user_uuid = UUID(user_id)
        return db.query(User).filter(User.id == user_uuid).first()
    except (ValueError, TypeError):
        return None

"""
万宗心悟AI疗愈智能体 - 管理端认证API
遵循白皮书：数据完全由公司掌控
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.database import get_db, Admin
from app.models.schemas import AdminLoginRequest, AdminResponse
from app.services.auth import verify_password, hash_password, create_access_token, decode_token

router = APIRouter(prefix="/admin-api/auth", tags=["管理端认证"])


def get_current_admin_from_token(
    authorization: str = None,
    db: Session = Depends(get_db)
) -> Admin:
    """从Token获取当前管理员"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未授权")

    token = authorization.replace("Bearer ", "")
    admin_id = decode_token(token)

    if not admin_id:
        raise HTTPException(status_code=401, detail="令牌无效或已过期")

    try:
        admin_uuid = UUID(admin_id)
        admin = db.query(Admin).filter(Admin.id == admin_uuid).first()

        if not admin:
            raise HTTPException(status_code=401, detail="管理员不存在")

        return admin
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="令牌格式错误")


@router.post("/login")
async def admin_login(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """管理员登录"""
    admin = db.query(Admin).filter(Admin.username == request.username).first()

    if not admin or not verify_password(request.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    access_token = create_access_token(data={"sub": str(admin.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "admin": AdminResponse.model_validate(admin)
    }


@router.post("/register")
async def admin_register(
    request: AdminLoginRequest,
    db: Session = Depends(get_db)
):
    """注册新管理员"""
    existing = db.query(Admin).filter(Admin.username == request.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    admin = Admin(
        username=request.username,
        password_hash=hash_password(request.password),
        role="admin"
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    return AdminResponse.model_validate(admin)

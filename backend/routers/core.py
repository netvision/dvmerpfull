from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from auth import create_access_token, decode_token, verify_password
from database import get_db
from models import User, UserRole
from schemas import LoginIn, RefreshTokenIn, WebsiteAuthUserOut

router = APIRouter()


def _split_name(full_name: str) -> tuple[str, str]:
    parts = full_name.strip().split()
    if len(parts) <= 1:
        return parts[0] if parts else "", ""
    return parts[0], " ".join(parts[1:])


def _website_role(user: User) -> str:
    if user.role in {UserRole.hm, UserRole.principal, UserRole.super_admin}:
        return "admin"
    return "user"


@router.post("/core/auth/login")
def login(body: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email).first()
    if user is None or not verify_password(body.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    token = create_access_token(data={"sub": user.email, "iat": datetime.now(timezone.utc).timestamp()})
    first_name, last_name = _split_name(user.name)

    return {
        "success": True,
        "data": {
            "accessToken": token,
            "user": WebsiteAuthUserOut(
                id=user.id,
                email=user.email,
                first_name=first_name,
                last_name=last_name,
                role=_website_role(user),
                is_active=user.is_active,
            ).model_dump(),
        },
    }


@router.post("/core/auth/refresh")
def refresh(body: RefreshTokenIn, db: Session = Depends(get_db)):
    payload = decode_token(body.refreshToken)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = db.query(User).filter(User.email == email).first()
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    access_token = create_access_token(data={"sub": user.email})
    return {"success": True, "data": {"accessToken": access_token}}

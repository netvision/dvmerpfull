from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from audit import write_audit_log
from auth import create_access_token, decode_token, verify_password
from database import get_db
from limiter import limiter
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


def _client_ip(request: Request) -> str | None:
    return request.client.host if request.client else None


def _write_security_event(
    db: Session,
    *,
    request: Request,
    action: str,
    entity_id: str,
    actor_user_id: int | None = None,
    change_summary: str,
    payload: dict,
) -> None:
    write_audit_log(
        db,
        actor_user_id=actor_user_id,
        entity_type="security_event",
        entity_id=entity_id,
        action=action,
        change_summary=change_summary,
        after_payload=payload,
        ip_address=_client_ip(request),
    )


@router.post("/core/auth/login")
@limiter.limit("10/minute")
def login(body: LoginIn, request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == body.email.lower()).first()
    if user is None or not verify_password(body.password, user.hashed_password):
        _write_security_event(
            db,
            request=request,
            action="login_failed",
            entity_id=body.email,
            actor_user_id=user.id if user else None,
            change_summary="Core login failed: invalid credentials",
            payload={
                "email": body.email,
                "reason": "invalid_credentials",
            },
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    if not user.is_active:
        _write_security_event(
            db,
            request=request,
            action="login_blocked",
            entity_id=str(user.id),
            actor_user_id=user.id,
            change_summary="Core login blocked for inactive user",
            payload={
                "email": user.email,
                "reason": "inactive_user",
            },
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )

    token = create_access_token(data={"sub": user.email, "iat": datetime.now(timezone.utc).timestamp()})
    first_name, last_name = _split_name(user.name)

    _write_security_event(
        db,
        request=request,
        action="login_success",
        entity_id=str(user.id),
        actor_user_id=user.id,
        change_summary="Core user logged in successfully",
        payload={
            "email": user.email,
            "role": user.role.value,
        },
    )
    db.commit()

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
    if user.token_invalid_before is not None:
        issued_at = payload.get("iat")
        if issued_at is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
        token_invalid_before = user.token_invalid_before
        if token_invalid_before.tzinfo is None:
            token_invalid_before = token_invalid_before.replace(tzinfo=timezone.utc)
        if datetime.fromtimestamp(float(issued_at), timezone.utc) < token_invalid_before:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )

    access_token = create_access_token(data={"sub": user.email})
    return {"success": True, "data": {"accessToken": access_token}}

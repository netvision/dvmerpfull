import os
import sys

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "test-secret")

from auth import create_access_token
from database import Base, get_db
from limiter import limiter
from models import AuditLog, User, UserRole
from routers import core, portal, users


def _user(user_id: int, email: str, role: UserRole) -> User:
    return User(
        id=user_id,
        name=f"{role.value} User",
        email=email,
        hashed_password="x",
        role=role,
        is_active=True,
    )


def _auth(email: str) -> dict[str, str]:
    token = create_access_token({"sub": email})
    return {"Authorization": f"Bearer {token}"}


def _seed_users(session_factory) -> None:
    with session_factory() as db:
        db.add_all(
            [
                _user(1, "super@example.com", UserRole.super_admin),
                _user(2, "principal@example.com", UserRole.principal),
                _user(3, "admin@example.com", UserRole.admin),
                _user(4, "accounts@example.com", UserRole.accounts),
                _user(5, "teacher@example.com", UserRole.teacher),
            ]
        )
        db.commit()


def _make_client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    _seed_users(TestingSessionLocal)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.state.limiter = limiter
    app.include_router(users.router, prefix="/api/users")
    app.include_router(portal.router, prefix="/api/portal")
    app.include_router(core.router, prefix="/api/v1")
    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    client.db_session_factory = TestingSessionLocal
    client.engine = engine
    return client


def test_accounts_role_cannot_access_user_management_routes():
    client = _make_client()
    try:
        response = client.get("/api/users/", headers=_auth("accounts@example.com"))
        assert response.status_code == 403
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)


def test_non_super_admin_cannot_create_super_admin():
    client = _make_client()
    try:
        response = client.post(
            "/api/users/",
            headers=_auth("principal@example.com"),
            json={
                "name": "Escalated",
                "email": "escalated@example.com",
                "password": "secret123",
                "role": "super_admin",
            },
        )

        assert response.status_code == 403
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)


def test_non_super_admin_cannot_reset_super_admin_password():
    client = _make_client()
    try:
        response = client.post(
            "/api/users/1/reset-password",
            headers=_auth("principal@example.com"),
            json={"new_password": "secret123"},
        )

        assert response.status_code == 403
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)


def test_admin_can_still_create_normal_user_with_normalized_email():
    client = _make_client()
    try:
        response = client.post(
            "/api/users/",
            headers=_auth("admin@example.com"),
            json={
                "name": "New Teacher",
                "email": "NewTeacher@Example.COM",
                "password": "secret123",
                "role": "teacher",
            },
        )

        assert response.status_code == 201
        assert response.json()["email"] == "newteacher@example.com"
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)


def test_password_reset_invalidates_existing_user_tokens():
    client = _make_client()
    try:
        teacher_headers = _auth("teacher@example.com")

        response = client.post(
            "/api/users/5/reset-password",
            headers=_auth("admin@example.com"),
            json={"new_password": "secret123"},
        )
        assert response.status_code == 200

        response = client.get("/api/portal/auth/me", headers=teacher_headers)
        assert response.status_code == 401
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)


def test_core_login_failure_is_audited():
    client = _make_client()
    try:
        response = client.post(
            "/api/v1/core/auth/login",
            json={"email": "missing@example.com", "password": "wrong"},
        )

        assert response.status_code == 401
        with client.db_session_factory() as db:
            log = db.query(AuditLog).filter(AuditLog.action == "login_failed").one()
            assert log.entity_type == "security_event"
            assert log.entity_id == "missing@example.com"
    finally:
        client.close()
        Base.metadata.drop_all(bind=client.engine)

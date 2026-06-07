import io
import json
import os
import sys
import zipfile
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "test-secret")

from auth import create_access_token, get_current_user
from database import Base, get_db
from models import User, UserRole
from routers import portal


@pytest.fixture()
def client(tmp_path, monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    uploads_dir = tmp_path / "uploads"
    uploads_dir.mkdir()
    monkeypatch.setattr(portal, "UPLOADS_DIR", str(uploads_dir))

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_current_user():
        return User(
            id=999,
            name="Super Admin",
            email="super@example.com",
            hashed_password="x",
            role=UserRole.super_admin,
            is_active=True,
        )

    app = FastAPI()
    app.include_router(portal.router, prefix="/api/portal")
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user

    with TestClient(app) as test_client:
        test_client.db_session_factory = TestingSessionLocal
        test_client.uploads_dir = uploads_dir
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_backup_download_contains_database_rows_and_uploaded_assets(client):
    with client.db_session_factory() as db:
        db.add(
            User(
                id=1,
                name="Existing Teacher",
                email="teacher@example.com",
                hashed_password="x",
                role=UserRole.teacher,
                is_active=True,
            )
        )
        db.commit()

    (client.uploads_dir / "lesson.pdf").write_bytes(b"pdf-bytes")

    response = client.get("/api/portal/utilities/backup")

    assert response.status_code == 200
    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
        names = set(archive.namelist())
        assert "manifest.json" in names
        assert "database.json" in names
        assert "uploads/lesson.pdf" in names

        payload = json.loads(archive.read("database.json"))
        user_rows = payload["tables"]["users"]
        assert any(row["email"] == "teacher@example.com" for row in user_rows)
        assert archive.read("uploads/lesson.pdf") == b"pdf-bytes"


def test_restore_replaces_database_rows_and_uploaded_assets(client):
    with client.db_session_factory() as db:
        db.add(
            User(
                id=1,
                name="Original User",
                email="original@example.com",
                hashed_password="x",
                role=UserRole.teacher,
                is_active=True,
            )
        )
        db.commit()

    (client.uploads_dir / "old.pdf").write_bytes(b"old")
    backup = client.get("/api/portal/utilities/backup").content

    with client.db_session_factory() as db:
        db.query(User).delete()
        db.add(
            User(
                id=2,
                name="Changed User",
                email="changed@example.com",
                hashed_password="x",
                role=UserRole.teacher,
                is_active=True,
            )
        )
        db.commit()

    (client.uploads_dir / "old.pdf").unlink()
    (client.uploads_dir / "new.pdf").write_bytes(b"new")

    response = client.post(
        "/api/portal/utilities/restore",
        data={"confirm_restore": "RESTORE"},
        files={"file": ("backup.zip", backup, "application/zip")},
    )

    assert response.status_code == 200
    assert response.json()["restored_tables"] >= 1

    with client.db_session_factory() as db:
        emails = {user.email for user in db.query(User).all()}
        assert "original@example.com" in emails
        assert "changed@example.com" not in emails

    assert (client.uploads_dir / "old.pdf").read_bytes() == b"old"
    assert not (client.uploads_dir / "new.pdf").exists()


def test_restore_requires_super_admin(client, monkeypatch):
    def override_current_user():
        return User(
            id=998,
            name="Principal",
            email="principal@example.com",
            hashed_password="x",
            role=UserRole.principal,
            is_active=True,
        )

    client.app.dependency_overrides[get_current_user] = override_current_user

    response = client.post(
        "/api/portal/utilities/restore",
        data={"confirm_restore": "RESTORE"},
        files={"file": ("backup.zip", b"not-a-zip", "application/zip")},
    )

    assert response.status_code == 403


def test_restore_works_with_real_authenticated_user(tmp_path, monkeypatch):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    uploads_dir = tmp_path / "uploads"
    uploads_dir.mkdir()
    monkeypatch.setattr(portal, "UPLOADS_DIR", str(uploads_dir))

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(portal.router, prefix="/api/portal")
    app.dependency_overrides[get_db] = override_get_db

    with TestingSessionLocal() as db:
        db.add(
            User(
                id=1,
                name="Super Admin",
                email="super@example.com",
                hashed_password="x",
                role=UserRole.super_admin,
                is_active=True,
            )
        )
        db.commit()

    token = create_access_token({"sub": "super@example.com"})

    with TestClient(app) as authed_client:
        backup = authed_client.get(
            "/api/portal/utilities/backup",
            headers={"Authorization": f"Bearer {token}"},
        ).content
        response = authed_client.post(
            "/api/portal/utilities/restore",
            headers={"Authorization": f"Bearer {token}"},
            data={"confirm_restore": "RESTORE"},
            files={"file": ("backup.zip", backup, "application/zip")},
        )

    Base.metadata.drop_all(bind=engine)

    assert response.status_code == 200

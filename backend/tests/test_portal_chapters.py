import os
import sys

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("SECRET_KEY", "test-secret")

from auth import get_current_user
from database import Base, get_db
from models import Chapter, Class, Subject, User, UserRole
from routers import portal


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

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
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_chapter_detail_includes_order_index_for_edit_modal(client):
    with client.db_session_factory() as db:
        cls = Class(name="Class 6", display_order=1)
        subject = Subject(name="Mathematics", class_id=1)
        chapter = Chapter(title="Fractions", aim="Learn fractions", subject_id=1, order_index=7)
        db.add_all([cls, subject, chapter])
        db.commit()

    response = client.get("/api/portal/chapters/1")

    assert response.status_code == 200
    assert response.json()["order_index"] == 7


def test_xlsx_upload_endpoint_is_removed(client):
    response = client.post(
        "/api/portal/upload",
        data={"subject_id": "1"},
        files={
            "file": (
                "lesson.xlsx",
                b"placeholder",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        },
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Not Found"

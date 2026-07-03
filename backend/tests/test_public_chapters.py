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

from auth import create_access_token
from database import Base, get_db
from models import Chapter, Class, Subject, User, UserRole
from routers import public


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

    app = FastAPI()
    app.include_router(public.router, prefix="/api/public")
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        test_client.db_session_factory = TestingSessionLocal
        yield test_client

    Base.metadata.drop_all(bind=engine)


def test_public_chapter_detail_includes_order_index(client):
    with client.db_session_factory() as db:
        cls = Class(name="Class 6", display_order=1)
        subject = Subject(name="Mathematics", class_id=1)
        chapter = Chapter(title="Fractions", aim="Learn fractions", subject_id=1, order_index=7)
        user = User(
            name="Teacher",
            email="teacher@example.com",
            hashed_password="x",
            role=UserRole.teacher,
            is_active=True,
        )
        db.add_all([cls, subject, chapter, user])
        db.commit()

    token = create_access_token({"sub": "teacher@example.com"})
    response = client.get(
        "/api/public/chapters/1",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["order_index"] == 7


def test_public_chapter_detail_requires_authentication(client):
    response = client.get("/api/public/chapters/1")

    assert response.status_code == 401

import os
import sys
from datetime import date

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["AGENT_API_KEY"] = "test-agent-key"

from database import get_db
from models import Base, Department, StaffProfile, User, UserRole
from routers import agent


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
    app.include_router(agent.router, prefix="/api")
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        test_client.db_session_factory = TestingSessionLocal
        yield test_client

    Base.metadata.drop_all(bind=engine)


def _headers():
    return {"X-API-Key": "test-agent-key"}


def test_agent_staff_search_handles_staff_without_profile(client):
    with client.db_session_factory() as db:
        db.add(
            User(
                name="No Profile Teacher",
                email="noprof@example.com",
                hashed_password="x",
                role=UserRole.teacher,
                is_active=True,
            )
        )
        db.commit()

    response = client.get("/api/agent/staff", headers=_headers())

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["name"] == "No Profile Teacher"
    assert body["results"][0]["designation"] is None
    assert body["results"][0]["department"] is None


def test_agent_staff_search_uses_linked_department_name(client):
    with client.db_session_factory() as db:
        department = Department(name="Science", description="Science faculty")
        user = User(
            name="Anita Sharma",
            email="anita@example.com",
            hashed_password="x",
            role=UserRole.teacher,
            is_active=True,
        )
        db.add_all([department, user])
        db.flush()
        db.add(
            StaffProfile(
                user_id=user.id,
                department_id=department.id,
                designation="TGT",
                joining_date=date(2024, 4, 1),
            )
        )
        db.commit()

    response = client.get(
        "/api/agent/staff",
        params={"department": "Science"},
        headers=_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 1
    assert body["results"][0]["name"] == "Anita Sharma"
    assert body["results"][0]["department"] == "Science"

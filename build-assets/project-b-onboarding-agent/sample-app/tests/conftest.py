"""Shared test fixtures for TaskFlow API tests."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_taskflow.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def registered_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "securepassword123",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    return response.json()


@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "securepassword123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_project(client, auth_headers):
    response = client.post(
        "/api/projects/",
        json={"name": "Test Project", "description": "A test project", "slug": "test-project"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    return response.json()

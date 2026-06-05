"""Tests for authentication endpoints."""


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "new@example.com",
            "username": "newuser",
            "password": "password123",
            "full_name": "New User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert data["username"] == "newuser"
    assert "hashed_password" not in data


def test_register_duplicate_email(client, registered_user):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "username": "different",
            "password": "password123",
        },
    )
    assert response.status_code == 400


def test_login(client, registered_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "securepassword123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, registered_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_get_current_user(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_unauthorized_access(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401

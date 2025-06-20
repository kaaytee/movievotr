from fastapi.testclient import TestClient
from app.core.config import settings

def test_register_user(client: TestClient, test_db):
    response = client.post(
        f"{settings.API_URL}/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_existing_username(client: TestClient, test_db):
    client.post(
        f"{settings.API_URL}/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"},
    )
    response = client.post(
        f"{settings.API_URL}/register",
        json={"username": "testuser", "email": "another@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Username already registered"}


def test_register_existing_email(client: TestClient, test_db):
    client.post(
        f"{settings.API_URL}/register",
        json={"username": "testuser", "email": "test@example.com", "password": "testpassword"},
    )
    response = client.post(
        f"{settings.API_URL}/register",
        json={"username": "anotheruser", "email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_with_username(client: TestClient, test_db):
    user_payload = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post(f"{settings.API_URL}/register", json=user_payload)
    
    response = client.post(
        f"{settings.API_URL}/login?username_or_email={user_payload['username']}&password={user_payload['password']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_email(client: TestClient, test_db):
    user_payload = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post(f"{settings.API_URL}/register", json=user_payload)
    
    response = client.post(
        f"{settings.API_URL}/login?username_or_email={user_payload['email']}&password={user_payload['password']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient, test_db):
    user_payload = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post(f"{settings.API_URL}/register", json=user_payload)
    
    response = client.post(
        f"{settings.API_URL}/login?username_or_email={user_payload['username']}&password=wrongpassword"
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_get_current_user(client: TestClient, test_db):
    user_payload = {"username": "testuser", "email": "test@example.com", "password": "testpassword"}
    client.post(f"{settings.API_URL}/register", json=user_payload)
    
    login_response = client.post(
        f"{settings.API_URL}/login?username_or_email={user_payload['username']}&password={user_payload['password']}"
    )
    token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get(f"{settings.API_URL}/users/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_payload["username"]
    assert data["email"] == user_payload["email"]


def test_get_current_user_no_token(client: TestClient, test_db):
    response = client.get(f"{settings.API_URL}/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

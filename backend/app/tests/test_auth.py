import pytest
import sys
import os
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, root_dir)
sys.path.insert(0, app_dir)

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app.models.user import User
from app.core.security import get_password_hash

client = TestClient(app)

def test_register_user(db_session: Session):
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }

    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_register_duplicate_username(db_session: Session):
    # Create first user
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    client.post("/auth/register", json=user_data)

    # Try to create user with same username
    duplicate_data = {
        "username": "testuser",
        "email": "test2@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/register", json=duplicate_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_success(db_session: Session):
    # Register user first
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    client.post("/auth/register", json=user_data)

    # Login
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(db_session: Session):
    # Register user first
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    }
    client.post("/auth/register", json=user_data)

    # Try to login with wrong password
    login_data = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]
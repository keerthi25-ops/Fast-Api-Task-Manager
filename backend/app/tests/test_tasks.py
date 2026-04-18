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
from app.models.task import Task
from app.core.security import get_password_hash

client = TestClient(app)

def get_auth_token(db_session: Session):
    # Create a test user
    hashed_password = get_password_hash("testpassword")
    test_user = User(username="testuser", email="test@example.com", hashed_password=hashed_password)
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # Login to get token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=login_data)
    return response.json()["access_token"]

def test_create_task(db_session: Session):
    token = get_auth_token(db_session)

    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }

    response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == task_data["completed"]

def test_get_tasks(db_session: Session):
    token = get_auth_token(db_session)

    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )

    # Get tasks
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == task_data["title"]

def test_update_task(db_session: Session):
    token = get_auth_token(db_session)

    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "completed": True
    }
    response = client.put(
        f"/tasks/{task_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] == True

def test_delete_task(db_session: Session):
    token = get_auth_token(db_session)

    # Create a task first
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False
    }
    create_response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

    # Verify task is deleted
    get_response = client.get(
        f"/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert get_response.status_code == 404
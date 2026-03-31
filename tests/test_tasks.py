"""Tests for TaskFlow API."""

import pytest
from fastapi.testclient import TestClient

from taskflow.main import app
from taskflow.storage import storage


@pytest.fixture(autouse=True)
def reset_storage():
    storage._tasks.clear()
    storage._next_id = 1
    yield


client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_task():
    resp = client.post("/tasks", json={"title": "Write tests", "priority": "high"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["title"] == "Write tests"
    assert data["priority"] == "high"
    assert data["status"] == "todo"


def test_list_tasks_empty():
    resp = client.get("/tasks")
    assert resp.status_code == 200
    assert resp.json() == []


def test_list_tasks():
    client.post("/tasks", json={"title": "Task A"})
    client.post("/tasks", json={"title": "Task B"})
    resp = client.get("/tasks")
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task A"
    assert tasks[1]["title"] == "Task B"


def test_get_task():
    client.post("/tasks", json={"title": "Find me"})
    resp = client.get("/tasks/1")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Find me"


def test_get_task_not_found():
    resp = client.get("/tasks/999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Task not found"

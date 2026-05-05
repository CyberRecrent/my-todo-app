import pytest
import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"

from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["message"] == "Todo API is running"


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_get_todos_empty(client):
    res = client.get("/todos")
    assert res.status_code == 200
    assert res.get_json() == []


def test_create_todo(client):
    res = client.post("/todos", json={"title": "Learn Docker"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == "Learn Docker"
    assert data["done"] is False


def test_create_todo_no_title(client):
    res = client.post("/todos", json={})
    assert res.status_code == 400


def test_update_todo(client):
    client.post("/todos", json={"title": "Learn CI/CD"})
    res = client.patch("/todos/1", json={"done": True})
    assert res.status_code == 200
    assert res.get_json()["done"] is True


def test_update_todo_not_found(client):
    res = client.patch("/todos/999", json={"done": True})
    assert res.status_code == 404
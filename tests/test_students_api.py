import pytest

from app import create_app
from app.models import db


@pytest.fixture()
def app():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def create_student(client, name="Alice", age=21):
    return client.post("/api/v1/students", json={"name": name, "age": age})


def test_healthcheck_returns_healthy_status(client):
    response = client.get("/api/v1/healthcheck")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_create_student_returns_created_student(client):
    response = create_student(client)

    assert response.status_code == 201
    assert response.get_json() == {"id": 1, "name": "Alice", "age": 21}


def test_create_student_requires_name_and_age(client):
    response = client.post("/api/v1/students", json={"name": "Alice"})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Name and age are required"}


def test_list_students_returns_all_students(client):
    create_student(client, name="Alice", age=21)
    create_student(client, name="Bob", age=22)

    response = client.get("/api/v1/students")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "name": "Alice", "age": 21},
        {"id": 2, "name": "Bob", "age": 22},
    ]


def test_get_student_returns_student_by_id(client):
    create_student(client)

    response = client.get("/api/v1/students/1")

    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alice", "age": 21}


def test_get_student_returns_404_when_missing(client):
    response = client.get("/api/v1/students/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}


def test_update_student_changes_existing_student(client):
    create_student(client)

    response = client.put(
        "/api/v1/students/1", json={"name": "Alice Cooper", "age": 22}
    )

    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alice Cooper", "age": 22}


def test_update_student_rejects_empty_payload(client):
    create_student(client)

    response = client.put("/api/v1/students/1", json={})

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid JSON payload"}


def test_update_student_returns_404_when_missing(client):
    response = client.put("/api/v1/students/999", json={"name": "Alice"})

    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}


def test_delete_student_removes_existing_student(client):
    create_student(client)

    response = client.delete("/api/v1/students/1")

    assert response.status_code == 200
    assert response.get_json() == {"message": "Student deleted successfully"}

    get_response = client.get("/api/v1/students/1")
    assert get_response.status_code == 404


def test_delete_student_returns_404_when_missing(client):
    response = client.delete("/api/v1/students/999")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Student not found"}

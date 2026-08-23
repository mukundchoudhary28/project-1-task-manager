import uuid

from fastapi.testclient import TestClient
from sqlalchemy import select

from task_manager.main import app
from task_manager.models import Task, User


client = TestClient(app)


def test_create_task(auth_headers, db, test_user):
    task = {
        "name": "Test task",
        "description": "Created during automated testing",
        "completed": False,
    }

    response = client.post(
        "/tasks/",
        json=task,
        headers=auth_headers,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test task"
    assert data["description"] == "Created during automated testing"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data

    statement = select(Task).where(Task.name == "Test task")
    created_task = db.execute(statement).scalar_one_or_none()

    assert created_task is not None
    assert created_task.description == "Created during automated testing"
    assert created_task.completed is False
    assert created_task.user_id == test_user.id


def test_create_task_missing_name(auth_headers):
    task = {
        "description": "Created during automated testing without name",
        "completed": False,
    }

    response = client.post(
        "/tasks/",
        json=task,
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_get_tasks(db, auth_headers, test_user):
    task1 = Task(
        name="Task 1",
        description="First test task",
        completed=False,
        user_id=test_user.id,
    )

    task2 = Task(
        name="Task 2",
        description="Second test task",
        completed=True,
        user_id=test_user.id,
    )

    db.add_all([task1, task2])
    db.commit()

    response = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["name"] == "Task 1"
    assert data[1]["name"] == "Task 2"


def test_get_tasks_empty(auth_headers):
    response = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data == []


def test_get_task_by_id(test_task, auth_headers):
    response = client.get(
        f"/tasks/{test_task.id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_task.id)
    assert data["name"] == "Test task"


def test_get_task_not_found(auth_headers):
    task_id = uuid.uuid4()

    response = client.get(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_invalid_uuid(auth_headers):
    response = client.get(
        "/tasks/not-a-uuid",
        headers=auth_headers,
    )

    assert response.status_code == 422


def test_update_single_fields_task(test_task, auth_headers):
    update_data = {
        "completed": True
    }

    response = client.patch(
        f"/tasks/{test_task.id}",
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(test_task.id)
    assert data["name"] == "Test task"
    assert data["description"] == "Test task description"
    assert data["completed"] is True


def test_update_multiple_fields_task(test_task, auth_headers):
    update_data = {
        "name": "Updated Task Name",
        "completed": True,
    }

    response = client.patch(
        f"/tasks/{test_task.id}",
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated Task Name"
    assert data["completed"] is True


def test_update_task_not_found(auth_headers):
    task_id = uuid.uuid4()

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(db, test_task, auth_headers):
    response = client.delete(
        f"/tasks/{test_task.id}",
        headers=auth_headers,
    )

    assert response.status_code == 204

    statement = select(Task).where(Task.id == test_task.id)
    deleted_task = db.execute(statement).scalar_one_or_none()

    assert deleted_task is None


def test_delete_task_not_found(auth_headers):
    task_id = uuid.uuid4()

    response = client.delete(
        f"/tasks/{task_id}",
        headers=auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


#Authorization tests

def test_user_cannot_get_another_users_task(
    test_task,
    second_auth_headers,
):
    response = client.get(
        f"/tasks/{test_task.id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_user_cannot_update_another_users_task(
    test_task,
    second_auth_headers,
):
    response = client.patch(
        f"/tasks/{test_task.id}",
        json={"completed": True},
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_user_cannot_delete_another_users_task(
    test_task,
    second_auth_headers,
):
    response = client.delete(
        f"/tasks/{test_task.id}",
        headers=second_auth_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_user_only_sees_their_own_tasks(
    db,
    test_user,
    second_user,
    auth_headers,
    second_auth_headers,
):
    task_a = Task(
        name="User A Task",
        description="Belongs to User A",
        completed=False,
        user_id=test_user.id,
    )

    task_b = Task(
        name="User B Task",
        description="Belongs to User B",
        completed=False,
        user_id=second_user.id,
    )

    db.add_all([task_a, task_b])
    db.commit()

    response_a = client.get(
        "/tasks/",
        headers=auth_headers,
    )

    assert response_a.status_code == 200

    data_a = response_a.json()

    assert len(data_a) == 1
    assert data_a[0]["name"] == "User A Task"

    response_b = client.get(
        "/tasks/",
        headers=second_auth_headers,
    )

    assert response_b.status_code == 200

    data_b = response_b.json()

    assert len(data_b) == 1
    assert data_b[0]["name"] == "User B Task"
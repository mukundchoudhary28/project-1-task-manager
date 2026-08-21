from fastapi.testclient import TestClient
from task_manager.main import app
from task_manager.models import Task
from sqlalchemy import select

client = TestClient(app)


def test_create_task(db):
    task = {
        "name": "Test task",
        "description": "Created during automated testing",
        "completed": False,
    }

    response = client.post("/tasks/", json=task)

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



def test_create_task_missing_name(db):
    task  = {
        "description": "Created during automated testing without name",
        "completed": False,
    }
    response = client.post("/tasks/", json=task)
    assert response.status_code == 422


def test_get_tasks(db):
    task1 = Task(
        name="Task 1",
        description="First test task",
        completed=False,
    )

    task2 = Task(
        name="Task 2",
        description="Second test task",
        completed=True,
    )

    db.add_all([task1, task2])
    db.commit()

    response = client.get("/tasks/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Task 1"
    assert data[1]["name"] == "Task 2"


def test_get_tasks_empty():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert data == []


def test_get_task_by_id(db):
    task = Task(
        name = "Task for retrieval",
        description = "This task is created to test retrieval by ID",
        completed = False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    response = client.get(f"/tasks/{task.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(task.id)
    assert data["name"] == "Task for retrieval"


def test_get_task_not_found():
    import uuid
    task_id = uuid.uuid4()

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_get_task_invalid_uuid():
    response = client.get("/tasks/not-a-uuid")

    assert response.status_code == 422


def test_update_single_fields_task(db):
    task = Task(
        name="Task to update",
        description="This task will be updated",
        completed=False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    update_data = {
        "completed": True
    }

    response = client.patch(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()

    assert data["id"] == str(task.id)
    assert data["name"] == "Task to update"
    assert data["description"] == "This task will be updated"
    assert data["completed"] is True



def test_update_multiple_fields_task(db):
    task = Task(
        name="Task to update",
        description="This task will be updated",
        completed=False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    update_data = {
        "name": "Updated Task Name",
        "completed": True,
    }

    response = client.patch(f"/tasks/{task.id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Task Name"
    assert data["completed"] is True


def test_update_task_not_found():
    import uuid

    task_id = uuid.uuid4()

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_delete_task(db):
    task = Task(
        name="Task to delete",
        description="This task will be deleted",
        completed=False,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    response = client.delete(f"/tasks/{task.id}")
    assert response.status_code == 204

    statement = select(Task).where(Task.id == task.id)
    deleted_task = db.execute(statement).scalar_one_or_none()
    assert deleted_task is None


def test_delete_task_not_found():
    import uuid

    task_id = uuid.uuid4()
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
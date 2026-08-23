import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from task_manager.models import Base, User, Task
from task_manager.main import app
from task_manager.database import get_db


load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

test_engine = create_engine(TEST_DATABASE_URL)

client = TestClient(app)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)


@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def test_user(db):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = client.post("/register/", json=user_data)

    assert response.status_code == 201

    user = db.query(User).filter(
        User.email == user_data["email"]
    ).first()

    return user


@pytest.fixture
def auth_headers(test_user):
    response = client.post(
        "/login/",
        data={
            "username": "test@example.com",
            "password": "testpassword",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def test_task(db, test_user):
    task = Task(
        name="Test task",
        description="Test task description",
        completed=False,
        user_id=test_user.id,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@pytest.fixture
def second_user(db):
    user_data = {
        "email": "second@example.com",
        "password": "secondpassword",
    }

    response = client.post("/register/", json=user_data)

    assert response.status_code == 201

    user = db.query(User).filter(
        User.email == user_data["email"]
    ).first()

    return user


@pytest.fixture
def second_auth_headers(second_user):
    response = client.post(
        "/login/",
        data={
            "username": "second@example.com",
            "password": "secondpassword",
        },
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
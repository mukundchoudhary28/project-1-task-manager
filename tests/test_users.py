from fastapi.testclient import TestClient
from task_manager.main import app
from task_manager.models import User
from sqlalchemy import select
from task_manager.utils import hash_password, verify_password

client = TestClient(app)

def test_create_user(db):
    user = {
        "email":"mukund.ch28@gmail.com",
        "password":"hello@12345"
    }
    response = client.post("/register", json=user)

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "mukund.ch28@gmail.com"
    assert data["role"] == "employee"

    statement = select(User).where(User.email == "mukund.ch28@gmail.com")
    created_user = db.execute(statement).scalar_one_or_none()

    assert created_user is not None
    assert created_user.email == "mukund.ch28@gmail.com"


def test_exisiting_email(db):

    user1 = {
            "email":"mukund.ch28@gmail.com",
            "password":"hello@12345"
        }

    user2 = {
                "email":"mukund.ch28@gmail.com",
                "password":"hello@12345"
            }
    
    response1 = client.post("/register", json=user1)
    response2 = client.post("/register",json=user2)

    assert response2.status_code == 409


def test_password_hashed(db):
    user = {
                "email":"mukund.ch28@gmail.com",
                "password":"hello@12345"
            }
    response = client.post("/register/", json=user)
    data = response.json()

    statement = select(User).where(User.id == data["id"])
    user_out = db.execute(statement).scalar_one_or_none()
    assert user_out.password_hash != user["password"]
    assert verify_password(user["password"], user_out.password_hash)










from fastapi.testclient import TestClient
from task_manager.main import app
from task_manager.models import User
from sqlalchemy import select
from task_manager.utils import hash_password, verify_password
import os, jwt
from dotenv import load_dotenv

load_dotenv()

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


def test_successfull_login(db):
    user = {
        "email":"mukund.ch28@gmail.com",
        "password":"hello@12345"
    }
    _ = client.post("/register/",json=user)

    response = client.post(
            "/login/",
            data={
                "username": user["email"],
                "password": user["password"],
                }
            )
    assert response.status_code == 200

    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"


def test_wrong_password(db):
    user = {
        "email":"mukund.ch28@gmail.com",
        "password":"hello@12345"
    }
    _ = client.post("/register/",json=user)

    login_user = {
            "email":"mukund.ch28@gmail.com",
            "password":"hello@1234"
        }
    response = client.post(
            "/login/",
            data={
                "username": login_user["email"],
                "password": login_user["password"],
                }
            )
    assert response.status_code == 401



def test_nonexistent_user(db):
    user = {
        "email":"mukund.ch28@gmail.com",
        "password":"hello@12345"
    }
    _ = client.post("/register/",json=user)

    login_user = {
            "email":"mukund.ch@gmail.com",
            "password":"hello@1234"
        }
    
    response = client.post(
        "/login/",
        data={
            "username": login_user["email"],
            "password": login_user["password"],
            }
        )
    assert response.status_code == 401
    


def test_valid_jwt_token(db):
    user = {
            "email":"mukund.ch28@gmail.com",
            "password":"hello@12345"
        }
    response1 = client.post("/register/",json=user)
    data1 = response1.json()

    response = client.post(
        "/login/",
        data={
            "username": user["email"],
            "password": user["password"],
            }
        )
    assert response.status_code == 200

    data = response.json()
    jwt_token = str(data["access_token"])
    payload = jwt.decode(jwt_token, algorithms='HS256', verify=True, key=os.getenv("JWT_SECRET_KEY"))
    assert payload["sub"] == str(data1["id"])
    assert "exp" in payload
    assert "iat" in payload










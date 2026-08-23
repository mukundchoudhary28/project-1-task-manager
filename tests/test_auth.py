from fastapi.testclient import TestClient
from task_manager.main import app
from task_manager.models import User
from sqlalchemy import select
from task_manager.utils import hash_password, verify_password
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

def test_get_task_without_token(db):
    response = client.get("/tasks")
    assert response.status_code == 401

   
def test_get_tasks_with_token(db):

    user = {
        "email":"mukund.ch28@gmail.com",
        "password":"hello@12345"
    }
    _ = client.post("/register/",json=user)

    login_response = client.post(
    "/login/",
    data={
        "username": user["email"],
        "password": user["password"],
        }
    )

    data = login_response.json()
    token = data["access_token"]

    response = client.get(
    "/tasks/",
    headers={
        "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == 200


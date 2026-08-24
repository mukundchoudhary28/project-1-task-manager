import uuid
from datetime import datetime
from pydantic import BaseModel
from task_manager.models import Priority, Role
from enum import Enum

class TaskCreate(BaseModel):
    name: str
    description: str
    completed: bool = False
    priority: Priority = Priority.MEDIUM

class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    completed: bool
    priority: Priority
    created_at: datetime  

    model_config = {
        "from_attributes": True
    }  

class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: Priority | None = None


# --------------------------------------------

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    role: Role

# class LoginRequest(BaseModel):
#     email: str
#     password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str



    
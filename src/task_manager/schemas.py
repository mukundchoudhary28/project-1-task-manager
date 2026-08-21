import uuid
from datetime import datetime
from pydantic import BaseModel
from task_manager.models import Priority

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
    created_at: datetime  

    model_config = {
        "from_attributes": True
    }  


class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    completed: bool | None = None
    
import uuid
from datetime import datetime
from pydantic import BaseModel

class TaskCreate(BaseModel):
    name: str
    description: str
    completed: bool = False

class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    completed: bool
    created_at: datetime  

    model_config = {
        "from_attributes": True
    }  
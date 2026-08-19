from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from task_manager.models import Task
from task_manager.database import get_db
from task_manager.schemas import TaskCreate, TaskResponse


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    new_task = Task(
        name=task.name,
        description=task.description,
        completed=task.completed,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
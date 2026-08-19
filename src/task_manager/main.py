from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import select

from task_manager.models import Task
from task_manager.database import get_db
from task_manager.schemas import TaskCreate, TaskResponse


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, World!"}

@app.post("/tasks/", response_model=TaskResponse)
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

@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    #Task is the model class that tells how every row in the database is structured. The select function is used to create a SQL SELECT statement that retrieves all rows from the Task table in the database. The statement variable holds this SQL statement, which can then be executed against the database to fetch the data.
    statement = select(Task) 
    tasks = db.execute(statement).scalars().all()
    return tasks


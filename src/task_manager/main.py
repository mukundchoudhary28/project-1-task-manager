import uuid

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from task_manager.models import Task
from task_manager.database import get_db
from task_manager.schemas import TaskCreate, TaskResponse, TaskUpdate


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Task Management Platform!"}


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

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id)
    task = db.execute(statement).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task 

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: uuid.UUID, task_update: TaskUpdate, db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id)
    task = db.execute(statement).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="At least one field must be provided for update"
        )
    
    for key,value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task




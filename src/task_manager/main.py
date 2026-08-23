import uuid

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from task_manager.models import Task, User
from task_manager.database import get_db
from task_manager.schemas import TaskCreate, TaskResponse, TaskUpdate
from task_manager.schemas import UserCreate, UserResponse, LoginResponse
from task_manager.utils import hash_password, verify_password, create_access_token
from task_manager.dependencies import get_current_user

from fastapi.security import OAuth2PasswordRequestForm


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to Task Management Platform!"}


@app.post("/tasks/", response_model=TaskResponse, status_code=201)
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    new_task = Task(
        name=task.name,
        description=task.description,
        completed=task.completed,
        priority=task.priority,
        user_id=current_user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks/", response_model=list[TaskResponse])
def get_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    #Task is the model class that tells how every row in the database is structured. The select function is used to create a SQL SELECT statement that retrieves all rows from the Task table in the database. The statement variable holds this SQL statement, which can then be executed against the database to fetch the data.
    statement = select(Task).where(Task.user_id == current_user.id)
    tasks = db.execute(statement).scalars().all()
    return tasks


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.execute(statement).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task 

@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: uuid.UUID, task_update: TaskUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
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


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: uuid.UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    task = db.execute(statement).scalar_one_or_none()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()



@app.post("/register/", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    
    statement = select(User).where(User.email == user.email)
    u = db.execute(statement).scalar_one_or_none()
    if u:
        raise HTTPException(status_code = 409, detail="Email already in use.")

    user_db = User(email = user.email,password_hash = hash_password(user.password))
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db


@app.post("/login/", response_model=LoginResponse, status_code=200)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    email = form_data.username
    password = form_data.password

    statement = select(User).where(User.email == email)
    user = db.execute(statement).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password!"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password!"
        )

    token = create_access_token(user.id)

    return LoginResponse(
        access_token=token,
        token_type="bearer"
    )
    



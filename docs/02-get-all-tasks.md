# Checkpoint 2 — Get All Tasks

## What I built

Implemented `GET /tasks/` to retrieve all tasks from PostgreSQL.

## Flow

GET /tasks/
→ FastAPI
→ database session
→ select(Task)
→ PostgreSQL
→ list[Task]
→ TaskResponse
→ JSON

## Key concepts learned

### Querying with SQLAlchemy

`select(Task)` creates a SQLAlchemy SELECT statement for the `tasks` table.

### Executing a query

`db.execute(statement)` executes the statement using the SQLAlchemy session.

### scalars()

`scalars()` extracts the ORM objects from the SQLAlchemy result.

### all()

`all()` collects the results into a Python list.

## API design

The endpoint always returns a list.

If tasks exist:

[
    task1,
    task2
]

If no tasks exist:

[]

This is preferable to returning a different response structure such as:

{
    "message": "No tasks available"
}

because clients can always expect the same response type.

## Important mental model

`Task` represents the database table.

`TaskResponse` represents the API response contract.

We query the database using the SQLAlchemy model, then FastAPI/Pydantic handles the API representation.
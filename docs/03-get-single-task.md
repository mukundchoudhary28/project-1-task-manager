# Checkpoint 3 — Get a Single Task

## What I Built

Implemented:

`GET /tasks/{task_id}`

The endpoint retrieves a specific task using its UUID.

## Request Flow

```text
GET /tasks/{task_id}
        ↓
FastAPI extracts task_id
        ↓
Pydantic validates UUID
        ↓
Database session injected
        ↓
SQLAlchemy queries Task by ID
        ↓
Task found?
   ┌────┴────┐
  Yes        No
   ↓          ↓
Task       HTTP 404
   ↓
TaskResponse
   ↓
JSON response


## Path Parameters

A path parameter allows a value to be provided directly as part of the URL.

Example:

GET /tasks/550e8400-e29b-41d4-a716-446655440000

The endpoint defines:

task_id: uuid.UUID

FastAPI/Pydantic validates that the value is a valid UUID before the endpoint function executes.

If the value is not a valid UUID, the request fails with a 422 Unprocessable Entity response.

Querying a Specific Task

We use:

statement = select(Task).where(Task.id == task_id)

Conceptually, this represents:

SELECT *
FROM tasks
WHERE id = task_id;

Task is the SQLAlchemy model representing the tasks table.

scalar_one_or_none()

For a specific task, we expect either:

exactly one task
no task

Therefore we use:

task = db.execute(statement).scalar_one_or_none()

The result is:

Task found       → Task object
Task not found   → None
Multiple results → error

Since id is a primary key, multiple results should not occur.

This differs from:

scalars().all()

which we used for GET /tasks/ because that endpoint can return many tasks.

Handling a Missing Task

If no task exists with the requested UUID:

if task is None:
    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )

We return 404 Not Found because the request is valid, but the requested resource does not exist.

422 vs 404

These represent different problems.

Invalid UUID
GET /tasks/hello

The path parameter fails UUID validation.

Result:

422 Unprocessable Entity

The endpoint function does not execute.

Valid UUID but Task Doesn't Exist
GET /tasks/<valid-uuid>

The UUID is valid, but there is no corresponding task in the database.

Result:

404 Not Found

The endpoint executes and determines that the resource doesn't exist.

Important Mental Model

There is a difference between:

Invalid input

and

Valid input referring to a nonexistent resource.

Invalid UUID
    ↓
422


Valid UUID
    ↓
Database lookup
    ↓
No matching task
    ↓
404
Key Concepts Learned
Path parameters
UUID validation
FastAPI/Pydantic validation before endpoint execution
SQLAlchemy select()
SQLAlchemy where()
scalar_one_or_none()
HTTP 404 Not Found
Difference between 422 and 404
Difference between scalars().all() and scalar_one_or_none()
Handling unhappy paths in an API
Questions I Can Now Answer
What is a path parameter?
How does FastAPI validate a UUID path parameter?
What happens when the UUID is invalid?
Why do we use scalar_one_or_none() for a single task?
Why do we return 404 when a task doesn't exist?
What's the difference between 422 and 404?
What happens from the HTTP request until the JSON response?
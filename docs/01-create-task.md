# Checkpoint 1 — Create Task

## What I built

Implemented `POST /tasks/` to create a task and persist it in PostgreSQL.

## Architecture

Client
→ FastAPI
→ Pydantic
→ SQLAlchemy
→ PostgreSQL
→ Response

## Key concepts learned

### Pydantic schemas

`TaskCreate` defines and validates the structure of incoming API data.

`TaskResponse` defines the structure of outgoing API data.

### SQLAlchemy models

`Task` represents the `tasks` table in PostgreSQL.

### Sessions

A SQLAlchemy `Session` is used to perform database operations.

FastAPI creates a session through `Depends(get_db)` and closes it after the request.

### add vs commit

`db.add()` adds an object to the SQLAlchemy session's pending state.

`db.commit()` commits the transaction and persists the change to PostgreSQL.

### refresh

`db.refresh()` refreshes the Python SQLAlchemy object with the current values from the database.

## Important mental model

Pydantic models describe the API contract.

SQLAlchemy models describe database persistence.

They are separate because the API representation and database representation have different responsibilities.

## Things I initially found confusing

- Difference between SQLAlchemy Engine and Session
- Difference between `db.add()` and `db.commit()`
- Why `refresh()` is needed
- Why Pydantic and SQLAlchemy models are separate

## Questions I can now answer

- What happens when `POST /tasks/` is called?
- Why do we need `TaskCreate`?
- Why don't we send the UUID from the client?
- What does `Depends(get_db)` do?
- What does `commit()` do?
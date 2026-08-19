# Checkpoint 5 — CRUD Complete

## Milestone

The core CRUD functionality of the Task Manager API is now complete.

The application can create, retrieve, update, and delete tasks using a PostgreSQL database.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/tasks/` | Create a task |
| GET | `/tasks/` | Retrieve all tasks |
| GET | `/tasks/{id}` | Retrieve a specific task |
| PATCH | `/tasks/{id}` | Partially update a task |
| DELETE | `/tasks/{id}` | Delete a task |

## Architecture So Far

```text
Client
   ↓
FastAPI
   ↓
Pydantic schemas
   ↓
SQLAlchemy ORM
   ↓
PostgreSQL
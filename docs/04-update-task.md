# Checkpoint 4 — Update a Task

## What I Built

Implemented:

`PATCH /tasks/{task_id}`

The endpoint allows the client to partially update an existing task without sending the entire task.

For example:

```json
{
  "completed": true
}


The SQLAlchemy Task object is a Python representation of a database row.

Modifying the object:  "task.completed = True" changes the Python ORM object first.

Calling: "db.commit()" persists the tracked change to PostgreSQL.
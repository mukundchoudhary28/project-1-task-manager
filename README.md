# Task Manager

A task management platform with a FastAPI backend and a React + TypeScript frontend. Users register, log in, and manage their own tasks — create, edit, set priority (low/medium/high), mark complete, and delete.

## Architecture

```
Browser → Nginx (:80) → FastAPI (:8000) → PostgreSQL (:5432)
              │
              └─ serves the Vite-built React app, and reverse-proxies /api/* to FastAPI
```

React is built with Vite into static files, which Nginx serves. Nginx also reverse-proxies any request under `/api/` to the FastAPI backend, so the browser only ever talks to one origin — no CORS is needed between the frontend and API.

## Tech stack

**Backend** (`src/`)
- Python 3.14, FastAPI, SQLAlchemy 2.0, PostgreSQL 17, Alembic migrations
- JWT auth (Argon2 password hashing, 60-minute token expiry)
- Package manager: [uv](https://docs.astral.sh/uv/)

**Frontend** (`frontend/`)
- React 19 + TypeScript, Vite
- React Router, TanStack Query, Axios, Tailwind CSS
- Built and served by **Nginx** in production (multi-stage `frontend/Dockerfile`), which also reverse-proxies `/api/*` to the FastAPI container

## Prerequisites

- [Docker](https://www.docker.com/) and Docker Compose
- [Node.js](https://nodejs.org/) 18+ and npm (only needed for frontend hot-reload development, see below)

## 1. Configure environment variables

```bash
cp .env.example .env
```

```
DATABASE_URL=postgresql+psycopg://task_manager:task_manager_password@localhost:5432/task_manager
TEST_DATABASE_URL=postgresql+psycopg://task_manager_test:task_manager_test_password@localhost:5433/task_manager_test
JWT_SECRET_KEY=<any random string>
```

## 2. Run the full stack

```bash
docker compose up -d --build
```

This builds and starts everything:
- **db** — PostgreSQL
- **api** — FastAPI, runs Alembic migrations automatically on startup, at `http://localhost:8000`
- **frontend** — Vite build served by Nginx, at `http://localhost`

Open **http://localhost**, register an account, log in, and manage tasks. Nginx handles routing `/api/*` to the backend, so that's the only URL you need.

To rebuild a single service after changing its code:

```bash
docker compose up -d --build api        # backend changes
docker compose up -d --build frontend   # frontend changes
```

To run the backend test suite instead:

```bash
docker compose --profile test up -d test_db
docker compose --profile test run --rm test
```

## 3. Frontend development with hot reload

Rebuilding the Nginx image on every change is slow for active frontend development. Instead, run the backend in Docker and the frontend with Vite's dev server, which proxies `/api/*` to `localhost:8000` (configured in `frontend/vite.config.ts`) the same way Nginx does in production:

```bash
docker compose up -d db api
```

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:5173**.

## Project structure

```
src/task_manager/     FastAPI app: routes (main.py), models, schemas, auth
alembic/               Database migrations
tests/                  Backend test suite (pytest)
frontend/              React + TypeScript client (see frontend/README.md)
  Dockerfile            Multi-stage build: npm run build → served by Nginx
  nginx.conf             Serves the built app, reverse-proxies /api/* to the api service
docker-compose.yaml     frontend / db / test_db / api / test services
```


                         INTERNET / BROWSER
                                │
                                │ HTTP
                                ▼
                     ┌─────────────────────┐
                     │   Frontend Container │
                     │                     │
                     │       Nginx         │
                     │                     │
                     │  React static files │
                     └──────────┬──────────┘
                                │
                       /api/*   │
                                ▼
                     ┌─────────────────────┐
                     │    FastAPI API      │
                     │                     │
                     │     container       │
                     └──────────┬──────────┘
                                │
                                │ db:5432
                                ▼
                     ┌─────────────────────┐
                     │     PostgreSQL      │
                     │                     │
                     │      volume         │
                     └─────────────────────┘
# Task Manager — Frontend

React + TypeScript client for the Task Manager API. See the [repo root README](../README.md) for how to run the backend alongside this.

## Tech stack

- React 19 + TypeScript, Vite
- React Router — routing
- TanStack Query — server state (fetching, caching, mutations)
- Axios — HTTP client
- Tailwind CSS — styling

## Setup

```bash
npm install
```

The app calls the API at same-origin `/api/*`. In production, Nginx serves this build and reverse-proxies `/api/*` to the FastAPI container (see `Dockerfile` / `nginx.conf`). In dev, Vite's dev server does the equivalent proxying to `localhost:8000` (see the `server.proxy` block in `vite.config.ts`) — no env var needed.

## Running

Make sure the backend is running first (see the [root README](../README.md)):

```bash
docker compose up -d db api
```

Then, from `frontend/`:

```bash
npm run dev
```

Open http://localhost:5173.

To run the production build (Nginx-served, same as `docker compose up`) instead of the dev server, build the whole stack from the repo root — see the [root README](../README.md).

## Other scripts

```bash
npm run build     # type-check and build for production (output in dist/)
npm run preview   # preview the production build locally
npm run lint       # lint with oxlint
```

## Structure

```
Dockerfile     Multi-stage build: npm run build → served by Nginx
nginx.conf      Serves dist/, reverse-proxies /api/* to the api service
src/
  api/         axios client + auth/task API calls
  context/     AuthContext (JWT stored in localStorage)
  hooks/       useAuth, useTasks (TanStack Query hooks)
  components/  Navbar, ProtectedRoute, TaskList/TaskItem, form + confirm modals
  pages/       LoginPage, RegisterPage, TasksPage
  types/       TypeScript types mirroring the backend's Pydantic schemas
```

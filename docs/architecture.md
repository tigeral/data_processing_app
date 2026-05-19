# System Architecture

## Overview

The application is a desktop application composed of two main processes running locally:

1. **Backend** — a Python server providing the execution engine, task queue, and REST/WebSocket API.
2. **Frontend** — a React single-page application served by the backend (or an embedded browser in later phases).

Users interact exclusively through the frontend. The backend handles all processing, persistence, and external integrations.

## High-Level Component Diagram

```
+--------------------------------------------------+
|                 Desktop Application              |
|                                                  |
|  +------------------+    +--------------------+  |
|  |    Frontend       |    |      Backend       |  |
|  |  (React / TS)     |<-->|  (FastAPI / Python)|  |
|  |                   | REST|                   |  |
|  |  - Dashboard      | WS  |  - REST API       |  |
|  |  - Workflow       |    |  - WebSocket hub   |  |
|  |    Builder        |    |  - Celery worker   |  |
|  |  - Drop Zone      |    |  - Execution       |  |
|  |                   |    |    engine          |  |
|  +------------------+    +--------+-----------+  |
|                                   |               |
|                          +--------+-----------+   |
|                          |   PostgreSQL DB    |   |
|                          +--------------------+   |
+--------------------------------------------------+
         |                          |
         v                          v
   External APIs             Local File System
   AI model APIs
   Browser automation (Playwright)
```

## Components

### Backend (`backend/`)

- **FastAPI application** — HTTP and WebSocket server. Exposes REST endpoints for workflow management, task control, and file operations. Serves the frontend in production.
- **Celery workers** — asynchronous task queue for running processing pipelines. Workers can be scaled independently.
- **Execution engine** — (Phase 3+) orchestrates workflow step execution, manages state, handles errors and retries.
- **SQLAlchemy models + PostgreSQL** — persistent storage for workflows, task history, logs, and configuration.

### Frontend (`frontend/`)

- **React + TypeScript** — component-based UI.
- **React Flow** — (Phase 4+) visual workflow builder canvas.
- **Drop Zone component** — (Phase 1) accepts dropped files, URLs, and images. Identifies input type and dispatches to backend.
- **Dashboard** — (Phase 7+) user-composable layout of input widgets and status monitors.

### Communication

| Channel | Purpose |
|---|---|
| REST API | CRUD operations, workflow management, task submission |
| WebSockets | Real-time task progress, log streaming |

### Security and Remote Access

The application is primarily local, but may be accessed over LAN or the internet. Considerations:
- Authentication will be required for any non-localhost access.
- Passwordless authentication (e.g., magic links, passkeys) is under consideration.
- TLS must be enforced for any remote connections.
- Specific auth design is deferred to a later phase.

## Build and Deployment

- **Development** — backend and frontend run as separate processes with hot reload.
- **Desktop packaging** — (Phase 2+) native installers for Windows, macOS, and Linux. Packaging strategy TBD (Electron, Tauri, or custom launcher).
- **Staging/CI** — GitHub Actions deploys to a test server on each merge to the main branch.

## External Integrations

| Integration | Purpose |
|---|---|
| External REST APIs | Data fetch/push (e.g., Etsy, Odoo) |
| AI model APIs | Image/text processing via model inference APIs |
| Playwright | Browser automation for web scraping and form interaction |
| Local file system | Read, write, and overwrite user files |

# Data Processing App

A desktop application for building and running data processing pipelines and non-linear workflows. Users define workflows visually, compose dashboards with input widgets, then feed data by dragging and dropping files, URLs, or images. The backend executes the pipeline; the frontend provides the workflow designer and dashboard.

## Overview

The application follows a local client-server model: a Python/FastAPI backend serves as the execution engine and data layer, while a React frontend runs in an embedded browser view. Both are packaged together as a native desktop application.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11+, FastAPI, Celery, SQLAlchemy |
| Database | PostgreSQL |
| Frontend | React, TypeScript, React Flow |
| Communication | REST API, WebSockets |
| Desktop packaging | PyInstaller + Inno Setup (Windows) |
| Testing | pytest, Playwright |
| CI/CD | GitHub Actions |

## Key Features

- Drag-and-drop files, images, and URLs into the interface
- Visual workflow builder with configurable processing nodes
- Local file system access (read, overwrite, save with modified names)
- Integration with external APIs and services
- Integration with AI models
- Web browser automation via Playwright
- Real-time task status updates and log viewer
- CLI for scripting and AI-agent integration

## Project Structure

```
data_processing_app/
├── backend/          # FastAPI server, Celery tasks, SQLAlchemy models
├── frontend/         # React application
├── tests/            # Backend (pytest) and E2E (Playwright) tests
├── docs/             # Architecture, roadmap, feature specs
├── scripts/          # Setup, build, and maintenance scripts
└── logs/             # Runtime logs (development and testing)
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ and npm
- PostgreSQL is **not required** for Phase 1

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Or on Windows, run `scripts\start-backend.bat`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Or on Windows, run `scripts\start-frontend.bat`.

Open [http://localhost:5173](http://localhost:5173) in your browser. The backend must be running for drops to be forwarded to the server.

### Stopping the servers

```bat
scripts\stop-backend.bat
scripts\stop-frontend.bat
```

## Building a Windows Desktop Package

Produces a standalone installer that requires no Python or Node.js on the target machine.

### Prerequisites

- [Inno Setup 6](https://jrsoftware.org/isinfo.php) installed and `iscc` available in `PATH`
- Python venv set up (`py -m venv .venv && .venv\Scripts\pip install -r requirements.txt`)
- Node.js 20+ and npm

### Build

```bat
scripts\build-windows.bat
```

The script runs three steps automatically:

1. **Frontend** — `npm run build` compiles the React app to `frontend/dist/`.
2. **PyInstaller** — bundles the Python backend and `frontend/dist/` into `dist/DataProcessingApp/`.
3. **Inno Setup** — packages everything into `dist/installer/DataProcessingApp-setup.exe`.

### Install and run

Run `DataProcessingApp-setup.exe` on any Windows machine. After installation, use the desktop shortcut or Start Menu entry to launch the app. The launcher starts the backend server and opens the app in your default browser automatically.

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Phase 1 Spec](docs/phase1.md)
- [Development Workflow](docs/dev-workflow.md)

## Development Workflow

See [docs/dev-workflow.md](docs/dev-workflow.md) for the full branching, documentation, and review process.

## License

[MIT](LICENSE)

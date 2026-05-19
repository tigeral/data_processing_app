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
| Desktop packaging | (TBD — Phase 2) |
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

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Phase 1 Spec](docs/phase1.md)
- [Development Workflow](docs/dev-workflow.md)

## Development Workflow

See [docs/dev-workflow.md](docs/dev-workflow.md) for the full branching, documentation, and review process.

## License

[MIT](LICENSE)

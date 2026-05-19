# Project Roadmap

## Phase 1 — Drag-and-Drop Proof of Concept

Goal: Establish a working full-stack skeleton and validate the drag-and-drop input mechanism.

- Create a basic backend (FastAPI) + frontend (React) application.
- Set up a manual local build process for development.
- Implement a drag-and-drop component that logs all dropped items to the console and the backend.
- Detect dropped item type: local file, URL, image, directory.
- Support batch drops: multiple files, a folder, mixed content.

See [phase1.md](phase1.md) for the detailed specification.

---

## Phase 2 — Native Desktop App (Windows)

Goal: Package the application as a native Windows installer.

- Research and select desktop packaging approach (Electron, Tauri, or custom launcher).
- Set up local build scripts for producing a standalone Windows executable.
- Create a Windows installer (NSIS, WiX, or similar).

---

## Phase 3 — Workflow Execution Engine

Goal: Implement the backend engine that runs processing pipelines.

- Design the class structure for processing steps, workflows, and execution context.
- Implement the execution engine with logging, error handling, and progress reporting.
- Define data models for input, output, and intermediary results.
- Connect the drag-and-drop UI to processing steps: dropped items trigger a workflow.
- Implement a CLI for triggering workflows and managing tasks from the command line.

---

## Phase 4 — Workflow Builder UI

Goal: Enable users to visually design and persist workflows.

- Define a workflow serialization format (JSON or YAML).
- Implement the visual workflow builder using React Flow.
- Build forms for configuring processing step parameters.
- Implement saving and loading workflows from the database.

---

## Phase 5 — AI CLI Integration

Goal: Allow workflows to invoke AI coding assistants as processing steps.

- Evaluate and integrate one or more AI CLI tools: Claude Code, OpenAI Codex CLI, Gemini CLI.
- Define the interface for spawning AI CLI processes from within a workflow step.

---

## Phase 6 — Web Browser Automation

Goal: Enable workflows to automate browser interactions.

- Integrate Playwright (preferred) or Selenium.
- Design a browser automation step type: navigate, click, fill form, extract data.
- Handle browser lifecycle within the execution engine.

---

## Phase 7 — UI and UX Improvements

Goal: Polish the user experience and make the interface production-quality.

- Design and implement a composable dashboard where users place input widgets.
- Polish drag-and-drop interactions and visual feedback.
- Polish the workflow builder UI.
- Implement real-time task status updates and an in-app log viewer.

---

## Phase 8 — CI/CD and Comprehensive Testing

Goal: Automate quality assurance and establish a reliable release pipeline.

- Set up GitHub Actions for automated testing on every pull request.
- Set up automated deployment to a staging/test server on merge.
- Write comprehensive backend tests (pytest) and E2E tests (Playwright).
- Define test coverage targets and quality gates.

---

## Phase 9 — TBD

Scope to be determined based on project progress and user feedback.

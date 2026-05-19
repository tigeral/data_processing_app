# Phase 1 — Drag-and-Drop Proof of Concept

## Goal

Establish a working full-stack skeleton and validate the core input mechanism: drag-and-drop of files, URLs, and images. The result should demonstrate end-to-end data flow from the browser drop zone to the backend log.

## Deliverables

1. A running FastAPI backend with at least one endpoint that accepts dropped item data.
2. A React frontend with a working drag-and-drop zone component.
3. Item type detection logic (file, URL, plain image from web page, directory).
4. Batch drop support (multiple files, a folder, or a mixed selection).
5. Console and backend logging of all dropped items with their detected type and metadata.
6. A documented manual process for starting the dev environment locally.

## Out of Scope for Phase 1

- Workflow execution, processing steps, or any pipeline logic.
- Database persistence (logs to console/stdout only).
- Authentication or remote access.
- Native desktop packaging (Phase 2).
- Any UI beyond the drop zone and a basic log display.

## Acceptance Criteria

| # | Criterion |
|---|---|
| 1 | User can start backend and frontend locally by following setup instructions. |
| 2 | Dragging a local file onto the drop zone logs its name, size, and MIME type in the browser console and in the backend stdout. |
| 3 | Dragging a URL (text or link) onto the drop zone logs the URL string and identifies it as a URL. |
| 4 | Dragging an image directly from a web page (image drag) logs the image URL and identifies it as a web image. |
| 5 | Dragging a folder logs the folder name and the list of files inside it (one level deep minimum). |
| 6 | Dropping multiple items at once logs each item individually with correct type detection. |
| 7 | The drop zone provides visible feedback on drag-over (highlighted border or overlay). |
| 8 | All dropped item data is sent to the backend via a REST POST request and acknowledged with HTTP 200. |

## Task Breakdown

### Backend

- [x] Initialize FastAPI project under `backend/`.
- [x] Set up `requirements.txt` with FastAPI and Uvicorn.
- [x] Implement `POST /api/v1/drops` endpoint that accepts a JSON payload describing one or more dropped items and logs them.
- [x] Define a Pydantic schema for a dropped item: `type` (file | url | web-image | directory), `name`, `mime_type` (optional), `size` (optional), `url` (optional), `children` (optional list for directories).
- [x] Add CORS middleware to allow requests from the local frontend dev server.
- [x] Write `scripts/start-backend.bat` to start the server with Uvicorn in reload mode.

### Frontend

- [x] Initialize React + TypeScript project under `frontend/` using Vite.
- [x] Implement `DropZone` component (`src/components/DropZone.tsx`):
  - Handles `dragover`, `dragenter`, `dragleave`, `drop` events.
  - Reads `DataTransfer.items` and `DataTransfer.files` to extract dropped content.
  - Detects item type from `DataTransferItem.kind` and MIME type.
  - Uses `webkitGetAsEntry()` to detect directories and enumerate one level of contents.
  - Displays drag-over visual feedback (CSS class toggle).
- [x] Implement item type detection utility (`src/utils/detectDroppedItems.ts`).
- [x] Send detected items to `POST /api/v1/drops` after each drop event.
- [x] Display a log list below the drop zone showing dropped items with type badges.
- [x] Write `scripts/start-frontend.bat` to start the Vite dev server.

### Documentation

- [x] Add setup instructions to `README.md`.
- [x] Document known browser limitations for drag-and-drop.

## Decisions Made

- **Directory traversal depth**: one level deep (confirmed by user).
- **Frontend tooling**: Vite with `react-ts` template (confirmed by user).
- **Port configuration**: backend `8000`, frontend `5173` (confirmed by user).

## Known Browser Limitations

- A file dragged from another browser tab (web image) does not expose a local file path — only the source URL is available via `text/uri-list`. The `web-image` type is inferred from the URL extension.
- `webkitGetAsEntry()` is a non-standard API, but is supported in all major browsers (Chrome, Firefox, Safari, Edge). It is the only way to detect directories in a drop event without a file input.
- Some browsers do not populate `DataTransfer.items` in all drag scenarios (e.g., drags from native OS file managers on older versions). The implementation falls back to `DataTransfer.files` in that case.

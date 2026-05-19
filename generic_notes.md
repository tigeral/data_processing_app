Project notes and prompts for AI
================================

Project summary
---------------
Project is a desktop app built as server backend + web UI. 

The purpose of this app: build a data processing pipelines and non-linear workflows for processing files and web resources. User will define some processing workflows, put their input widgets on a dashboard, and then drag and drop files, or URLs, or images from web page. The app will handle the input and run the processing pipeline.
So, the backend will provide an execution engine and the UI will provide ability to design the processing workflows and compose dashboards. 

Tech stack
---------- 
- Backend: Python, FastAPI, Celery for task queue, SQLAlchemy + PostgreSQL for persistence.
- Frontend: React, TypeScript, React Flow for visualizing workflows.
- Communication: REST API for backend-frontend communication, WebSockets for real-time updates on task status. Possible to connect remote app through LAN or even over the internet, so we need to consider security and authentication (paswordless auth is possible too).
- Build and deployment: native desktop apps for Windows, macOS, and Linux.
- QA: Playwright for UI and end-to-end testing, pytest for backend testing.
- CI/CD: GitHub Actions for automated testing and deployment to test server.

Key features
------------
- Drag-and-drop files, images, and URLs to app interface.
- Visual workflow builder with nodes representing processing steps. Processing step can be chosen from a library of pre-defined actions and customized with parameters.
- Work with local file system. For example, if image file processing flow supposes to change image file size, the app should be able to overwrite the original file (if it was local) or save the processed file in the same folder with modified name.
- Integration with external APIs and services. For example, it should be possible to create a flow that will get product details from Etsy website by URL and create same item in Odoo shop.
- Integration with AI models. For example, it should be possible to send image file with a predefined prompt to Nano Banana API and get the processed image back. 
- Ability to automate actions in a web browser. For example, it should be possible to create a flow that will open a web page, fill in some forms, and submit them.
- Real-time status updates on processing tasks, with ability to view logs and results.
- CLI for advanced users or for AI integration, allowing users to trigger workflows and manage tasks from the command line.

Project structure
-----------------
- `backend/`: contains the FastAPI server code, Celery tasks, and database models.
- `frontend/`: contains the React application code, including components, hooks, and styles.
- `tests/`: contains unit and integration tests for both backend and frontend.
- `docs/`: contains project documentation, including API docs and user guides.
- `scripts/`: contains utility scripts for setup, deployment, and maintenance.
- `logs/`: directory for storing application logs duuring development and testing.

Development workflow
--------------------
- Create a new branch for each feature or bug fix.
- Desing the feature and write documentation for it in `docs/features/` directory in Markdown format.
  - Add feature description, user stories, and acceptance criteria.
  - If any UI changes are needed, include mockups or wireframes.
- Implement the feature in the codebase, following best practices and coding standards.
- Write unit tests for the new feature and ensure they pass.
- Add feature implementation notes to the feature documentation, including any important design decisions, tradeoffs, new libraries used and how to use the feature.
- Update common project documentation if the new feature affects something that already exists in the docs.
- Create a pull request and request reviews from team members.
- After approval, merge the pull request. A CI/CD pipeline will run tests and deploy the updated app to the test server for further testing.

Project roadmap
---------------
- Phase 1: drag and drop proof of concept.
  - Create a basic backend + frontend app, setup manual build process.
  - Create a drag-and-drop component on UI that will log all dropped items to the console.
  - Try to recognize dropped item type (file, URL, image, etc.).
  - Allow batch processing: drag and drop multiple items, files directory, etc.
- Phase 2: build a native desktop app for Windows OS.
  - Set up local build scripts.
  - Create an installer for Windows OS.  
- Phase 3: workflow execution engine
  - Design class structure for processing steps and workflows in the backend.
  - Create an execution engine, logging, error handling, and progress reporting.
  - Create class structure for input data, output data, and processing intermediary results.
  - Attach processing steps to the drag-and-drop UI component.
  - Create a CLI for triggering workflows and managing tasks. 
- Phase 4: workflow builder UI
  - Design workflow serialization format based on JSON or YAML.
  - Design a visual workflow builder using React Flow.
  - Implement forms to configure processing step parameters.
  - Implement saving and loading workflows from the database.
- Phase 5: integration with some AI CLI
  - Attach Claude Code, Codex or Jemini CLI to the app.
- Phase 6: integration with web browser automation
  - Integrate Playwright or Selenium for browser automation.
- Phase 7: improve UI and user experience
  - Design a dashboard where users can place input widgets and monitor processing tasks.
  - Polish drag-and-drop interactions and workflow builder builder UI.
  - Implement real-time status updates and logs viewing in the UI.
- Phase 8: CI/CD and testing
  - Set up GitHub Actions for automated testing and deployment.
  - Write comprehensive tests for both backend and frontend.
  - Set up a test server for staging deployments and user acceptance testing.
- Phase 9: TBD


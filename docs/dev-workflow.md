# Development Workflow

## Branching

- Create a dedicated branch for each feature or bug fix.
- Branch name convention: `feature/<short-description>` or `fix/<short-description>`.
- Never commit directly to `main`.

## Feature Development Process

### 1. Design First

Before writing any code, create a feature spec in `docs/features/<feature-name>.md`. The spec must include:

- **Description** — what the feature does and why it exists.
- **User stories** — one or more `As a <role>, I want <action> so that <outcome>` statements.
- **Acceptance criteria** — a numbered checklist of testable conditions that define "done".
- **UI mockups or wireframes** — required if the feature involves any visual changes (ASCII diagrams are acceptable for simple layouts).

### 2. Implement

- Follow the coding standards for the relevant layer (Python/FastAPI conventions for backend, React/TypeScript conventions for frontend).
- Keep changes focused on the feature branch — avoid unrelated refactors.

### 3. Write Tests

- Backend: write pytest unit tests for new logic. Integration tests where the feature touches the database or external services.
- Frontend/E2E: write Playwright tests for user-facing flows introduced by the feature.
- Tests must pass before opening a pull request.

### 4. Update Documentation

After implementation:
- Add an **Implementation Notes** section to the feature doc (`docs/features/<feature-name>.md`) covering:
  - Key design decisions and the reasoning behind them.
  - Trade-offs considered.
  - Any new libraries introduced and how to use them.
- Update shared docs (`docs/architecture.md`, `README.md`, etc.) if the feature affects anything already documented there.

### 5. Pull Request

- Open a pull request against `main`.
- PR description should summarize what changed, link to the feature doc, and note any deployment considerations.
- Request reviews from at least one team member.
- Address review comments before merging.

### 6. Merge and Deploy

- Merge only after approval.
- A CI/CD pipeline (GitHub Actions) will automatically run the full test suite and deploy to the staging/test server on merge.
- Verify the deployment on the test server before closing the feature ticket.

## Documentation Structure

```
docs/
├── architecture.md       # System architecture and tech decisions
├── roadmap.md            # Project phases and goals
├── dev-workflow.md       # This file
├── phase1.md             # Phase 1 detailed spec
└── features/             # One file per feature
    └── <feature-name>.md
```

## Code Review Guidelines

- Review for correctness, security, and test coverage — not just style.
- Flag any changes that affect shared infrastructure (DB schema, API contracts, build process).
- Approve only when acceptance criteria from the feature doc are demonstrably met.

# MVP_SPEC.md

## Purpose

This document defines the first practical MVP for `agent-project-memory`.

The MVP must be small, local-first, useful without AI, and easy for future agents to implement without changing the product concept.

## 1. Product Scope

### What The MVP Does

The MVP provides a local Web UI and local JSON API for maintaining project memory records.

It supports:

- Creating and listing local projects.
- Managing canonical context entries for each project.
- Managing decisions.
- Managing open questions.
- Managing glossary terms.
- Managing notes.
- Managing agent work logs.
- Exporting an AI-readable `context.md` for a project.
- Persisting data in SQLite.

The MVP is useful for human maintainers even without any AI integration. A maintainer can open the local app, record project knowledge, and export readable Markdown context.

### What The MVP Does Not Do

The MVP does not include:

- Login or user accounts.
- Cloud sync.
- Hosted service features.
- GitHub Issues or PR integration.
- LLM API calls.
- Semantic search.
- Vector databases.
- Multi-user permissions.
- Plugin architecture.
- Complex project management features.
- Realtime collaboration.
- Frontend frameworks.

## 2. Data Model

SQLite is the MVP database. Use simple tables, explicit columns, and ISO-8601 UTC timestamps stored as text.

Recommended local database path for MVP: `./.agent-project-memory/memory.sqlite`.

All content fields store Markdown-compatible plain text unless otherwise specified.

### Common Conventions

- Primary keys are integer autoincrement IDs.
- Foreign keys are enforced with `PRAGMA foreign_keys = ON`.
- `created_at` and `updated_at` are required on all user-editable tables.
- `status` fields use small lowercase strings.
- Avoid soft deletion in the first MVP unless explicitly needed.

### projects

Stores tracked projects.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Local project ID. |
| name | TEXT | yes | Human-readable project name. |
| slug | TEXT UNIQUE | yes | URL/API-safe identifier. |
| description | TEXT | no | Short project summary. |
| root_path | TEXT | no | Optional local path; do not require it for MVP. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Unique index on `slug`.

### context_entries

Stores canonical context sections for a project.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Context entry ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| section | TEXT | yes | Example: `summary`, `goals`, `non_goals`, `architecture`, `constraints`. |
| title | TEXT | yes | Display title. |
| body | TEXT | yes | Markdown-compatible content. |
| position | INTEGER | yes | Export/display order. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Unique index on `(project_id, section)`.
- Index on `(project_id, position)`.

### decisions

Stores product and technical decisions.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Decision ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| title | TEXT | yes | Decision title. |
| status | TEXT | yes | `proposed`, `accepted`, or `superseded`. |
| decision | TEXT | yes | The decision itself. |
| rationale | TEXT | no | Why the decision exists. |
| consequences | TEXT | no | Tradeoffs or follow-up effects. |
| supersedes_decision_id | INTEGER | no | Optional reference to another decision. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Index on `(project_id, status)`.

### open_questions

Stores unresolved and resolved project questions.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Question ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| title | TEXT | yes | Short question title. |
| status | TEXT | yes | `open`, `answered`, or `deferred`. |
| question | TEXT | yes | The unresolved question. |
| context | TEXT | no | Why it matters. |
| answer | TEXT | no | Filled when answered. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Index on `(project_id, status)`.

### glossary_terms

Stores project-specific terminology.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Glossary term ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| term | TEXT | yes | Canonical term. |
| definition | TEXT | yes | Meaning in this project. |
| aliases | TEXT | no | Comma-separated aliases for MVP simplicity. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Unique index on `(project_id, term)`.

### notes

Stores general project memory notes.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Note ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| title | TEXT | yes | Note title. |
| body | TEXT | yes | Markdown-compatible content. |
| tags | TEXT | no | Comma-separated tags for MVP simplicity. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Index on `created_at`.

### agent_logs

Stores structured work logs from AI agents or automated tools.

Columns:

| Column | Type | Required | Notes |
| --- | --- | --- | --- |
| id | INTEGER PRIMARY KEY AUTOINCREMENT | yes | Agent log ID. |
| project_id | INTEGER | yes | References `projects.id`. |
| agent_name | TEXT | no | Example: `Codex`, `Claude`, `Gemini`, or tool name. |
| summary | TEXT | yes | What happened. |
| changed_files | TEXT | no | Newline-separated file paths for MVP simplicity. |
| checks_run | TEXT | no | Tests or manual checks run. |
| known_issues | TEXT | no | Remaining issues. |
| next_task | TEXT | no | Recommended next task. |
| created_at | TEXT | yes | ISO-8601 UTC timestamp. |
| updated_at | TEXT | yes | ISO-8601 UTC timestamp. |

Indexes:

- Index on `project_id`.
- Index on `created_at`.

## 3. API Design

The MVP API is local-only JSON over HTTP. It is intended for the Web UI, local scripts, and future AI agent integrations.

### General API Rules

- Request bodies are JSON for `POST` endpoints.
- Responses are JSON except Markdown export.
- Validation errors return HTTP `400`.
- Missing records return HTTP `404`.
- Successful creation returns HTTP `201`.
- List endpoints return records ordered deterministically.
- No authentication in MVP.

### GET /api/health

Returns service status.

Response:

```json
{
  "status": "ok"
}
```

### GET /api/projects

Returns all projects ordered by `name`.

### POST /api/projects

Creates a project.

Required fields:

- `name`
- `slug`

Optional fields:

- `description`
- `root_path`

### GET /api/projects/<project_id>

Returns one project by ID.

### GET /api/projects/<project_id>/context

Returns context entries ordered by `position`, then `title`.

### POST /api/projects/<project_id>/context

Creates a context entry.

Required fields:

- `section`
- `title`
- `body`
- `position`

### GET /api/projects/<project_id>/decisions

Returns decisions ordered by status priority, then `created_at`.

Default export-relevant status priority:

- `accepted`
- `proposed`
- `superseded`

### POST /api/projects/<project_id>/decisions

Creates a decision.

Required fields:

- `title`
- `status`
- `decision`

Optional fields:

- `rationale`
- `consequences`
- `supersedes_decision_id`

### GET /api/projects/<project_id>/questions

Returns open questions ordered by status priority, then `created_at`.

Default status priority:

- `open`
- `deferred`
- `answered`

### POST /api/projects/<project_id>/questions

Creates an open question.

Required fields:

- `title`
- `status`
- `question`

Optional fields:

- `context`
- `answer`

### GET /api/projects/<project_id>/glossary

Returns glossary terms ordered by `term`.

### POST /api/projects/<project_id>/glossary

Creates a glossary term.

Required fields:

- `term`
- `definition`

Optional fields:

- `aliases`

### GET /api/projects/<project_id>/notes

Returns notes ordered by `created_at` descending.

### POST /api/projects/<project_id>/notes

Creates a note.

Required fields:

- `title`
- `body`

Optional fields:

- `tags`

### POST /api/projects/<project_id>/agent-logs

Creates an agent work log.

This endpoint is recommended for MVP even though it was not in the initial required endpoint list, because `agent_logs` is a required MVP table and the Web UI needs a write path.

Required fields:

- `summary`

Optional fields:

- `agent_name`
- `changed_files`
- `checks_run`
- `known_issues`
- `next_task`

### GET /api/projects/<project_id>/agent-logs

Returns agent logs ordered by `created_at` descending.

This endpoint is recommended for symmetry with the write endpoint and the notes/agent log page.

### GET /api/projects/<project_id>/export/context.md

Returns AI-readable Markdown as `text/markdown`.

Export order:

1. Project summary
2. Canonical context entries
3. Accepted decisions
4. Proposed decisions
5. Open questions
6. Deferred questions
7. Glossary terms
8. Recent notes
9. Recent agent logs

Answered questions and superseded decisions are excluded by default from export unless a later export profile explicitly includes historical records.

## 4. Web UI Screens

The MVP Web UI is server-rendered Flask templates with vanilla HTML/CSS/JavaScript.

### Project List

Purpose: Show all projects and allow creating a new project.

Core elements:

- Project table/list.
- Create project form.
- Links to project dashboards.

### Project Dashboard

Purpose: Give a project-level overview and navigation.

Core elements:

- Project name and description.
- Counts for context entries, decisions, open questions, glossary terms, notes, and agent logs.
- Links to all project memory sections.
- Link to export page.

### Context Page

Purpose: Manage canonical context entries.

Core elements:

- Ordered list of context sections.
- Create/edit form.
- Fields for section, title, body, and position.

### Decisions Page

Purpose: Manage product and technical decisions.

Core elements:

- Decision list grouped or filterable by status.
- Create/edit form.
- Fields for title, status, decision, rationale, consequences, and superseded decision.

### Open Questions Page

Purpose: Track unresolved, deferred, and answered questions.

Core elements:

- Question list grouped or filterable by status.
- Create/edit form.
- Fields for title, status, question, context, and answer.

### Glossary Page

Purpose: Manage project-specific terms.

Core elements:

- Alphabetical glossary list.
- Create/edit form.
- Fields for term, definition, and aliases.

### Notes / Agent Log Page

Purpose: Capture general notes and agent work logs.

Core elements:

- Recent notes list.
- Recent agent logs list.
- Create note form.
- Create agent log form.

### Export Page

Purpose: Preview and access AI-readable context.

Core elements:

- Preview of generated Markdown.
- Link to `GET /api/projects/<project_id>/export/context.md`.
- Explanation of what sections are included.

## 5. File Structure

Initial repository structure:

```text
agent-project-memory/
  AGENTS.md
  CONTEXT.md
  DECISIONS.md
  GLOSSARY.md
  MVP_SPEC.md
  OPEN_QUESTIONS.md
  README.md
  ROADMAP.md
  STATUS.md
  TASKS.md
  pyproject.toml
  .gitignore
  src/
    agent_project_memory/
      __init__.py
      app.py
      config.py
      db.py
      schema.sql
      repositories.py
      export.py
      routes/
        __init__.py
        api.py
        web.py
      templates/
        base.html
        projects.html
        project_dashboard.html
        context.html
        decisions.html
        questions.html
        glossary.html
        notes_logs.html
        export.html
      static/
        styles.css
        app.js
  tests/
    test_db.py
    test_repositories.py
    test_api.py
    test_export.py
```

Notes:

- `README.md`, `.gitignore`, and `pyproject.toml` are part of implementation setup, not this specification task.
- Keep templates simple and server-rendered.
- Keep JavaScript optional and progressively enhanced.

## 6. Completion Criteria

The MVP is complete when all of the following are true:

- A user can initialize a local SQLite database.
- A user can run the Flask app locally.
- A user can create and view projects.
- A user can create and view context entries, decisions, open questions, glossary terms, notes, and agent logs.
- A user can export AI-readable Markdown context for a project.
- The required API endpoints work locally.
- The Web UI provides the required screens.
- Database behavior is covered by tests.
- Export behavior is covered by tests.
- API health and core create/list endpoints are covered by tests.
- The app works without login, cloud services, GitHub integration, or LLM API calls.
- Documentation explains how to install, run, and use the MVP.

## 7. First 10 Implementation Tasks

These tasks should be reflected in `TASKS.md` in priority order.

1. Create basic Python project structure.
2. Add project metadata and minimal dependencies.
3. Add SQLite schema.
4. Add database connection and initialization workflow.
5. Implement repository/data access functions for projects and core memory records.
6. Add tests for database initialization and repository operations.
7. Create minimal Flask app and health API endpoint.
8. Implement project list/create/detail API endpoints.
9. Implement core memory create/list API endpoints.
10. Implement AI-readable Markdown export and tests.


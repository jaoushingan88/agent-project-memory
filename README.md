# agent-project-memory

Local-first project memory for human maintainers and AI coding agents.

## Current State

This repository is in MVP implementation. The current app includes:

- `GET /`
- `GET /api/health`
- Local SQLite initialization
- Project API endpoints
- Core memory create/list API endpoints
- AI-readable `context.md` export

The full MVP is not implemented yet.

## MVP Feature Overview

`agent-project-memory` stores local project memory in SQLite and exposes it through a local Flask app.

Current MVP features:

- Projects
- Canonical context entries
- Decisions
- Open questions
- Glossary terms
- Notes
- Agent work logs
- AI-readable Markdown context export

Deferred from MVP:

- Accounts
- Cloud sync
- GitHub integration
- LLM API calls
- Authentication

## Requirements

- Python 3.11 or newer
- `pip`

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the package with development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Optional: copy environment defaults:

```powershell
Copy-Item .env.example .env
```

`requirements.txt` is kept for simple runtime installs and delegates to `pyproject.toml`:

```powershell
python -m pip install -r requirements.txt
```

## Initialize Database

Initialize the local SQLite database:

```powershell
python app.py --init-db
```

This creates the MVP schema for projects, context entries, decisions, open questions, glossary terms, notes, and agent logs. The command is safe to run more than once.

After editable installation, the console script can also be used:

```powershell
agent-project-memory --init-db
```

If the Python scripts directory is not on `PATH`, use:

```powershell
python -m agent_project_memory --init-db
```

Flask's local CLI command is also available:

```powershell
python -m flask --app agent_project_memory.app init-db
```

Seed demo data for manual smoke testing:

```powershell
python -m flask --app agent_project_memory.app seed-demo
```

## Run

Start the local app:

```powershell
python app.py
```

Or, after editable installation:

```powershell
agent-project-memory
```

If the Python scripts directory is not on `PATH`, use:

```powershell
python -m agent_project_memory
```

Open:

- Web UI: `http://127.0.0.1:5000/`
- Health API: `http://127.0.0.1:5000/api/health`

## Test

Run the test suite:

```powershell
python -m pytest
```

## API Examples

Health:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/health"
```

Create a project:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"name":"Agent Project Memory","slug":"agent-project-memory","description":"Local-first project memory."}'
```

List projects:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/projects"
```

Get a project:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/projects/1"
```

Create a context entry:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/context" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"section":"summary","title":"Summary","body":"Canonical project context.","position":1}'
```

Create a decision:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/decisions" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title":"Use SQLite","status":"accepted","decision":"Use SQLite for local-first MVP storage."}'
```

Create an open question:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/questions" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title":"Export scope","status":"open","question":"What should the first export include?"}'
```

Create a glossary term:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/glossary" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"term":"Canonical Context","definition":"The current authoritative project context."}'
```

Create a note:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/notes" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"title":"MVP note","body":"Keep the MVP small."}'
```

Create an agent log:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:5000/api/projects/1/agent-logs" `
  -Method Post `
  -ContentType "application/json" `
  -Body '{"agent_name":"Codex","summary":"Completed a focused task.","checks_run":"python -m pytest"}'
```

Export AI-readable context:

```powershell
Invoke-WebRequest `
  -Uri "http://127.0.0.1:5000/api/projects/1/export/context.md" `
  -OutFile "context.md"
```

## AI-Readable Export Format

The `context.md` export is deterministic Markdown intended for humans and coding agents to read before work.

It uses this section order:

1. Project overview
2. Canonical context
3. Decisions
4. Open questions
5. Glossary
6. Notes
7. Agent logs

Included by default:

- All canonical context entries, ordered for display/export.
- Decisions with `accepted` or `proposed` status.
- Questions with `open` or `deferred` status.
- All glossary terms.
- Notes in newest-first order.
- Agent logs in newest-first order.

Excluded by default:

- Decisions with `superseded` status.
- Questions with `answered` status.

## Local Data

By default, the SQLite database is created at:

```text
.agent-project-memory/memory.sqlite
```

Override it with:

```powershell
$env:APPM_DATABASE_PATH="path\to\memory.sqlite"
python app.py --init-db
```

## Project Structure

```text
.
├── app.py
├── pyproject.toml
├── requirements.txt
├── src/
│   └── agent_project_memory/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app.py
│       ├── db.py
│       └── templates/
│           └── index.html
└── tests/
    ├── test_app.py
    └── test_db.py
```

The current structure intentionally remains small. Full MVP CRUD, export, and Web UI screens are planned in later tasks.

# agent-project-memory

Local-first project memory for human maintainers and AI coding agents.

## Current State

This repository is in the first implementation phase. The current app is a minimal Flask + SQLite skeleton with:

- `GET /`
- `GET /api/health`
- Local SQLite initialization

The full MVP is not implemented yet.

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

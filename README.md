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

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Optional: copy environment defaults:

```powershell
Copy-Item .env.example .env
```

## Run

Initialize the local SQLite database:

```powershell
python app.py --init-db
```

Start the local app:

```powershell
python app.py
```

Open:

- Web UI: `http://127.0.0.1:5000/`
- Health API: `http://127.0.0.1:5000/api/health`

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


# Contributing to agent-project-memory

Thank you for considering a contribution to `agent-project-memory`.

This project is a local-first project memory tool for human maintainers and AI coding agents. Keep contributions small, reviewable, and aligned with the existing MVP direction.

## Development Setup

Requirements:

- Python 3.11 or newer
- `pip`

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the package with development dependencies:

```powershell
python -m pip install -e ".[dev]"
```

Initialize the local SQLite database when you need to run the app manually:

```powershell
python -m agent_project_memory --init-db
```

Run the local app:

```powershell
python -m agent_project_memory
```

If you prefer the top-level script, this also works:

```powershell
python app.py
```

## Running Tests

Run the full test suite before opening a PR:

```powershell
python -m pytest
```

Do not report tests as passing unless you actually ran them. If a test fails, either fix the issue or describe the failure clearly in the PR.

## Project Control Documents

Before making changes, read:

- `AGENTS.md`
- `CONTEXT.md`
- `DECISIONS.md`
- `TASKS.md`
- `STATUS.md`
- `OPEN_QUESTIONS.md`
- `GLOSSARY.md`

For longer autonomous or agent-assisted sessions, also read:

- `AUTONOMY.md`
- `QUALITY_GATE.md`

Before considering a task complete, check `QUALITY_GATE.md`.

After completing work:

- Update `TASKS.md` when a task is completed or blocked.
- Update `STATUS.md` with the summary, changed files, checks run, known issues, and recommended next task.
- Update `DECISIONS.md` only for durable product or technical decisions.
- Update `OPEN_QUESTIONS.md` when a product, technical, or UX ambiguity remains unresolved.

## One Task, One Commit

Each commit should have one purpose.

Good examples:

- `Add glossary API tests`
- `Fix context export ordering`
- `Update README setup notes`

Avoid mixing unrelated changes such as UI edits, API behavior, documentation rewrites, and refactors in the same commit.

Do not commit generated local artifacts:

- `.agent-project-memory/`
- SQLite database files
- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `*.egg-info/`

## Issues

Use issues for bugs, small feature proposals, documentation gaps, and open design questions.

Good issues include:

- Expected behavior
- Actual behavior
- Reproduction steps, when relevant
- Environment details, when relevant
- Links to related `TASKS.md`, `STATUS.md`, or `OPEN_QUESTIONS.md` entries

For large product or architecture changes, start with an issue before implementation.

## Pull Requests

Keep PRs focused and easy to review.

Each PR should include:

- A short summary of the change
- The task or issue it addresses
- Tests or checks run
- Known limitations or follow-up tasks
- Screenshots only when UI changes need visual review

PRs should not introduce MVP-deferred features such as accounts, cloud sync, LLM API calls, GitHub integration, realtime collaboration, Docker, or frontend frameworks unless the project direction has explicitly changed and the decision is documented.

## Agent-Assisted Contributions

AI coding agents are welcome, but their output must follow the same rules as human contributions.

Agent-assisted work must:

- Read the required control documents before changes.
- Follow `TASKS.md` priority unless the maintainer directs otherwise.
- Keep changes small.
- Run relevant tests.
- Avoid invented command output or fabricated verification.
- Update `STATUS.md` and `TASKS.md` after the work.

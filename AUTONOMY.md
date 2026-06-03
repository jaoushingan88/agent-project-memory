# AUTONOMY.md

Rules for long-running autonomous Codex sessions in `agent-project-memory`.

Autonomy is allowed only inside the project direction already defined by `AGENTS.md`, `CONTEXT.md`, `DECISIONS.md`, `TASKS.md`, `ROADMAP.md`, and `MVP_SPEC.md`.

## Required Reading

Before a long-running autonomous session, read:

- `AGENTS.md`
- `AUTONOMY.md`
- `QUALITY_GATE.md`
- `CONTEXT.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`
- `STATUS.md`
- `OPEN_QUESTIONS.md`
- `GLOSSARY.md`
- `MVP_SPEC.md`

Do not rely on chat history as the source of truth.

## Task Selection

1. Choose the highest-priority `todo` task in `TASKS.md` that is not blocked.
2. Prefer P1 tasks until the MVP foundation is complete.
3. Do not start from `BACKLOG.md` while clear unfinished `TASKS.md` items exist.
4. If a task is too large, split it into smaller `TASKS.md` items before implementation.
5. If the next task is ambiguous, record the ambiguity in `OPEN_QUESTIONS.md`, mark the task `blocked`, and stop.

## Per-Task Loop

For each task:

1. Read the relevant specs and current code.
2. Implement only that task.
3. Run relevant tests or a focused startup/API check.
4. If tests fail, debug inside the same task.
5. If the failure cannot be resolved, update `STATUS.md` and `OPEN_QUESTIONS.md`, then stop.
6. Check `QUALITY_GATE.md`.
7. Update `TASKS.md`.
8. Update `STATUS.md`.
9. Update `DECISIONS.md` if a durable product or technical decision was made.
10. Check `git status --short --ignored`.
11. Check `git diff --stat`.
12. Remove or ignore generated files, caches, virtualenvs, and local DB files.
13. Commit exactly one task with a concise English message.

## Commit Rules

- One commit must have one purpose.
- Do not mix unrelated documentation, API, UI, and refactor work unless the selected task explicitly requires them.
- Do not commit `.agent-project-memory/`, SQLite DB files, `.venv/`, `__pycache__/`, `.pytest_cache/`, build outputs, or egg-info metadata.
- Do not commit generated local artifacts unless the task is explicitly about committed examples or fixtures.

## Stop Conditions

Stop autonomous work when:

- The requested task limit is reached.
- Tests fail and cannot be fixed within the current task.
- The implementation requires a product decision not covered by existing docs.
- A task conflicts with `DECISIONS.md` or `MVP_SPEC.md`.
- A dependency addition seems necessary.
- The next task would require building a feature outside the MVP.

## When Tasks Run Out

If `TASKS.md` has no clear `todo` task:

1. Read `MVP_SPEC.md` and `ROADMAP.md`.
2. Generate the next smallest useful MVP task.
3. Add it to `TASKS.md`.
4. Do not add large speculative features.
5. Do not pull from `BACKLOG.md` unless it directly supports the MVP milestone.


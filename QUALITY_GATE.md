# QUALITY_GATE.md

Quality gate for each completed task in `agent-project-memory`.

Before marking a task done or committing, check every applicable item below.

## Scope

- The change implements exactly the selected task.
- No specification-outside features were added.
- No GitHub integration, LLM API, auth, cloud sync, Docker, realtime, or frontend framework was added for the MVP.
- The product concept remains unchanged.

## Tests And Verification

- Relevant tests pass.
- Existing tests are not broken.
- If no automated test is relevant, a startup check or API check was run.
- Failed tests are not ignored or described as passing.
- The command output recorded in `STATUS.md` matches what was actually run.

## Data And API Behavior

- SQLite initialization remains local-first and idempotent.
- Foreign keys remain enabled for DB operations.
- API responses use consistent JSON shapes.
- API errors have clear status codes and response bodies.
- Markdown export output remains deterministic where relevant.

## Documentation

- `STATUS.md` was updated with summary, changed files, checks, known issues, and next task.
- `TASKS.md` was updated when a task was completed or blocked.
- `DECISIONS.md` was updated for durable decisions.
- `OPEN_QUESTIONS.md` was updated for unresolved ambiguity.
- `README.md` was updated when setup, commands, API usage, or user workflow changed.

## Git Hygiene

- `git status --short --ignored` was checked.
- `git diff --stat` or `git diff --cached --stat` was checked.
- Generated DB files are not staged.
- Caches are not staged.
- Virtual environments are not staged.
- Build outputs and egg-info metadata are not staged.
- The commit contains one purpose only.

## Reviewability

- Changes are small enough to review.
- Names are explicit and consistent with existing code.
- New helpers remove real duplication or clarify boundaries.
- Error handling is understandable.
- No heavy dependency was added.


# AGENTS.md

Rules for AI coding agents working on `agent-project-memory`.

`agent-project-memory` is a serious OSS project. Treat this repository as a long-lived codebase, not a one-off prototype. The purpose of these rules is to keep future Codex, Gemini, Claude, Cursor agents, and human maintainers aligned across sessions.

## Required Reading Before Changes

Before making any change, read these files in full:

- `AGENTS.md`
- `CONTEXT.md`
- `DECISIONS.md`
- `TASKS.md`
- `STATUS.md`
- `OPEN_QUESTIONS.md`
- `GLOSSARY.md`

Do not rely only on chat history. Repository files are the source of truth.

For long-running autonomous sessions, also read:

- `AUTONOMY.md`
- `QUALITY_GATE.md`

## Core Rules

1. Always read `AGENTS.md`, `CONTEXT.md`, `DECISIONS.md`, `TASKS.md`, `STATUS.md`, `OPEN_QUESTIONS.md`, and `GLOSSARY.md` before change work.
2. Do not change the product concept casually. If a concept change seems necessary, record it as a proposal in `DECISIONS.md` instead of silently implementing it.
3. Choose tasks from `TASKS.md` in priority order unless the user explicitly directs otherwise or a blocking dependency requires a different order.
4. Keep changes small, focused, and easy to review.
5. Do not add heavy dependencies. If a dependency is added, record the reason in `DECISIONS.md`.
6. Do not fabricate tests, command outputs, benchmark results, or manual verification.
7. If something is ambiguous, do not proceed by hidden assumption. Record the ambiguity in `OPEN_QUESTIONS.md` and either ask the user or make a clearly documented temporary assumption.
8. After each work session, update `STATUS.md` with:
   - Summary
   - Changed files
   - Tests/checks run
   - Known issues
   - Recommended next task
9. When a task is completed or blocked, update `TASKS.md`.
10. Preserve local-first and repository-friendly design.
11. Prefer simple technology for the MVP.
12. Do not build unrelated features.
13. The first MVP must focus on project memory, decisions, open questions, glossary, notes, and AI-readable context export.
14. In long-running autonomous sessions, always read `AUTONOMY.md` and `QUALITY_GATE.md`.
15. If `TASKS.md` has clear unfinished tasks, do not start large new features from `BACKLOG.md`.
16. Before completing each task, check `QUALITY_GATE.md`.
17. If any test fails, do not continue to the next task.
18. If debugging cannot resolve a failure, update `STATUS.md` and `OPEN_QUESTIONS.md`, then stop.
19. Keep each commit to one purpose.
20. If autonomous work runs out of tasks, generate the next small MVP task from `MVP_SPEC.md` and `ROADMAP.md`, add it to `TASKS.md`, and avoid large specification-outside features.

## MVP Technology Constraints

The initial MVP uses:

- Python
- Flask
- SQLite
- Vanilla HTML/CSS/JavaScript
- Local-first storage
- No account system
- No cloud sync
- No LLM API dependency

Do not introduce a frontend framework, cloud service, background worker system, vector database, authentication provider, or LLM integration for the MVP unless the decision is explicitly approved and documented.

## Work Style

- Prefer boring, maintainable code.
- Keep data formats understandable in Git diffs.
- Favor explicit names over clever abstractions.
- Make file layout obvious to new contributors.
- Write tests for behavior that can regress.
- Use documentation to preserve context, not to hide incomplete design.

## Source Of Truth Order

When information conflicts, use this order:

1. Explicit user instruction in the current session
2. `DECISIONS.md`
3. `CONTEXT.md`
4. `TASKS.md`
5. `STATUS.md`
6. Other repository documentation
7. Chat history

If conflict remains unresolved, record it in `OPEN_QUESTIONS.md`.

## Session Exit Checklist

Before ending a development session:

- Ensure implemented work matches the selected task.
- Run relevant tests or checks, or state why they were not run.
- Update `STATUS.md`.
- Update `TASKS.md` if task state changed.
- Add new unresolved issues to `OPEN_QUESTIONS.md`.
- Add new permanent decisions to `DECISIONS.md`.

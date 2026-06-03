# TASKS.md

## Task States

Use these states:

- `todo`: Not started.
- `in_progress`: Currently being worked on.
- `blocked`: Cannot proceed until an open question or dependency is resolved.
- `done`: Completed and verified.

When task state changes, update this file in the same work session.

## Priority 0: Project Control

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P0-001 | done | Create project control documents | Initial repository memory files created before app implementation. |

## Priority 1: MVP Foundation

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P1-001 | done | Create basic Python project structure | Added top-level `app.py`, `src/agent_project_memory/`, minimal template, README setup notes, `.gitignore`, `.env.example`, and `requirements.txt`. |
| P1-002 | done | Add project metadata and minimal dependencies | Added `pyproject.toml`, dev dependency group with pytest, package config, pytest config, README setup commands, and initial tests. |
| P1-003 | done | Add SQLite schema | Added full MVP schema from `MVP_SPEC.md` with projects, context_entries, decisions, open_questions, glossary_terms, notes, agent_logs, indexes, foreign keys, and schema tests. |
| P1-004 | done | Add database connection and initialization workflow | Added Flask-aware database connection lifecycle, row access by name, app teardown close handling, and `init-db` Flask CLI command. |
| P1-005 | done | Implement repository/data access functions | Added simple create/get/list repository functions for projects and all MVP memory record types. |
| P1-006 | done | Add database and repository tests | Added repository tests for create/get/list flows, ordering, timestamps, duplicate project slugs, and invalid decision status boundaries. |
| P1-007 | done | Create minimal Flask app and health API endpoint | Existing app factory, `GET /`, `GET /api/health`, tests, and startup check verified. |
| P1-008 | done | Implement project API endpoints | Added `GET /api/projects`, `POST /api/projects`, `GET /api/projects/<project_id>`, JSON errors, and API tests. |
| P1-009 | todo | Implement core memory create/list API endpoints | Add context, decisions, questions, glossary, notes, and agent log endpoints. |
| P1-010 | todo | Implement AI-readable Markdown export and tests | Add `GET /api/projects/<project_id>/export/context.md` with deterministic formatting. |
| P1-011 | todo | Add API error handling consistency | Standardize JSON error bodies and status codes for validation failures, missing records, and database constraint errors. |
| P1-012 | todo | Add README API examples | Document local API examples for health, projects, memory records, and context export. |
| P1-013 | todo | Add seed demo data workflow | Provide a small local-only demo dataset for manual MVP smoke testing. |
| P1-014 | todo | Add final MVP API smoke test | Cover health, project creation, memory record creation, and context export in one focused test. |

## Priority 2: MVP Web UI

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P2-001 | todo | Add base layout and navigation templates | Use vanilla HTML/CSS and server-rendered Flask templates. |
| P2-002 | todo | Add project list and create screen | Include links to project dashboards. |
| P2-003 | todo | Add project dashboard screen | Show counts and navigation for memory sections. |
| P2-004 | todo | Add context page | Create and list canonical context entries. |
| P2-005 | todo | Add decisions page | Create and list decisions by status. |
| P2-006 | todo | Add open questions page | Create and list open, deferred, and answered questions. |
| P2-007 | todo | Add glossary page | Create and list glossary terms alphabetically. |
| P2-008 | todo | Add notes / agent log page | Create and list notes plus agent work logs. |
| P2-009 | todo | Add export page | Preview generated Markdown and link to export endpoint. |
| P2-010 | todo | Add basic forms for MVP entities | Ensure each MVP entity can be created from the Web UI without large UI expansion. |
| P2-011 | todo | Add final MVP UI smoke test | Verify the minimal dashboard and entity creation flow manually or with a small automated smoke test. |

## Priority 3: Context Export

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P3-001 | todo | Define AI-readable export format | Document section order and included record states. |
| P3-002 | todo | Implement Markdown context export | Generate deterministic output for agents. |
| P3-003 | todo | Add export tests | Verify ordering, escaping, and inclusion rules. |
| P3-004 | todo | Add UI action to export context | Keep it local and explicit. |

## Priority 4: Local API And OSS Readiness

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P4-001 | todo | Add read-only local REST API endpoints | Useful for AI agents and scripts. |
| P4-002 | todo | Add write API endpoints for selected record types | Do this only after data model stabilizes. |
| P4-003 | todo | Write README | Include install, run, and first workflow. |
| P4-004 | todo | Add license | Choose before accepting external contributions. |
| P4-005 | todo | Add contribution guide | Include agent rules and status update expectations. |
| P4-006 | todo | Add CI for tests | Keep it lightweight. |

## Current Recommended Next Task

Start with `P1-009`: implement core memory create/list API endpoints.

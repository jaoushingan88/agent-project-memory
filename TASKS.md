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
| P1-009 | done | Implement core memory create/list API endpoints | Added create/list APIs and tests for context, decisions, questions, glossary, notes, and agent logs. |
| P1-010 | done | Implement AI-readable Markdown export and tests | Added deterministic Markdown export endpoint and tests covering included and excluded sections. |
| P1-011 | done | Add API error handling consistency | Standardized JSON error bodies with message/status fields and added tests for 400, 404, and 405 behavior. |
| P1-012 | done | Add README API examples | Added MVP feature overview and PowerShell API examples for health, projects, memory records, agent logs, and context export. |
| P1-013 | done | Add seed demo data workflow | Added local `seed-demo` Flask CLI command, demo project data, README note, and tests. |
| P1-014 | done | Add final MVP API smoke test | Added end-to-end API smoke test for health, project creation, all memory record creation, and context export. |

## Priority 2: MVP Web UI

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P2-001 | done | Add base layout and navigation templates | Added base template, shared CSS, navigation, and index template inheritance. |
| P2-002 | done | Add project list and create screen | Added Web UI project creation form, project list, dashboard links, and tests. |
| P2-003 | done | Add project dashboard screen | Added dashboard counts, section navigation, and context export link. |
| P2-004 | done | Add context page | Added context list/create Web UI and dashboard links. |
| P2-005 | done | Add decisions page | Added decisions list/create Web UI and dashboard links. |
| P2-006 | done | Add open questions page | Added open questions list/create Web UI and dashboard links. |
| P2-007 | done | Add glossary page | Added glossary list/create Web UI and dashboard links. |
| P2-008 | done | Add notes / agent log page | Added combined notes and agent logs list/create Web UI and dashboard links. |
| P2-009 | done | Add export page | Added Web UI export preview and context.md download link. |
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

Start with `P2-010`: add basic forms for MVP entities.

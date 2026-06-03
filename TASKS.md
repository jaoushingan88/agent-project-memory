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
| P2-010 | done | Add basic forms for MVP entities | Verified forms exist for projects, context entries, decisions, open questions, glossary terms, notes, and agent logs. |
| P2-011 | done | Add final MVP UI smoke test | Added end-to-end Web UI smoke test for project creation, all MVP entity forms, dashboard, and export preview. |

## Priority 3: Context Export

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P3-001 | done | Define AI-readable export format | Documented section order and included/excluded record states in `README.md`. |
| P3-002 | done | Implement Markdown context export | Existing `GET /api/projects/<project_id>/export/context.md` renders deterministic Markdown through `export.py`. |
| P3-003 | done | Add export tests | Added export section-order coverage; existing tests cover inclusion and exclusion rules. |
| P3-004 | done | Add UI action to export context | Existing dashboard and export page link to preview/download context; tests now assert export link targets. |

## Priority 4: Local API And OSS Readiness

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P4-001 | done | Add read-only local REST API endpoints | Existing local REST API provides read endpoints for projects, MVP memory records, agent logs, and context export. |
| P4-002 | done | Add write API endpoints for selected record types | Existing local REST API provides POST endpoints for projects, MVP memory records, and agent logs with tests. |
| P4-003 | done | Write README | Updated README with current MVP state, install/run/test/API examples, Web UI workflow, export format, local data, and current structure. |
| P4-004 | done | Add license | Added MIT `LICENSE`, README license section, and package license metadata. |
| P4-005 | todo | Add contribution guide | Include agent rules and status update expectations. |
| P4-006 | todo | Add CI for tests | Keep it lightweight. |

## Priority 5: MVP Completion

| ID | State | Task | Notes |
| --- | --- | --- | --- |
| P5-001 | done | Run final MVP completion audit | Verified API, data model, context export, Web UI, tests, docs, and Git hygiene against the goal completion criteria. |
| P5-002 | done | Run post-MVP audit | Re-ran README setup, tests, init-db, app startup, API checks, Web UI form flow, export check, and fixed stale MVP spec details. |

## Current Recommended Next Task

After MIT licensing is in place, start with `P4-005`: add a contribution guide.

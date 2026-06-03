# ROADMAP.md

## Roadmap

This roadmap moves `agent-project-memory` from project control documents to a practical local-first OSS tool.

## Milestone 0: Repository Control Documents

Goal: Establish project memory and agent operating rules before implementation begins.

Deliverables:

- `AGENTS.md`
- `CONTEXT.md`
- `ROADMAP.md`
- `TASKS.md`
- `DECISIONS.md`
- `STATUS.md`
- `OPEN_QUESTIONS.md`
- `GLOSSARY.md`

Exit criteria:

- Future agents can understand the project goal, constraints, and next tasks without relying on chat history.

## Milestone 1: Minimal Local Data Model

Goal: Define and validate the core memory model.

Deliverables:

- SQLite schema for canonical context, decisions, open questions, glossary terms, notes, and agent work logs.
- Python data access layer.
- Basic migration/init command.
- Tests for create/read/update/list behavior.

Exit criteria:

- A local database can be initialized and core record types can be persisted and retrieved.

## Milestone 2: Minimal Flask Web UI

Goal: Provide a usable local interface for maintaining project memory.

Deliverables:

- Flask app entry point.
- Server-rendered list/detail/create/edit pages for core record types.
- Basic navigation.
- Minimal vanilla CSS.
- Form validation with useful error messages.

Exit criteria:

- A maintainer can manage MVP memory records locally through a browser.

## Milestone 3: AI-Readable Context Export

Goal: Generate a compact, reliable Markdown context file for coding agents.

Deliverables:

- Deterministic export command or endpoint.
- Export sections for canonical context, active decisions, open questions, glossary, recent notes, and recent agent logs.
- Tests for export ordering and formatting.

Exit criteria:

- An agent can read one exported Markdown file before work and understand the current project state.

## Milestone 4: Local REST API

Goal: Allow AI agents and local tools to query project memory programmatically.

Deliverables:

- Read endpoints for core record types.
- Write endpoints for notes, decisions, open questions, glossary, and logs.
- Simple API documentation.
- Tests for API behavior.

Exit criteria:

- Local tools can integrate with the memory store without scraping HTML.

## Milestone 5: OSS Readiness

Goal: Make the project usable and contributable by external maintainers.

Deliverables:

- README with installation and usage.
- Example project memory.
- Contribution guide.
- License.
- Basic packaging strategy.
- CI for tests and formatting.

Exit criteria:

- A new user can clone the repo, run the tool, and understand how to contribute.

## Milestone 6: Practical Integrations

Goal: Add integrations only after the local MVP is stable.

Candidate deliverables:

- Markdown import/export improvements.
- GitHub Issues/PR linking.
- Agent-specific context profiles.
- CLI commands.
- Backup/export workflow.

Exit criteria:

- Integrations improve local-first workflows without turning the project into a hosted platform.


# OPEN_QUESTIONS.md

## Open Questions

Record unresolved product, technical, and UX questions here. Do not bury uncertainty in chat history.

## Product Questions

### OQ-001: Should canonical context be one record or multiple sections?

Question: Should the MVP store canonical context as a single editable document, or as structured sections such as summary, goals, non-goals, architecture, and constraints?

Why it matters: A single document is simpler, but structured sections may produce better AI-readable exports.

Status: Open.

### OQ-002: What is the minimum useful agent work log format?

Question: What fields should an agent work log require in the MVP?

Candidate fields: timestamp, agent/tool name, summary, changed files, tests/checks, known issues, next recommendation.

Status: Open.

### OQ-003: Should resolved open questions remain visible by default?

Question: Should the UI and exports show resolved questions by default, or only active open questions?

Why it matters: Resolved questions can preserve rationale, but too much resolved history may clutter agent context.

Status: Open.

## Technical Questions

### OQ-004: Should migrations use a tiny custom migration table or a dependency?

Question: For the MVP, should schema changes be handled by a simple custom migration mechanism or by adding a migration library?

Current leaning: Use a tiny custom migration table first to avoid unnecessary dependency weight.

Status: Open.

### OQ-005: Where should the default SQLite database live?

Question: Should the default database path be inside the repository, inside a hidden project directory, or configured by environment variable?

Candidate options:

- `./.agent-project-memory/memory.sqlite`
- `./memory.sqlite`
- User-specified path through config or environment variable

Status: Open.

### OQ-006: Should Markdown exports be committed?

Question: Should generated AI-readable context exports be intended for committing to Git, or treated as local generated artifacts?

Why it matters: Committed exports improve reviewability, but generated files can become stale.

Status: Open.

## UX Questions

### OQ-007: Should the MVP start with Web UI only, CLI only, or both?

Question: The stated direction includes a simple Web UI, but should the earliest implementation expose a CLI for database initialization and export before full UI CRUD?

Current leaning: Add minimal command functions for initialization/export while keeping the main user workflow in the Web UI.

Status: Open.

### OQ-008: What should the first export profile include?

Question: Should AI-readable export include all records, only active/current records, or a bounded recent history?

Current leaning: Include canonical context, accepted decisions, open questions, glossary, and recent notes/logs with deterministic ordering.

Status: Open.


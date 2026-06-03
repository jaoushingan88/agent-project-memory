# CONTEXT.md

## Project

Name: `agent-project-memory`

One-line description: Local-first project memory for human maintainers and AI coding agents.

## Problem

AI coding agents can write code, review changes, and generate documentation. In long-running projects, they often lose context between sessions.

Important project knowledge becomes scattered across:

- Decisions
- Assumptions
- Open questions
- Glossary terms
- Architecture direction
- Previous AI agent work logs
- Current and outdated specifications
- Chat messages, IDE notes, terminals, issues, docs, and ad hoc files

When this knowledge is fragmented, Codex, Gemini, Claude, Cursor, and human maintainers may work from stale assumptions or incorrect interpretations.

## Product Concept

`agent-project-memory` stores a project's correct working memory in a local-first, repository-friendly format.

It helps maintainers and agents capture, update, inspect, and export:

- Canonical context
- Decisions
- Open questions
- Glossary terms
- Notes
- Agent work logs

The system should make it easy for AI coding agents and human maintainers to read the current project context before starting work.

## Target Users

- Human maintainers of long-lived software projects
- Solo developers using AI coding agents across many sessions
- OSS maintainers coordinating agent-assisted contributions
- Teams that want project memory stored alongside code
- AI coding agents that need a compact, reliable context export before making changes

## Core Use Cases

- Record why a product or technical decision was made.
- Track unresolved questions without burying them in chat history.
- Maintain a glossary of project-specific terms.
- Keep canonical project context separate from transient discussion.
- Store notes and agent work logs in a reviewable local database.
- Export AI-readable context before an agent starts coding.
- Preserve project memory in Git-friendly files and/or export formats.

## Non-Goals For MVP

- No hosted SaaS.
- No cloud sync.
- No user accounts.
- No multi-user permission system.
- No LLM API integration.
- No semantic search or vector database.
- No complex project management suite.
- No GitHub Issues or PR automation in MVP.
- No plugin ecosystem in MVP.
- No replacement for full documentation sites.

## Initial MVP Scope

The first MVP focuses on:

- Project memory records
- Decisions
- Open questions
- Glossary terms
- Notes
- Agent work logs
- AI-readable context export
- Simple local Web UI
- SQLite persistence
- Markdown export where useful

## Initial Technical Direction

The MVP should be implemented with:

- Python
- Flask
- SQLite
- Vanilla HTML/CSS/JavaScript
- Local file/database storage
- Simple server-rendered pages where practical
- Minimal dependencies

The product should run locally from a cloned repository and store project memory in a way that is understandable, inspectable, and friendly to version control.

## Architecture Direction

Expected high-level shape:

- Flask application for local Web UI and local REST endpoints.
- SQLite database for structured records.
- Export layer that generates AI-readable Markdown context.
- Simple templates and static assets.
- Tests around data operations and export behavior.

Keep the architecture modular enough to support future CLI/API features, but do not over-engineer before the MVP exists.

## Repository-Friendly Principles

- Prefer plain text exports.
- Keep generated context deterministic where possible.
- Avoid opaque binary state except for SQLite database files used locally.
- Make configuration explicit and simple.
- Avoid storing machine-specific absolute paths in committed files.
- Ensure important project memory can be reviewed in pull requests.

## Future Feature Candidates

- Project management
- Canonical context management
- Decisions management
- Open questions management
- Glossary management
- Notes and agent logs management
- AI-readable `context.md` export
- REST API for AI agents
- Simple Web UI
- Markdown export
- Future GitHub Issues/PR integration


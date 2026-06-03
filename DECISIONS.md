# DECISIONS.md

## Decision Log

This file records product and technical decisions that agents must not casually change. If a future change is needed, add a proposal or superseding decision with rationale.

## Accepted Decisions

### D-001: Product Name

Decision: The project is named `agent-project-memory`.

Rationale: The name directly describes the product: project memory designed for agents and maintainers.

Status: Accepted.

### D-002: Product Mission

Decision: The project provides local-first project memory for human maintainers and AI coding agents.

Rationale: Long-lived agent-assisted projects need a stable source of truth that survives chat/session boundaries.

Status: Accepted.

### D-003: MVP Technology Stack

Decision: The MVP uses Python, Flask, SQLite, and vanilla HTML/CSS/JavaScript.

Rationale: This stack is simple, familiar, local-first, easy to run, and appropriate for an OSS MVP.

Status: Accepted.

### D-004: Local-First MVP

Decision: The MVP has no accounts, no cloud sync, and no hosted dependency.

Rationale: The project must work from a local repository and preserve user control over project memory.

Status: Accepted.

### D-005: No LLM API Dependency In MVP

Decision: The MVP must not depend on an LLM API.

Rationale: The tool should store and export reliable context independently of any model provider.

Status: Accepted.

### D-006: MVP Scope Focus

Decision: The first MVP focuses on project memory, decisions, open questions, glossary, notes, agent work logs, and AI-readable context export.

Rationale: These are the core memory primitives needed to reduce context loss across agent sessions.

Status: Accepted.

### D-007: Repository-Friendly Memory

Decision: The project should prefer formats and workflows that can be inspected, reviewed, backed up, and versioned alongside code.

Rationale: The tool is meant to support maintainers and OSS workflows, not hide context in opaque remote systems.

Status: Accepted.

## Proposed Decisions

No pending proposals.

## Superseded Decisions

No superseded decisions.


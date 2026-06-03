# GLOSSARY.md

## Glossary

This glossary defines project-specific terms. Future agents should use these meanings consistently.

## Terms

### Agent Work Log

A structured record of work performed by an AI coding agent or automation. It should capture what changed, what was checked, known issues, and recommended next steps.

### AI-Readable Context

A compact export intended to be read by AI coding agents before work. It should summarize the current source of truth without requiring agents to inspect every historical note.

### Canonical Context

The current authoritative project context: what the project is, what it is not, who it serves, what constraints matter, and what architecture direction is currently accepted.

### Decision

A product or technical choice that should not be casually changed. Decisions should include rationale and status.

### Local-First

A design principle where the tool works locally without accounts, hosted services, cloud sync, or network dependencies for core MVP workflows.

### Note

A general memory entry that captures useful project information but is not necessarily a formal decision, open question, glossary term, or work log.

### Open Question

An unresolved product, technical, or UX issue that needs clarification. Open questions prevent hidden assumptions from becoming accidental design decisions.

### Project Memory

The durable collection of context, decisions, questions, glossary entries, notes, and work logs that helps humans and agents understand the project across sessions.

### Repository-Friendly

Designed so project memory can live near the code, be reviewed by maintainers, survive local workflows, and avoid unnecessary opaque or remote-only state.

### Source Of Truth

The most authoritative location for current project knowledge. In this repository, accepted decisions and control documents outrank chat history.


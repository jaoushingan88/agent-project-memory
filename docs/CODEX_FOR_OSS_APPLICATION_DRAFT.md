# Codex for OSS Application Draft

## Project Name

agent-project-memory

## Repository URL

https://github.com/jaoushingan88/agent-project-memory

## Short Description

Local-first project memory for human maintainers and AI coding agents.

## Problem Statement

AI coding agents are increasingly useful for implementing features, reviewing code, and producing documentation. The harder problem in long-running open-source projects is continuity: an agent often starts each session without the durable context behind past decisions, unresolved questions, terminology, architecture constraints, and previous agent work.

When this context is scattered across chats, issue comments, IDE notes, terminals, and partial documentation, both humans and agents can repeat old debates, follow stale assumptions, or make changes that do not match the current project direction.

## Why This Project Helps Open-Source Maintainers

`agent-project-memory` gives maintainers a small local tool for storing the current project memory in structured records:

- Canonical context
- Decisions
- Open questions
- Glossary terms
- Notes
- Agent work logs

The tool exports AI-readable Markdown so maintainers can give Codex or another coding agent a compact source of truth before a work session. This is especially useful for OSS projects where contributors, maintainers, and AI agents may interact asynchronously and need to understand what is currently true.

The MVP is local-first and repository-friendly. It avoids accounts, cloud sync, and LLM API dependencies so it can be evaluated and improved as a normal open-source tool.

## How Codex Will Be Used

Codex will be used as a development assistant for this repository in the same way the project is intended to support other repositories:

- Read the project control documents before making changes.
- Select focused tasks from `TASKS.md`.
- Implement small changes with tests.
- Update `STATUS.md` after each session.
- Preserve decisions and unresolved questions in the repository.
- Use the exported project context as a session primer for future work.

This creates a practical feedback loop: Codex helps build the tool, and the tool records the context Codex needs to continue working responsibly over time.

## Current Status

The project has an early MVP implemented and pushed to GitHub.

Current MVP capabilities:

- Flask Web UI
- SQLite persistence
- Project records
- Context entries
- Decisions
- Open questions
- Glossary terms
- Notes
- Agent work logs
- AI-readable `context.md` export
- Local REST API
- pytest test suite
- GitHub Actions CI

The repository also includes project control documents for future human and AI-assisted development.

## Future Roadmap

Near-term improvements:

- Improve project dashboard UX.
- Add stronger API documentation examples.
- Add release checklist workflow.
- Add broader Markdown export workflows.
- Improve context export profiles for different agent workflows.

Longer-term candidates:

- GitHub Issues import prototype.
- GitHub PR or issue linking.
- CLI export commands.
- More explicit project-memory review workflows.
- Optional import/export formats for maintainers who want to commit generated context files.

## Honest Early-Stage Note

This is an early-stage open-source project. The MVP is intentionally small and local-first. It is not yet a hosted service, a full project management system, or an AI automation platform.

The current value is narrow but concrete: it gives maintainers a structured place to store project memory and export it for humans and coding agents before work begins.

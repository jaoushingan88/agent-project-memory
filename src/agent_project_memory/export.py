from .repositories import (
    list_agent_logs,
    list_context_entries,
    list_decisions,
    list_glossary_terms,
    list_notes,
    list_open_questions,
)


def _append_optional(lines, label, value):
    if value:
        lines.append(f"- {label}: {value}")


def render_context_markdown(connection, project):
    lines = [
        f"# {project['name']} Context",
        "",
        "## Project Overview",
        "",
    ]

    _append_optional(lines, "Name", project["name"])
    _append_optional(lines, "Slug", project["slug"])
    _append_optional(lines, "Description", project.get("description"))
    _append_optional(lines, "Root path", project.get("root_path"))

    lines.extend(["", "## Canonical Context", ""])
    context_entries = list_context_entries(connection, project["id"])
    if context_entries:
        for entry in context_entries:
            lines.extend([f"### {entry['title']}", "", entry["body"], ""])
    else:
        lines.extend(["No canonical context entries recorded.", ""])

    accepted_decisions = [
        decision
        for decision in list_decisions(connection, project["id"])
        if decision["status"] == "accepted"
    ]
    proposed_decisions = [
        decision
        for decision in list_decisions(connection, project["id"])
        if decision["status"] == "proposed"
    ]

    lines.extend(["## Decisions", ""])
    if accepted_decisions or proposed_decisions:
        for decision in accepted_decisions + proposed_decisions:
            lines.extend(
                [
                    f"### [{decision['status']}] {decision['title']}",
                    "",
                    decision["decision"],
                    "",
                ]
            )
            if decision.get("rationale"):
                lines.extend([f"Rationale: {decision['rationale']}", ""])
            if decision.get("consequences"):
                lines.extend([f"Consequences: {decision['consequences']}", ""])
    else:
        lines.extend(["No active decisions recorded.", ""])

    active_questions = [
        question
        for question in list_open_questions(connection, project["id"])
        if question["status"] in {"open", "deferred"}
    ]

    lines.extend(["## Open Questions", ""])
    if active_questions:
        for question in active_questions:
            lines.extend(
                [
                    f"### [{question['status']}] {question['title']}",
                    "",
                    question["question"],
                    "",
                ]
            )
            if question.get("context"):
                lines.extend([f"Context: {question['context']}", ""])
    else:
        lines.extend(["No open questions recorded.", ""])

    lines.extend(["## Glossary", ""])
    glossary_terms = list_glossary_terms(connection, project["id"])
    if glossary_terms:
        for term in glossary_terms:
            aliases = f" ({term['aliases']})" if term.get("aliases") else ""
            lines.extend([f"- **{term['term']}**{aliases}: {term['definition']}"])
        lines.append("")
    else:
        lines.extend(["No glossary terms recorded.", ""])

    lines.extend(["## Notes", ""])
    notes = list_notes(connection, project["id"])
    if notes:
        for note in notes:
            lines.extend([f"### {note['title']}", "", note["body"], ""])
    else:
        lines.extend(["No notes recorded.", ""])

    lines.extend(["## Agent Logs", ""])
    agent_logs = list_agent_logs(connection, project["id"])
    if agent_logs:
        for log in agent_logs:
            heading = log.get("agent_name") or "Agent"
            lines.extend([f"### {heading} - {log['created_at']}", "", log["summary"], ""])
            _append_optional(lines, "Changed files", log.get("changed_files"))
            _append_optional(lines, "Checks run", log.get("checks_run"))
            _append_optional(lines, "Known issues", log.get("known_issues"))
            _append_optional(lines, "Next task", log.get("next_task"))
            lines.append("")
    else:
        lines.extend(["No agent logs recorded.", ""])

    return "\n".join(lines).rstrip() + "\n"


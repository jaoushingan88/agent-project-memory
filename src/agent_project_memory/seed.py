from .db import connect_database, init_database
from .repositories import (
    create_agent_log,
    create_context_entry,
    create_decision,
    create_glossary_term,
    create_note,
    create_open_question,
    create_project,
    list_projects,
)


DEMO_PROJECT_SLUG = "demo-agent-project-memory"


def _find_project_by_slug(connection, slug):
    for project in list_projects(connection):
        if project["slug"] == slug:
            return project
    return None


def seed_demo_data(database_path):
    init_database(database_path)

    with connect_database(database_path) as connection:
        project = _find_project_by_slug(connection, DEMO_PROJECT_SLUG)
        if project is not None:
            return project

        project = create_project(
            connection,
            name="Demo Agent Project Memory",
            slug=DEMO_PROJECT_SLUG,
            description="Demo project for local-first project memory.",
        )
        create_context_entry(
            connection,
            project_id=project["id"],
            section="summary",
            title="Summary",
            body="This demo project shows the MVP memory primitives.",
            position=1,
        )
        create_decision(
            connection,
            project_id=project["id"],
            title="Use SQLite",
            status="accepted",
            decision="Use SQLite for local-first MVP storage.",
            rationale="SQLite is simple, local, and repository-friendly.",
        )
        create_open_question(
            connection,
            project_id=project["id"],
            title="Export profile",
            status="open",
            question="Which records should future export profiles include?",
            context="The MVP export should stay compact for AI agents.",
        )
        create_glossary_term(
            connection,
            project_id=project["id"],
            term="Canonical Context",
            definition="The current authoritative project context.",
        )
        create_note(
            connection,
            project_id=project["id"],
            title="Demo note",
            body="Notes capture useful project memory that is not a formal decision.",
            tags="demo",
        )
        create_agent_log(
            connection,
            project_id=project["id"],
            agent_name="Codex",
            summary="Seeded demo data for manual MVP smoke testing.",
            changed_files="local database only",
            checks_run="seed-demo",
            next_task="Open the dashboard or export context.md.",
        )
        return project


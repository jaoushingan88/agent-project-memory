import sqlite3

import pytest

from agent_project_memory.db import connect_database, init_database
from agent_project_memory.repositories import (
    create_agent_log,
    create_context_entry,
    create_decision,
    create_glossary_term,
    create_note,
    create_open_question,
    create_project,
    get_agent_log,
    get_context_entry,
    get_decision,
    get_glossary_term,
    get_note,
    get_open_question,
    get_project,
    list_agent_logs,
    list_context_entries,
    list_decisions,
    list_glossary_terms,
    list_notes,
    list_open_questions,
    list_projects,
)


@pytest.fixture
def connection(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)

    with connect_database(database_path) as db_connection:
        yield db_connection


@pytest.fixture
def project(connection):
    return create_project(
        connection,
        name="Agent Project Memory",
        slug="agent-project-memory",
        description="Local project memory",
    )


def assert_timestamps(record):
    assert record["created_at"].endswith("Z")
    assert record["updated_at"].endswith("Z")


def test_project_repository_create_get_and_list(connection):
    later = create_project(connection, name="Beta", slug="beta")
    earlier = create_project(connection, name="Alpha", slug="alpha")

    assert get_project(connection, later["id"])["slug"] == "beta"
    assert [project["name"] for project in list_projects(connection)] == [
        "Alpha",
        "Beta",
    ]
    assert_timestamps(earlier)


def test_context_repository_create_get_and_list(connection, project):
    second = create_context_entry(
        connection,
        project_id=project["id"],
        section="goals",
        title="Goals",
        body="Build the MVP.",
        position=2,
    )
    first = create_context_entry(
        connection,
        project_id=project["id"],
        section="summary",
        title="Summary",
        body="Local-first memory.",
        position=1,
    )

    assert get_context_entry(connection, second["id"])["section"] == "goals"
    assert [entry["section"] for entry in list_context_entries(connection, project["id"])] == [
        "summary",
        "goals",
    ]
    assert_timestamps(first)


def test_decision_repository_create_get_and_list(connection, project):
    proposed = create_decision(
        connection,
        project_id=project["id"],
        title="Proposed decision",
        status="proposed",
        decision="Consider a change.",
    )
    accepted = create_decision(
        connection,
        project_id=project["id"],
        title="Accepted decision",
        status="accepted",
        decision="Use SQLite.",
        rationale="Local-first MVP.",
    )

    assert get_decision(connection, proposed["id"])["status"] == "proposed"
    assert [decision["status"] for decision in list_decisions(connection, project["id"])] == [
        "accepted",
        "proposed",
    ]
    assert_timestamps(accepted)


def test_open_question_repository_create_get_and_list(connection, project):
    answered = create_open_question(
        connection,
        project_id=project["id"],
        title="Answered question",
        status="answered",
        question="Was this resolved?",
        answer="Yes.",
    )
    open_question = create_open_question(
        connection,
        project_id=project["id"],
        title="Open question",
        status="open",
        question="What comes next?",
    )

    assert get_open_question(connection, answered["id"])["answer"] == "Yes."
    assert [
        question["status"]
        for question in list_open_questions(connection, project["id"])
    ] == ["open", "answered"]
    assert_timestamps(open_question)


def test_glossary_repository_create_get_and_list(connection, project):
    second = create_glossary_term(
        connection,
        project_id=project["id"],
        term="Repository-Friendly",
        definition="Reviewable with code.",
    )
    first = create_glossary_term(
        connection,
        project_id=project["id"],
        term="Canonical Context",
        definition="Authoritative project context.",
        aliases="context",
    )

    assert get_glossary_term(connection, second["id"])["term"] == "Repository-Friendly"
    assert [term["term"] for term in list_glossary_terms(connection, project["id"])] == [
        "Canonical Context",
        "Repository-Friendly",
    ]
    assert_timestamps(first)


def test_note_repository_create_get_and_list(connection, project):
    first = create_note(
        connection,
        project_id=project["id"],
        title="First note",
        body="Keep the MVP small.",
        tags="mvp",
    )

    assert get_note(connection, first["id"])["tags"] == "mvp"
    assert [note["title"] for note in list_notes(connection, project["id"])] == [
        "First note"
    ]
    assert_timestamps(first)


def test_agent_log_repository_create_get_and_list(connection, project):
    log = create_agent_log(
        connection,
        project_id=project["id"],
        agent_name="Codex",
        summary="Added repository tests.",
        changed_files="tests/test_repositories.py",
        checks_run="python -m pytest",
        next_task="Project API",
    )

    assert get_agent_log(connection, log["id"])["agent_name"] == "Codex"
    assert [entry["summary"] for entry in list_agent_logs(connection, project["id"])] == [
        "Added repository tests."
    ]
    assert_timestamps(log)


def test_repository_boundaries_reject_duplicate_project_slug(connection):
    create_project(connection, name="One", slug="duplicate")

    with pytest.raises(sqlite3.IntegrityError):
        create_project(connection, name="Two", slug="duplicate")


def test_repository_boundaries_reject_invalid_decision_status(connection, project):
    with pytest.raises(sqlite3.IntegrityError):
        create_decision(
            connection,
            project_id=project["id"],
            title="Invalid",
            status="invalid",
            decision="This should fail.",
        )


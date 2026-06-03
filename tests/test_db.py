import sqlite3

import pytest

from agent_project_memory.db import connect_database, init_database


EXPECTED_TABLES = {
    "app_metadata",
    "projects",
    "context_entries",
    "decisions",
    "open_questions",
    "glossary_terms",
    "notes",
    "agent_logs",
}


def table_columns(connection, table_name):
    rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {row[1] for row in rows}


def test_init_database_creates_sqlite_file_metadata_and_mvp_tables(tmp_path):
    database_path = tmp_path / "memory.sqlite"

    returned_path = init_database(database_path)

    assert returned_path == database_path
    assert database_path.exists()

    with connect_database(database_path) as connection:
        row = connection.execute(
            "SELECT value FROM app_metadata WHERE key = 'schema_version'"
        ).fetchone()
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }

    assert row == ("1",)
    assert EXPECTED_TABLES.issubset(tables)


@pytest.mark.parametrize(
    ("table_name", "expected_columns"),
    [
        (
            "projects",
            {
                "id",
                "name",
                "slug",
                "description",
                "root_path",
                "created_at",
                "updated_at",
            },
        ),
        (
            "context_entries",
            {
                "id",
                "project_id",
                "section",
                "title",
                "body",
                "position",
                "created_at",
                "updated_at",
            },
        ),
        (
            "decisions",
            {
                "id",
                "project_id",
                "title",
                "status",
                "decision",
                "rationale",
                "consequences",
                "supersedes_decision_id",
                "created_at",
                "updated_at",
            },
        ),
        (
            "open_questions",
            {
                "id",
                "project_id",
                "title",
                "status",
                "question",
                "context",
                "answer",
                "created_at",
                "updated_at",
            },
        ),
        (
            "glossary_terms",
            {
                "id",
                "project_id",
                "term",
                "definition",
                "aliases",
                "created_at",
                "updated_at",
            },
        ),
        (
            "notes",
            {
                "id",
                "project_id",
                "title",
                "body",
                "tags",
                "created_at",
                "updated_at",
            },
        ),
        (
            "agent_logs",
            {
                "id",
                "project_id",
                "agent_name",
                "summary",
                "changed_files",
                "checks_run",
                "known_issues",
                "next_task",
                "created_at",
                "updated_at",
            },
        ),
    ],
)
def test_mvp_tables_have_expected_columns(tmp_path, table_name, expected_columns):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)

    with connect_database(database_path) as connection:
        assert expected_columns.issubset(table_columns(connection, table_name))


def test_init_database_is_idempotent(tmp_path):
    database_path = tmp_path / "memory.sqlite"

    init_database(database_path)
    init_database(database_path)

    with connect_database(database_path) as connection:
        row = connection.execute(
            "SELECT value FROM app_metadata WHERE key = 'schema_version'"
        ).fetchone()

    assert row == ("1",)


def test_foreign_keys_are_enforced(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)

    with connect_database(database_path) as connection:
        with pytest.raises(sqlite3.IntegrityError):
            connection.execute(
                """
                INSERT INTO notes (
                    project_id,
                    title,
                    body,
                    created_at,
                    updated_at
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (999, "orphan", "missing project", "2026-06-03T00:00:00Z", "2026-06-03T00:00:00Z"),
            )

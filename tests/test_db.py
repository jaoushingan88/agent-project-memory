import sqlite3

from agent_project_memory.db import init_database


def test_init_database_creates_sqlite_file_and_metadata(tmp_path):
    database_path = tmp_path / "memory.sqlite"

    returned_path = init_database(database_path)

    assert returned_path == database_path
    assert database_path.exists()

    with sqlite3.connect(database_path) as connection:
        row = connection.execute(
            "SELECT value FROM app_metadata WHERE key = 'schema_version'"
        ).fetchone()

    assert row == ("0",)


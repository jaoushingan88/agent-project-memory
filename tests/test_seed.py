from agent_project_memory.app import create_app
from agent_project_memory.db import connect_database, init_database
from agent_project_memory.repositories import (
    list_agent_logs,
    list_context_entries,
    list_decisions,
    list_glossary_terms,
    list_notes,
    list_open_questions,
)
from agent_project_memory.seed import DEMO_PROJECT_SLUG, seed_demo_data


def test_seed_demo_data_creates_one_complete_demo_project(tmp_path):
    database_path = tmp_path / "memory.sqlite"

    first_project = seed_demo_data(database_path)
    second_project = seed_demo_data(database_path)

    assert first_project["id"] == second_project["id"]
    assert first_project["slug"] == DEMO_PROJECT_SLUG

    with connect_database(database_path) as connection:
        project_id = first_project["id"]
        assert len(list_context_entries(connection, project_id)) == 1
        assert len(list_decisions(connection, project_id)) == 1
        assert len(list_open_questions(connection, project_id)) == 1
        assert len(list_glossary_terms(connection, project_id)) == 1
        assert len(list_notes(connection, project_id)) == 1
        assert len(list_agent_logs(connection, project_id)) == 1


def test_seed_demo_flask_command_creates_demo_project(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    runner = app.test_cli_runner()

    result = runner.invoke(args=["seed-demo"])

    assert result.exit_code == 0
    assert f"Seeded demo project: {DEMO_PROJECT_SLUG}" in result.output

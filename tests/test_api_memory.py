from agent_project_memory.app import create_app
from agent_project_memory.db import init_database


def make_client(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    return app.test_client()


def create_project(client):
    response = client.post(
        "/api/projects",
        json={"name": "Agent Project Memory", "slug": "agent-project-memory"},
    )
    return response.get_json()["project"]


def post_and_list(client, project_id, path, payload, collection_key, record_key):
    create_response = client.post(f"/api/projects/{project_id}/{path}", json=payload)
    assert create_response.status_code == 201
    created = create_response.get_json()[record_key]

    list_response = client.get(f"/api/projects/{project_id}/{path}")
    assert list_response.status_code == 200
    records = list_response.get_json()[collection_key]
    assert len(records) == 1
    assert records[0]["id"] == created["id"]
    return created


def test_context_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "context",
        {
            "section": "summary",
            "title": "Summary",
            "body": "Local-first project memory.",
            "position": 1,
        },
        "context_entries",
        "context_entry",
    )

    assert created["section"] == "summary"


def test_decisions_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "decisions",
        {
            "title": "Use SQLite",
            "status": "accepted",
            "decision": "Use SQLite for the MVP.",
            "rationale": "Local-first storage.",
        },
        "decisions",
        "decision",
    )

    assert created["status"] == "accepted"


def test_questions_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "questions",
        {
            "title": "Export scope",
            "status": "open",
            "question": "Which records should export include?",
            "context": "Agent context should stay compact.",
        },
        "open_questions",
        "open_question",
    )

    assert created["status"] == "open"


def test_glossary_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "glossary",
        {
            "term": "Canonical Context",
            "definition": "Authoritative project context.",
            "aliases": "context",
        },
        "glossary_terms",
        "glossary_term",
    )

    assert created["term"] == "Canonical Context"


def test_notes_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "notes",
        {
            "title": "MVP note",
            "body": "Keep the MVP small.",
            "tags": "mvp",
        },
        "notes",
        "note",
    )

    assert created["tags"] == "mvp"


def test_agent_logs_api_create_and_list(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    created = post_and_list(
        client,
        project["id"],
        "agent-logs",
        {
            "agent_name": "Codex",
            "summary": "Added API tests.",
            "changed_files": "tests/test_api_memory.py",
            "checks_run": "python -m pytest",
        },
        "agent_logs",
        "agent_log",
    )

    assert created["agent_name"] == "Codex"


def test_memory_api_returns_404_for_missing_project(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/projects/999/context")

    assert response.status_code == 404
    assert response.get_json()["error"]["message"] == "Project not found."


def test_memory_api_rejects_missing_required_fields(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    response = client.post(
        f"/api/projects/{project['id']}/decisions",
        json={"title": "Missing status"},
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["message"] == "Missing required field: status"


def test_memory_api_rejects_invalid_status(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)

    response = client.post(
        f"/api/projects/{project['id']}/questions",
        json={
            "title": "Invalid status",
            "status": "invalid",
            "question": "Should fail?",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["message"] == "Invalid open question data."


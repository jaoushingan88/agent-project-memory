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
        json={
            "name": "Agent Project Memory",
            "slug": "agent-project-memory",
            "description": "Local-first project memory.",
        },
    )
    return response.get_json()["project"]


def test_export_context_markdown_includes_mvp_sections(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)
    project_url = f"/api/projects/{project['id']}"

    client.post(
        f"{project_url}/context",
        json={
            "section": "summary",
            "title": "Summary",
            "body": "Canonical context body.",
            "position": 1,
        },
    )
    client.post(
        f"{project_url}/decisions",
        json={
            "title": "Use SQLite",
            "status": "accepted",
            "decision": "Use SQLite for local-first storage.",
        },
    )
    client.post(
        f"{project_url}/questions",
        json={
            "title": "Export profile",
            "status": "open",
            "question": "What should be exported?",
        },
    )
    client.post(
        f"{project_url}/glossary",
        json={
            "term": "Canonical Context",
            "definition": "Current authoritative context.",
        },
    )
    client.post(
        f"{project_url}/notes",
        json={"title": "MVP note", "body": "Notes are included."},
    )
    client.post(
        f"{project_url}/agent-logs",
        json={"agent_name": "Codex", "summary": "Agent logs are included."},
    )

    response = client.get(f"{project_url}/export/context.md")

    assert response.status_code == 200
    assert response.mimetype == "text/markdown"
    markdown = response.data.decode("utf-8")
    assert "# Agent Project Memory Context" in markdown
    assert "## Project Overview" in markdown
    assert "## Canonical Context" in markdown
    assert "Canonical context body." in markdown
    assert "## Decisions" in markdown
    assert "Use SQLite for local-first storage." in markdown
    assert "## Open Questions" in markdown
    assert "What should be exported?" in markdown
    assert "## Glossary" in markdown
    assert "Canonical Context" in markdown
    assert "## Notes" in markdown
    assert "Notes are included." in markdown
    assert "## Agent Logs" in markdown
    assert "Agent logs are included." in markdown


def test_export_context_markdown_excludes_answered_and_superseded_records(tmp_path):
    client = make_client(tmp_path)
    project = create_project(client)
    project_url = f"/api/projects/{project['id']}"

    client.post(
        f"{project_url}/decisions",
        json={
            "title": "Old decision",
            "status": "superseded",
            "decision": "Do not include this.",
        },
    )
    client.post(
        f"{project_url}/questions",
        json={
            "title": "Answered",
            "status": "answered",
            "question": "Do not include this?",
            "answer": "No.",
        },
    )

    response = client.get(f"{project_url}/export/context.md")
    markdown = response.data.decode("utf-8")

    assert "Do not include this." not in markdown
    assert "Do not include this?" not in markdown


def test_export_context_returns_404_for_missing_project(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/projects/999/export/context.md")

    assert response.status_code == 404
    assert response.get_json()["error"]["message"] == "Project not found."


from agent_project_memory.app import create_app
from agent_project_memory.db import init_database


def test_mvp_ui_smoke_flow(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()

    project_response = client.post(
        "/projects",
        data={
            "name": "UI Smoke Project",
            "slug": "ui-smoke-project",
            "description": "Created through the Web UI.",
        },
    )
    assert project_response.status_code == 302

    form_posts = [
        (
            "/projects/1/context",
            {
                "section": "summary",
                "title": "Summary",
                "body": "UI smoke context.",
                "position": "1",
            },
        ),
        (
            "/projects/1/decisions",
            {
                "title": "Use UI smoke tests",
                "status": "accepted",
                "decision": "Verify the Web UI MVP flow.",
            },
        ),
        (
            "/projects/1/questions",
            {
                "title": "UI completion",
                "status": "open",
                "question": "Is the Web UI minimally usable?",
            },
        ),
        (
            "/projects/1/glossary",
            {
                "term": "UI Smoke",
                "definition": "A broad Web UI flow check.",
            },
        ),
        (
            "/projects/1/notes",
            {
                "title": "UI note",
                "body": "Notes can be created through the Web UI.",
            },
        ),
        (
            "/projects/1/agent-logs",
            {
                "agent_name": "Codex",
                "summary": "Agent logs can be created through the Web UI.",
            },
        ),
    ]

    for path, data in form_posts:
        response = client.post(path, data=data)
        assert response.status_code == 302

    dashboard = client.get("/projects/1")
    assert dashboard.status_code == 200
    assert b"UI Smoke Project" in dashboard.data
    assert b"Download context.md" in dashboard.data

    export = client.get("/projects/1/export")
    assert export.status_code == 200
    assert b"UI smoke context." in export.data
    assert b"Verify the Web UI MVP flow." in export.data
    assert b"Is the Web UI minimally usable?" in export.data
    assert b"UI Smoke" in export.data
    assert b"Notes can be created through the Web UI." in export.data
    assert b"Agent logs can be created through the Web UI." in export.data


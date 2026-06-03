from agent_project_memory.app import create_app
from agent_project_memory.db import init_database


def test_mvp_api_smoke_flow(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()

    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.get_json() == {"ok": True}

    project_response = client.post(
        "/api/projects",
        json={
            "name": "Smoke Project",
            "slug": "smoke-project",
            "description": "MVP smoke test project.",
        },
    )
    assert project_response.status_code == 201
    project = project_response.get_json()["project"]
    project_url = f"/api/projects/{project['id']}"

    create_requests = [
        (
            "context",
            {
                "section": "summary",
                "title": "Summary",
                "body": "Smoke canonical context.",
                "position": 1,
            },
        ),
        (
            "decisions",
            {
                "title": "Use tests",
                "status": "accepted",
                "decision": "Use smoke tests for MVP verification.",
            },
        ),
        (
            "questions",
            {
                "title": "Remaining work",
                "status": "open",
                "question": "What remains before release?",
            },
        ),
        (
            "glossary",
            {
                "term": "Smoke Test",
                "definition": "A broad verification of the MVP flow.",
            },
        ),
        (
            "notes",
            {
                "title": "Smoke note",
                "body": "Notes work in the MVP flow.",
            },
        ),
        (
            "agent-logs",
            {
                "agent_name": "Codex",
                "summary": "Smoke flow executed.",
            },
        ),
    ]

    for path, payload in create_requests:
        response = client.post(f"{project_url}/{path}", json=payload)
        assert response.status_code == 201

    export_response = client.get(f"{project_url}/export/context.md")
    assert export_response.status_code == 200
    markdown = export_response.data.decode("utf-8")

    assert "Smoke Project Context" in markdown
    assert "Smoke canonical context." in markdown
    assert "Use smoke tests for MVP verification." in markdown
    assert "What remains before release?" in markdown
    assert "Smoke Test" in markdown
    assert "Notes work in the MVP flow." in markdown
    assert "Smoke flow executed." in markdown


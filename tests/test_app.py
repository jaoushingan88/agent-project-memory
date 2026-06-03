from agent_project_memory.app import create_app
from agent_project_memory.db import init_database


def test_health_endpoint_returns_ok():
    app = create_app({"TESTING": True})
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"ok": True}


def test_index_endpoint_returns_minimal_ui():
    app = create_app({"TESTING": True})
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"agent-project-memory" in response.data
    assert b"GET /api/health" in response.data


def test_index_uses_base_navigation():
    app = create_app({"TESTING": True})
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Projects" in response.data
    assert b"Health" in response.data


def test_project_create_form_creates_project_and_redirects(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()

    response = client.post(
        "/projects",
        data={
            "name": "Web Project",
            "slug": "web-project",
            "description": "Created from the Web UI.",
        },
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/projects/1")

    list_response = client.get("/")
    assert b"Web Project" in list_response.data


def test_project_dashboard_renders_project(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Dashboard Project", "slug": "dashboard"})

    response = client.get("/projects/1")

    assert response.status_code == 200
    assert b"Dashboard Project" in response.data
    assert b"Download context.md" in response.data
    assert b"Context" in response.data
    assert b"Decisions" in response.data
    assert b"Agent logs" in response.data


def test_context_page_creates_and_lists_context_entry(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Context Project", "slug": "context-project"})

    create_response = client.post(
        "/projects/1/context",
        data={
            "section": "summary",
            "title": "Summary",
            "body": "Canonical context from the Web UI.",
            "position": "1",
        },
    )

    assert create_response.status_code == 302
    page = client.get("/projects/1/context")
    assert b"Summary" in page.data
    assert b"Canonical context from the Web UI." in page.data


def test_decisions_page_creates_and_lists_decision(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Decision Project", "slug": "decision-project"})

    create_response = client.post(
        "/projects/1/decisions",
        data={
            "title": "Use Flask",
            "status": "accepted",
            "decision": "Use Flask for the local MVP.",
            "rationale": "Already selected in project decisions.",
        },
    )

    assert create_response.status_code == 302
    page = client.get("/projects/1/decisions")
    assert b"Use Flask" in page.data
    assert b"Use Flask for the local MVP." in page.data


def test_questions_page_creates_and_lists_question(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Question Project", "slug": "question-project"})

    create_response = client.post(
        "/projects/1/questions",
        data={
            "title": "Export scope",
            "status": "open",
            "question": "What should the export include?",
            "context": "Keep context compact.",
        },
    )

    assert create_response.status_code == 302
    page = client.get("/projects/1/questions")
    assert b"Export scope" in page.data
    assert b"What should the export include?" in page.data


def test_glossary_page_creates_and_lists_term(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Glossary Project", "slug": "glossary-project"})

    create_response = client.post(
        "/projects/1/glossary",
        data={
            "term": "Canonical Context",
            "definition": "The authoritative project context.",
            "aliases": "context",
        },
    )

    assert create_response.status_code == 302
    page = client.get("/projects/1/glossary")
    assert b"Canonical Context" in page.data
    assert b"The authoritative project context." in page.data


def test_notes_logs_page_creates_and_lists_note_and_agent_log(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Notes Project", "slug": "notes-project"})

    note_response = client.post(
        "/projects/1/notes",
        data={
            "title": "MVP note",
            "body": "Notes work from the Web UI.",
            "tags": "mvp",
        },
    )
    log_response = client.post(
        "/projects/1/agent-logs",
        data={
            "agent_name": "Codex",
            "summary": "Agent logs work from the Web UI.",
            "checks_run": "python -m pytest",
        },
    )

    assert note_response.status_code == 302
    assert log_response.status_code == 302
    page = client.get("/projects/1/notes-logs")
    assert b"MVP note" in page.data
    assert b"Notes work from the Web UI." in page.data
    assert b"Codex" in page.data
    assert b"Agent logs work from the Web UI." in page.data


def test_export_page_previews_context_markdown(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    client = app.test_client()
    client.post("/projects", data={"name": "Export Project", "slug": "export-project"})
    client.post(
        "/projects/1/context",
        data={
            "section": "summary",
            "title": "Summary",
            "body": "Export preview body.",
            "position": "1",
        },
    )

    response = client.get("/projects/1/export")

    assert response.status_code == 200
    assert b"Download context.md" in response.data
    assert b"Export preview body." in response.data

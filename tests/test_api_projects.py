from agent_project_memory.app import create_app
from agent_project_memory.db import init_database


def make_client(tmp_path):
    database_path = tmp_path / "memory.sqlite"
    init_database(database_path)
    app = create_app({"TESTING": True, "DATABASE_PATH": str(database_path)})
    return app.test_client()


def test_list_projects_returns_empty_list(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/projects")

    assert response.status_code == 200
    assert response.get_json() == {"projects": []}


def test_create_and_get_project(tmp_path):
    client = make_client(tmp_path)

    create_response = client.post(
        "/api/projects",
        json={
            "name": "Agent Project Memory",
            "slug": "agent-project-memory",
            "description": "Local project memory",
        },
    )

    assert create_response.status_code == 201
    created = create_response.get_json()["project"]
    assert created["name"] == "Agent Project Memory"
    assert created["slug"] == "agent-project-memory"

    get_response = client.get(f"/api/projects/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.get_json()["project"]["id"] == created["id"]


def test_list_projects_orders_by_name(tmp_path):
    client = make_client(tmp_path)
    client.post("/api/projects", json={"name": "Beta", "slug": "beta"})
    client.post("/api/projects", json={"name": "Alpha", "slug": "alpha"})

    response = client.get("/api/projects")

    assert response.status_code == 200
    assert [project["name"] for project in response.get_json()["projects"]] == [
        "Alpha",
        "Beta",
    ]


def test_create_project_requires_json(tmp_path):
    client = make_client(tmp_path)

    response = client.post("/api/projects", data="not json")

    assert response.status_code == 400
    assert response.get_json()["error"]["message"] == "Request body must be JSON."


def test_create_project_requires_name_and_slug(tmp_path):
    client = make_client(tmp_path)

    response = client.post("/api/projects", json={"name": "Missing Slug"})

    assert response.status_code == 400
    assert response.get_json()["error"]["message"] == "Missing required field: slug"


def test_create_project_rejects_duplicate_slug(tmp_path):
    client = make_client(tmp_path)
    client.post("/api/projects", json={"name": "One", "slug": "duplicate"})

    response = client.post("/api/projects", json={"name": "Two", "slug": "duplicate"})

    assert response.status_code == 400
    assert response.get_json()["error"]["message"] == "Project slug must be unique."


def test_get_project_returns_404_for_missing_project(tmp_path):
    client = make_client(tmp_path)

    response = client.get("/api/projects/999")

    assert response.status_code == 404
    assert response.get_json()["error"]["message"] == "Project not found."


from agent_project_memory.app import create_app


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

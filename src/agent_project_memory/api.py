import sqlite3

from flask import Blueprint, Response, jsonify, request
from werkzeug.exceptions import HTTPException

from .db import get_database
from .export import render_context_markdown
from .repositories import (
    create_agent_log,
    create_context_entry,
    create_decision,
    create_glossary_term,
    create_note,
    create_open_question,
    create_project,
    get_project,
    list_agent_logs,
    list_context_entries,
    list_decisions,
    list_glossary_terms,
    list_notes,
    list_open_questions,
    list_projects,
)


api = Blueprint("api", __name__, url_prefix="/api")


def json_error(status_code, message):
    response = jsonify({"error": {"message": message, "status": status_code}})
    response.status_code = status_code
    return response


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(error):
        return json_error(404, "Not found.")

    @app.errorhandler(405)
    def method_not_allowed(error):
        return json_error(405, "Method not allowed.")

    @app.errorhandler(sqlite3.IntegrityError)
    def database_integrity_error(error):
        return json_error(400, "Database constraint violation.")

    @app.errorhandler(Exception)
    def internal_error(error):
        if isinstance(error, HTTPException):
            return json_error(error.code, error.description)
        if app.config.get("TESTING"):
            raise error
        return json_error(500, "Internal server error.")


def request_json():
    if not request.is_json:
        return None
    return request.get_json(silent=True)


def require_fields(data, fields):
    missing = [field for field in fields if not data.get(field)]
    if missing:
        return f"Missing required field: {missing[0]}"
    return None


def ensure_project(connection, project_id):
    project = get_project(connection, project_id)
    if project is None:
        return None, json_error(404, "Project not found.")
    return project, None


@api.get("/health")
def health():
    return jsonify({"ok": True})


@api.get("/projects")
def projects_index():
    projects = list_projects(get_database())
    return jsonify({"projects": projects})


@api.post("/projects")
def projects_create():
    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["name", "slug"])
    if missing:
        return json_error(400, missing)

    try:
        project = create_project(
            get_database(),
            name=data["name"],
            slug=data["slug"],
            description=data.get("description"),
            root_path=data.get("root_path"),
        )
    except sqlite3.IntegrityError:
        return json_error(400, "Project slug must be unique.")

    response = jsonify({"project": project})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>")
def projects_show(project_id):
    project = get_project(get_database(), project_id)
    if project is None:
        return json_error(404, "Project not found.")
    return jsonify({"project": project})


@api.get("/projects/<int:project_id>/context")
def context_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"context_entries": list_context_entries(connection, project_id)})


@api.post("/projects/<int:project_id>/context")
def context_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["section", "title", "body", "position"])
    if missing:
        return json_error(400, missing)

    try:
        entry = create_context_entry(
            connection,
            project_id=project_id,
            section=data["section"],
            title=data["title"],
            body=data["body"],
            position=data["position"],
        )
    except sqlite3.IntegrityError:
        return json_error(400, "Context section must be unique per project.")

    response = jsonify({"context_entry": entry})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/decisions")
def decisions_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"decisions": list_decisions(connection, project_id)})


@api.post("/projects/<int:project_id>/decisions")
def decisions_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["title", "status", "decision"])
    if missing:
        return json_error(400, missing)

    try:
        decision = create_decision(
            connection,
            project_id=project_id,
            title=data["title"],
            status=data["status"],
            decision=data["decision"],
            rationale=data.get("rationale"),
            consequences=data.get("consequences"),
            supersedes_decision_id=data.get("supersedes_decision_id"),
        )
    except sqlite3.IntegrityError:
        return json_error(400, "Invalid decision data.")

    response = jsonify({"decision": decision})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/questions")
def questions_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"open_questions": list_open_questions(connection, project_id)})


@api.post("/projects/<int:project_id>/questions")
def questions_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["title", "status", "question"])
    if missing:
        return json_error(400, missing)

    try:
        question = create_open_question(
            connection,
            project_id=project_id,
            title=data["title"],
            status=data["status"],
            question=data["question"],
            context=data.get("context"),
            answer=data.get("answer"),
        )
    except sqlite3.IntegrityError:
        return json_error(400, "Invalid open question data.")

    response = jsonify({"open_question": question})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/glossary")
def glossary_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"glossary_terms": list_glossary_terms(connection, project_id)})


@api.post("/projects/<int:project_id>/glossary")
def glossary_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["term", "definition"])
    if missing:
        return json_error(400, missing)

    try:
        term = create_glossary_term(
            connection,
            project_id=project_id,
            term=data["term"],
            definition=data["definition"],
            aliases=data.get("aliases"),
        )
    except sqlite3.IntegrityError:
        return json_error(400, "Glossary term must be unique per project.")

    response = jsonify({"glossary_term": term})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/notes")
def notes_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"notes": list_notes(connection, project_id)})


@api.post("/projects/<int:project_id>/notes")
def notes_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["title", "body"])
    if missing:
        return json_error(400, missing)

    note = create_note(
        connection,
        project_id=project_id,
        title=data["title"],
        body=data["body"],
        tags=data.get("tags"),
    )

    response = jsonify({"note": note})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/agent-logs")
def agent_logs_index(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error
    return jsonify({"agent_logs": list_agent_logs(connection, project_id)})


@api.post("/projects/<int:project_id>/agent-logs")
def agent_logs_create(project_id):
    connection = get_database()
    _, error = ensure_project(connection, project_id)
    if error:
        return error

    data = request_json()
    if data is None:
        return json_error(400, "Request body must be JSON.")

    missing = require_fields(data, ["summary"])
    if missing:
        return json_error(400, missing)

    log = create_agent_log(
        connection,
        project_id=project_id,
        summary=data["summary"],
        agent_name=data.get("agent_name"),
        changed_files=data.get("changed_files"),
        checks_run=data.get("checks_run"),
        known_issues=data.get("known_issues"),
        next_task=data.get("next_task"),
    )

    response = jsonify({"agent_log": log})
    response.status_code = 201
    return response


@api.get("/projects/<int:project_id>/export/context.md")
def export_context(project_id):
    connection = get_database()
    project, error = ensure_project(connection, project_id)
    if error:
        return error

    markdown = render_context_markdown(connection, project)
    return Response(markdown, mimetype="text/markdown")

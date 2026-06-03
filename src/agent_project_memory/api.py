import sqlite3

from flask import Blueprint, jsonify, request

from .db import get_database
from .repositories import create_project, get_project, list_projects


api = Blueprint("api", __name__, url_prefix="/api")


def json_error(status_code, message):
    response = jsonify({"error": {"message": message}})
    response.status_code = status_code
    return response


def request_json():
    if not request.is_json:
        return None
    return request.get_json(silent=True)


def require_fields(data, fields):
    missing = [field for field in fields if not data.get(field)]
    if missing:
        return f"Missing required field: {missing[0]}"
    return None


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


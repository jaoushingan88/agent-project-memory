import argparse
import os
import sys
from pathlib import Path

import sqlite3

from flask import Flask, redirect, render_template, request, url_for

from .api import api, register_error_handlers
from .db import get_database, init_app, init_database
from .repositories import create_project, get_project, list_projects


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE_PATH=os.environ.get(
            "APPM_DATABASE_PATH",
            str(Path(".agent-project-memory") / "memory.sqlite"),
        )
    )

    if test_config:
        app.config.update(test_config)

    init_app(app)
    app.register_blueprint(api)
    register_error_handlers(app)

    @app.get("/")
    def index():
        return render_template("index.html", projects=list_projects(get_database()))

    @app.post("/projects")
    def create_project_view():
        try:
            project = create_project(
                get_database(),
                name=request.form.get("name", "").strip(),
                slug=request.form.get("slug", "").strip(),
                description=request.form.get("description", "").strip() or None,
                root_path=request.form.get("root_path", "").strip() or None,
            )
        except sqlite3.IntegrityError:
            return render_template(
                "index.html",
                projects=list_projects(get_database()),
                error="Project slug must be unique.",
            ), 400

        return redirect(url_for("project_dashboard", project_id=project["id"]))

    @app.get("/projects/<int:project_id>")
    def project_dashboard(project_id):
        project = get_project(get_database(), project_id)
        if project is None:
            return render_template("not_found.html"), 404
        return render_template("project_dashboard.html", project=project)

    return app


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run the local agent-project-memory Flask app."
    )
    parser.add_argument(
        "--init-db",
        action="store_true",
        help="Initialize the local SQLite database and exit.",
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=5000, type=int)
    args = parser.parse_args(argv)

    app = create_app()

    if args.init_db:
        db_path = init_database(app.config["DATABASE_PATH"])
        print(f"Initialized database: {db_path}")
        return 0

    init_database(app.config["DATABASE_PATH"])
    app.run(host=args.host, port=args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

import argparse
import os
import sys
from pathlib import Path

import sqlite3

from flask import Flask, redirect, render_template, request, url_for

from .api import api, register_error_handlers
from .db import get_database, init_app, init_database
from .repositories import (
    create_project,
    create_context_entry,
    create_decision,
    create_open_question,
    get_project,
    list_agent_logs,
    list_context_entries,
    list_decisions,
    list_glossary_terms,
    list_notes,
    list_open_questions,
    list_projects,
)


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
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        counts = {
            "context": len(list_context_entries(connection, project_id)),
            "decisions": len(list_decisions(connection, project_id)),
            "questions": len(list_open_questions(connection, project_id)),
            "glossary": len(list_glossary_terms(connection, project_id)),
            "notes": len(list_notes(connection, project_id)),
            "agent_logs": len(list_agent_logs(connection, project_id)),
        }
        return render_template("project_dashboard.html", project=project, counts=counts)

    @app.get("/projects/<int:project_id>/context")
    def context_page(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        return render_template(
            "context.html",
            project=project,
            context_entries=list_context_entries(connection, project_id),
        )

    @app.post("/projects/<int:project_id>/context")
    def create_context_view(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        try:
            create_context_entry(
                connection,
                project_id=project_id,
                section=request.form.get("section", "").strip(),
                title=request.form.get("title", "").strip(),
                body=request.form.get("body", "").strip(),
                position=int(request.form.get("position", "0")),
            )
        except (sqlite3.IntegrityError, ValueError):
            return render_template(
                "context.html",
                project=project,
                context_entries=list_context_entries(connection, project_id),
                error="Context entries require a unique section and numeric position.",
            ), 400
        return redirect(url_for("context_page", project_id=project_id))

    @app.get("/projects/<int:project_id>/decisions")
    def decisions_page(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        return render_template(
            "decisions.html",
            project=project,
            decisions=list_decisions(connection, project_id),
        )

    @app.post("/projects/<int:project_id>/decisions")
    def create_decision_view(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        try:
            create_decision(
                connection,
                project_id=project_id,
                title=request.form.get("title", "").strip(),
                status=request.form.get("status", "").strip(),
                decision=request.form.get("decision", "").strip(),
                rationale=request.form.get("rationale", "").strip() or None,
                consequences=request.form.get("consequences", "").strip() or None,
            )
        except sqlite3.IntegrityError:
            return render_template(
                "decisions.html",
                project=project,
                decisions=list_decisions(connection, project_id),
                error="Decision requires a valid status.",
            ), 400
        return redirect(url_for("decisions_page", project_id=project_id))

    @app.get("/projects/<int:project_id>/questions")
    def questions_page(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        return render_template(
            "questions.html",
            project=project,
            questions=list_open_questions(connection, project_id),
        )

    @app.post("/projects/<int:project_id>/questions")
    def create_question_view(project_id):
        connection = get_database()
        project = get_project(connection, project_id)
        if project is None:
            return render_template("not_found.html"), 404
        try:
            create_open_question(
                connection,
                project_id=project_id,
                title=request.form.get("title", "").strip(),
                status=request.form.get("status", "").strip(),
                question=request.form.get("question", "").strip(),
                context=request.form.get("context", "").strip() or None,
                answer=request.form.get("answer", "").strip() or None,
            )
        except sqlite3.IntegrityError:
            return render_template(
                "questions.html",
                project=project,
                questions=list_open_questions(connection, project_id),
                error="Open question requires a valid status.",
            ), 400
        return redirect(url_for("questions_page", project_id=project_id))

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

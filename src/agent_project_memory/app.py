import argparse
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template

from .db import init_app, init_database


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

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})

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

import sqlite3
from importlib import resources
from pathlib import Path

import click
from flask import current_app, g
from flask.cli import with_appcontext


def load_schema():
    return resources.files("agent_project_memory").joinpath("schema.sql").read_text()


def connect_database(database_path):
    connection = sqlite3.connect(Path(database_path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database(database_path):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with connect_database(path) as connection:
        connection.executescript(load_schema())
        connection.commit()

    return path


def get_database():
    if "database" not in g:
        g.database = connect_database(current_app.config["DATABASE_PATH"])
    return g.database


def close_database(error=None):
    connection = g.pop("database", None)

    if connection is not None:
        connection.close()


@click.command("init-db")
@with_appcontext
def init_database_command():
    db_path = init_database(current_app.config["DATABASE_PATH"])
    click.echo(f"Initialized database: {db_path}")


@click.command("seed-demo")
@with_appcontext
def seed_demo_command():
    from .seed import seed_demo_data

    project = seed_demo_data(current_app.config["DATABASE_PATH"])
    click.echo(f"Seeded demo project: {project['slug']}")


def init_app(app):
    app.teardown_appcontext(close_database)
    app.cli.add_command(init_database_command)
    app.cli.add_command(seed_demo_command)

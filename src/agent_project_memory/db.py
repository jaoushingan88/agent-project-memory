import sqlite3
from importlib import resources
from pathlib import Path


def load_schema():
    return resources.files("agent_project_memory").joinpath("schema.sql").read_text()


def connect_database(database_path):
    connection = sqlite3.connect(Path(database_path))
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_database(database_path):
    path = Path(database_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with connect_database(path) as connection:
        connection.executescript(load_schema())
        connection.commit()

    return path

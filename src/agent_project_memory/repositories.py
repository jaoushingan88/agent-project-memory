from datetime import UTC, datetime


def utc_now():
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def row_to_dict(row):
    if row is None:
        return None
    return dict(row)


def _insert(connection, table_name, values):
    now = utc_now()
    record = {**values, "created_at": now, "updated_at": now}
    columns = ", ".join(record)
    placeholders = ", ".join(["?"] * len(record))

    cursor = connection.execute(
        f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
        tuple(record.values()),
    )
    connection.commit()
    return cursor.lastrowid


def _get_by_id(connection, table_name, record_id):
    row = connection.execute(
        f"SELECT * FROM {table_name} WHERE id = ?",
        (record_id,),
    ).fetchone()
    return row_to_dict(row)


def _list_by_project(connection, table_name, project_id, order_by):
    rows = connection.execute(
        f"SELECT * FROM {table_name} WHERE project_id = ? ORDER BY {order_by}",
        (project_id,),
    ).fetchall()
    return [row_to_dict(row) for row in rows]


def create_project(connection, name, slug, description=None, root_path=None):
    project_id = _insert(
        connection,
        "projects",
        {
            "name": name,
            "slug": slug,
            "description": description,
            "root_path": root_path,
        },
    )
    return get_project(connection, project_id)


def get_project(connection, project_id):
    return _get_by_id(connection, "projects", project_id)


def list_projects(connection):
    rows = connection.execute("SELECT * FROM projects ORDER BY name").fetchall()
    return [row_to_dict(row) for row in rows]


def create_context_entry(connection, project_id, section, title, body, position):
    entry_id = _insert(
        connection,
        "context_entries",
        {
            "project_id": project_id,
            "section": section,
            "title": title,
            "body": body,
            "position": position,
        },
    )
    return get_context_entry(connection, entry_id)


def get_context_entry(connection, entry_id):
    return _get_by_id(connection, "context_entries", entry_id)


def list_context_entries(connection, project_id):
    return _list_by_project(connection, "context_entries", project_id, "position, title")


def create_decision(
    connection,
    project_id,
    title,
    status,
    decision,
    rationale=None,
    consequences=None,
    supersedes_decision_id=None,
):
    decision_id = _insert(
        connection,
        "decisions",
        {
            "project_id": project_id,
            "title": title,
            "status": status,
            "decision": decision,
            "rationale": rationale,
            "consequences": consequences,
            "supersedes_decision_id": supersedes_decision_id,
        },
    )
    return get_decision(connection, decision_id)


def get_decision(connection, decision_id):
    return _get_by_id(connection, "decisions", decision_id)


def list_decisions(connection, project_id):
    return _list_by_project(
        connection,
        "decisions",
        project_id,
        """
        CASE status
            WHEN 'accepted' THEN 1
            WHEN 'proposed' THEN 2
            WHEN 'superseded' THEN 3
            ELSE 4
        END,
        created_at,
        id
        """,
    )


def create_open_question(
    connection,
    project_id,
    title,
    status,
    question,
    context=None,
    answer=None,
):
    question_id = _insert(
        connection,
        "open_questions",
        {
            "project_id": project_id,
            "title": title,
            "status": status,
            "question": question,
            "context": context,
            "answer": answer,
        },
    )
    return get_open_question(connection, question_id)


def get_open_question(connection, question_id):
    return _get_by_id(connection, "open_questions", question_id)


def list_open_questions(connection, project_id):
    return _list_by_project(
        connection,
        "open_questions",
        project_id,
        """
        CASE status
            WHEN 'open' THEN 1
            WHEN 'deferred' THEN 2
            WHEN 'answered' THEN 3
            ELSE 4
        END,
        created_at,
        id
        """,
    )


def create_glossary_term(connection, project_id, term, definition, aliases=None):
    term_id = _insert(
        connection,
        "glossary_terms",
        {
            "project_id": project_id,
            "term": term,
            "definition": definition,
            "aliases": aliases,
        },
    )
    return get_glossary_term(connection, term_id)


def get_glossary_term(connection, term_id):
    return _get_by_id(connection, "glossary_terms", term_id)


def list_glossary_terms(connection, project_id):
    return _list_by_project(connection, "glossary_terms", project_id, "term")


def create_note(connection, project_id, title, body, tags=None):
    note_id = _insert(
        connection,
        "notes",
        {
            "project_id": project_id,
            "title": title,
            "body": body,
            "tags": tags,
        },
    )
    return get_note(connection, note_id)


def get_note(connection, note_id):
    return _get_by_id(connection, "notes", note_id)


def list_notes(connection, project_id):
    return _list_by_project(connection, "notes", project_id, "created_at DESC, id DESC")


def create_agent_log(
    connection,
    project_id,
    summary,
    agent_name=None,
    changed_files=None,
    checks_run=None,
    known_issues=None,
    next_task=None,
):
    log_id = _insert(
        connection,
        "agent_logs",
        {
            "project_id": project_id,
            "agent_name": agent_name,
            "summary": summary,
            "changed_files": changed_files,
            "checks_run": checks_run,
            "known_issues": known_issues,
            "next_task": next_task,
        },
    )
    return get_agent_log(connection, log_id)


def get_agent_log(connection, log_id):
    return _get_by_id(connection, "agent_logs", log_id)


def list_agent_logs(connection, project_id):
    return _list_by_project(connection, "agent_logs", project_id, "created_at DESC, id DESC")

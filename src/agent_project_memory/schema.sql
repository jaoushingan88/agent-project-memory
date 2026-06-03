PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS app_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT NOT NULL UNIQUE,
    description TEXT,
    root_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS context_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    section TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    position INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    UNIQUE (project_id, section)
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('proposed', 'accepted', 'superseded')),
    decision TEXT NOT NULL,
    rationale TEXT,
    consequences TEXT,
    supersedes_decision_id INTEGER,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    FOREIGN KEY (supersedes_decision_id) REFERENCES decisions (id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS open_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('open', 'answered', 'deferred')),
    question TEXT NOT NULL,
    context TEXT,
    answer TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS glossary_terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    aliases TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
    UNIQUE (project_id, term)
);

CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    tags TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS agent_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    agent_name TEXT,
    summary TEXT NOT NULL,
    changed_files TEXT,
    checks_run TEXT,
    known_issues TEXT,
    next_task TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_context_entries_project_id
    ON context_entries (project_id);

CREATE INDEX IF NOT EXISTS idx_context_entries_project_position
    ON context_entries (project_id, position);

CREATE INDEX IF NOT EXISTS idx_decisions_project_id
    ON decisions (project_id);

CREATE INDEX IF NOT EXISTS idx_decisions_project_status
    ON decisions (project_id, status);

CREATE INDEX IF NOT EXISTS idx_open_questions_project_id
    ON open_questions (project_id);

CREATE INDEX IF NOT EXISTS idx_open_questions_project_status
    ON open_questions (project_id, status);

CREATE INDEX IF NOT EXISTS idx_glossary_terms_project_id
    ON glossary_terms (project_id);

CREATE INDEX IF NOT EXISTS idx_notes_project_id
    ON notes (project_id);

CREATE INDEX IF NOT EXISTS idx_notes_created_at
    ON notes (created_at);

CREATE INDEX IF NOT EXISTS idx_agent_logs_project_id
    ON agent_logs (project_id);

CREATE INDEX IF NOT EXISTS idx_agent_logs_created_at
    ON agent_logs (created_at);

INSERT INTO app_metadata (key, value)
VALUES ('schema_version', '1')
ON CONFLICT(key) DO UPDATE SET value = excluded.value;


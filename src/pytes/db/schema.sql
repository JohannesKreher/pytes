CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    theme TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS notes_fts
USING fts5(
    title,
    content,
    content='notes',
    content_rowid=id
);

CREATE TRIGGER [UPDATE_DT]
    AFTER UPDATE ON notes FOR EACH ROW
    WHEN OLD.modified_at = NEW.modified_at  OR OLD.modified_at  IS NULL
BEGIN
    UPDATE notes SET modified_at=CURRENT_TIMESTAMP WHERE id=NEW.id;
END;

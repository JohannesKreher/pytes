from typing import Literal
from utils import crypto
from utils.config import db_path, get_password
import sqlite3


def init_db():
    global con, cur
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    with open('db/schema.sql') as f:
        schema = f.read()
    cur.executescript(schema)
    con.commit()

def add_note(theme, title, content):
    crypto.decrypt_db(get_password())
    cur.execute('INSERT INTO notes (theme, title, content) VALUES (?, ?, ?)', (theme, title, content))
    con.commit()
    crypto.encrypt_db(get_password())

def update_a_note(id, theme, title, content):
    sql = "UPDATE notes SET theme = (?), title = (?), content = (?) WHERE id = (?)"
    crypto.decrypt_db(get_password())
    cur.execute(sql, (theme, title, content, id))
    con.commit()
    crypto.encrypt_db(get_password())

def get_notes_by_query(query: str, opt: Literal["Theme", "Title", "Content"])->list:
    opt = opt.lower()
    crypto.decrypt_db(get_password())
    sql = f"SELECT id, theme, title, content FROM notes WHERE {opt} LIKE ?;"
    entries = cur.execute(sql, (f"%{query}%",))
    crypto.encrypt_db(get_password())
    notes_list = entries.fetchall()
    return notes_list




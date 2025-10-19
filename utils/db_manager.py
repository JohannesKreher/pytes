from typing import Literal
from utils import crypto
import sqlite3

def init_db(db_path):
    global con, cur
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    with open('db/schema.sql') as f:
        schema = f.read()
    cur.executescript(schema)
    con.commit()

def add_note(password, theme, title, content):
    crypto.decrypt_db(password)
    cur.execute('INSERT INTO notes (theme, title, content) VALUES (?, ?, ?)', (theme, title, content))
    con.commit()
    crypto.encrypt_db(password)

def get_notes_by_query(password, query: str, opt: Literal["theme", "title", "content"])->list:
    crypto.decrypt_db(password)
    entries = cur.execute(f'SELECT theme, title, content FROM notes WHERE {opt} = (?)', ({query},))
    crypto.encrypt_db(password)
    notes_list = entries.fetchall()
    return notes_list




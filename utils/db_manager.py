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


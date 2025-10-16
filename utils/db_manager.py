import sqlite3

def init_db(db_path):
    global con, cur
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    with open('db/schema.sql') as f:
        schema = f.read()
    cur.executescript(schema)
    con.commit()

def add_note(theme, title, content):
    cur.execute('INSERT INTO notes VALUES (?, ?, ?)', (theme, title, content))


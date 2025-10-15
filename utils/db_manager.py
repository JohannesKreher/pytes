import sqlite3

def init_db(db_path):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    with open('db/schema.sql') as f:
        schema = f.read()
    cur.executescript(schema)
    con.commit()


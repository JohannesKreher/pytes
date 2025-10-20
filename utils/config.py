from pathlib import Path

db_path = Path("db/nodes.db")
password = bytes | None | None

def set_password(new_pw):
    global password
    password = new_pw

def get_password():
    return password
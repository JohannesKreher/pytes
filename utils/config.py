from pathlib import Path

search_not_by_only_one_char = False             # recommended to set True if you have a big notes db
db_path = Path("db/nodes.db")
password = bytes | None | None

def set_password(new_pw):
    global password
    password = new_pw

def get_password():
    return password
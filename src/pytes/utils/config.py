from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent  # points to pytes/
db_path = BASE_DIR / "db" / "notes.db"
schema_path = BASE_DIR / "db" / "schema.sql"


search_not_by_only_one_char = False             # recommended to set True if you have a big notes db
edit_mode = "VI"                                # VI / EMACS
password = bytes | None | None
marker = ">"                                    # len <= 4 / setup your own marker





def set_password(new_pw):
    global password
    password = new_pw

def get_password():
    return password

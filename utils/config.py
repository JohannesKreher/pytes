from pathlib import Path

search_not_by_only_one_char = False             # recommended to set True if you have a big notes db
edit_mode = "VI"                                # VI / EMACS
db_path = Path("db/nodes.db")
password = bytes | None | None
marker = ">"                                    # len <= 4 / setup your own marker





def set_password(new_pw):
    global password
    password = new_pw

def get_password():
    return password
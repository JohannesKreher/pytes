from utils import db_manager, ui, crypto
from pathlib import Path


db_path = Path('db/nodes.db')

def login():
    if not db_path.is_file():
        password = ui.register_screen()
        db_manager.init_db(db_path)
        crypto.encrypt_db(db_path, password)

    while True:
        password = ui.login_screen()
        if crypto.decrypt_db(db_path, password):
            break
    return password

def run(password):

    input("Press enter to continue...")







if __name__ == '__main__':
    password = login()
    try:
        run(password)
        crypto.encrypt_db(db_path, password)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        crypto.encrypt_db(db_path, password)

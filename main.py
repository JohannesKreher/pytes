from utils import db_manager, crypto, logic
from utils.ui import menu, register_screen, login_screen
from pathlib import Path


db_path = Path('db/nodes.db')

def login():
    if not db_path.is_file():
        password = register_screen()
        db_manager.init_db(db_path)
        crypto.encrypt_db(db_path, password)

    while True:
        password = login_screen()
        if crypto.decrypt_db(db_path, password):
            break
    return password

def run():
    while True:
        opr = menu()

        if opr == '4':
            raise KeyboardInterrupt
        elif opr == '1':
            logic.write_note()

        elif opr == '2':
            pass
        elif opr == '3':
            pass




if __name__ == '__main__':
    password = login()
    try:
        run()
        crypto.encrypt_db(db_path, password)
    except KeyboardInterrupt:
        print("\n\nExiting...")
        crypto.encrypt_db(db_path, password)

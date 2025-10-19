from utils import db_manager, crypto, logic
from utils.ui import menu, register_screen, login_screen
from utils.config import password, db_path
from pathlib import Path



def login()->bytes:
    global password
    if not db_path.is_file():
        password = register_screen()
        db_manager.init_db()
        crypto.encrypt_db(password)
        return password
    else:
        while True:
            password = login_screen()
            if crypto.decrypt_db(password):
                db_manager.init_db()
                crypto.encrypt_db(password)
                break
        return password

def run():
    while True:
        opr = menu()

        if opr == '4':
            raise KeyboardInterrupt
        elif opr == '1':
            logic.write_a_note(password)
        elif opr == '2':
            logic.select_a_note(password)
            #logic.read_a_note(password)
        elif opr == '3':
            pass


if __name__ == '__main__':
    try:
        password = login()
        run()
    except KeyboardInterrupt:
        print("\n\nExiting...")

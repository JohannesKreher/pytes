from utils import db_manager, crypto, logic
from utils.ui import menu, register_screen, login_screen
from utils.config import db_path, set_password, get_password

import test

def login()->bytes:
    if not db_path.is_file():
        new_password = register_screen()
        set_password(new_password)
        db_manager.init_db()
        crypto.encrypt_db(get_password())
    else:
        while True:
            new_password = login_screen()
            set_password(new_password)
            if crypto.decrypt_db(get_password()):
                db_manager.init_db()
                crypto.encrypt_db(get_password())
                break

def run():
    while True:
        opr = menu()

        if opr == '4':
            raise KeyboardInterrupt
        elif opr == '1':
            logic.write_a_note()
        elif opr == '2':
            logic.update_a_note()
        elif opr == '3':
            db_manager.d_encrypt_db()


if __name__ == '__main__':
    try:
        login()
        run()
    except KeyboardInterrupt:
        print("\n\nExiting...")

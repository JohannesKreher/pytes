from utils import db_manager, crypto, logic
from utils.ui import menu, register_screen, login_screen, print_info
from utils.config import db_path, set_password, get_password


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
                input("iii")
                db_manager.init_db(False)
                crypto.encrypt_db(get_password())
                break
            
def run():
    while True:
        opr = menu()

        if opr == '5':
            raise KeyboardInterrupt
        elif opr == '1':
            logic.write_a_note()
        elif opr == '2':
            logic.update_a_note()
        elif opr == '3':
            db_manager.decrypt_db_manually()
        elif opr == '4':
            print_info()


if __name__ == '__main__':
    try:
        login()
        run()
    except KeyboardInterrupt:
        print("\n\nExiting...")

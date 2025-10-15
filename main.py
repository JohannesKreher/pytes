from utils import db_manager, ui, crypto


from pathlib import Path

def run():
    db_path = Path('db/nodes.db')

    if not db_path.is_file():
        key = ui.register_screen()
        db_manager.init_db(db_path)
        crypto.encrypt_db(db_path, key)

    key = ui.login_screen()
    crypto.decrypt_db(db_path, key)

    input("Press enter to continue...")


if __name__ == '__main__':
    run()
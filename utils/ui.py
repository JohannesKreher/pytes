import getpass

def login_screen()->str:
    key = getpass.getpass('Password: ').strip()
    return str(key)

def register_screen()->str:
    print("Ensure that you dont forget your password!")
    while True:
        key = getpass.getpass('Password: ').strip()
        key_confirm = getpass.getpass('Confirm Password: ').strip()
        if key != key_confirm:
            print("Passwords don't match!")
            continue
        else:
            return str(key)



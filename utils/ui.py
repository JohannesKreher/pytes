import getpass

def login_screen()->bytes:
    print('Logging in...')
    password = getpass.getpass('Password: ').strip()
    return password.encode()

def register_screen()->bytes:
    print("Registering new account.")
    print("Ensure that you dont forget your password!")
    while True:
        password = getpass.getpass('Password: ').strip()
        password_confirm = getpass.getpass('Confirm Password: ').strip()
        if password != password_confirm:
            print("Passwords don't match!")
            continue
        else:
            return password.encode()



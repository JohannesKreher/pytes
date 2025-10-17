import getpass, os, termcolor



#_________________ login / register / menu

def menu():
    c()
    print(termcolor.colored(logo, "cyan"))
    print("1 -> Write a note")
    print("2 -> Read a note")
    print("3 -> Search in notes")
    print("4 -> Exit")

    choice = input("\n\n-> ")
    return choice

def login_screen()->bytes:
    c()
    print('Logging in...\n')
    password = getpass.getpass('Password: ').strip()
    return password.encode()

def register_screen()->bytes:
    c()
    print("Registering new account.")
    print("Ensure that you dont forget your password!\n")
    while True:
        password = getpass.getpass('Password: ').strip()
        password_confirm = getpass.getpass('Confirm Password: ').strip()
        if password != password_confirm:
            print("Passwords don't match!")
            continue
        else:
            return password.encode()

#__________ intern recourses
def c():
    os.system('clear')
logo = r"""
    ██████╗ ██╗   ██╗████████╗███████╗███████╗
    ██╔══██╗╚██╗ ██╔╝╚══██╔══╝██╔════╝██╔════╝
    ██████╔╝ ╚████╔╝    ██║   █████╗  ███████╗
    ██╔═══╝   ╚██╔╝     ██║   ██╔══╝  ╚════██║
    ██║        ██║      ██║   ███████╗███████║
    ╚═╝        ╚═╝      ╚═╝   ╚══════╝╚══════╝
                Pytes Notes CLI
    """





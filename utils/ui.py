from random import choice
from getpass import getpass
import os
from utils import apps



def print_info():
    c()
    print(info)
    input("\nPress enter to continue...")

#_________________ login / register / menu

def menu():
    c()
    print(RANDC + logo + ENDC)
    print("1 -> Write a note")
    print("2 -> Search in notes")
    print("3 -> Decrypt-db")
    print("4 -> Hints")
    print("5 -> Exit")
    choice = input("\n\n-> ")
    return choice

def login_screen()->bytes:
    c()
    print('Logging in...\n')
    password = getpass('Password: ').strip()
    return password.encode()

def register_screen()->bytes:
    c()
    print("Registering new account.")
    print("Ensure that you dont forget your password!\n")
    while True:
        password = getpass('Password: ').strip()
        password_confirm = getpass('Confirm Password: ').strip()
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
bcolors = {
    "MAGENTA": "\033[95m",
    "BLUE": "\033[94m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m"
}
ENDC = '\033[0m'
RANDC = choice([c for n, c in bcolors.items()])
info = ("_ _ _/The Hints you ware searching for\_ _ _\n"
        "\n"
        "* There is a smale config file on utils/config.py\n"
        "* Default is VI-movement (you can change to EMACS in config).\n"
        "\n"
        "* Global-keybindings:\n"
        "\t- CTRL-d    -> Delete a note\n"
        "\t- CTRL-e    -> Go back\n"
        "\t- CTRL-c    -> Quit\n"
        "\t- TAB       -> Focus next\n"
        "\t- SHIFT-TAB -> Focus previous\n"
        "\n"
        "* Search-pane-keybindings:\n"
        "\n"
        "\t- ENTER     -> Select filter/entry\n"
        "\t- /         -> Select by number\n"
        "\t- UP/DOWN   -> Move Up/Down\n"
        "\t- CTRL-k/j  -> Scroll Up/Down\n")





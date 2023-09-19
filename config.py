import subprocess
from checks import *

from utils import *

from enum import Enum


class config_menu(Enum):
    CHECK = 'c'
    CONFIG_NAME = 'n'
    CONFIG_EMAIL = 'e'
    MANAGE_BRANCHES = 'm'

def configuration():
    while True:
        print(f"\n{GREEN}Configuration:{ENDC}")
        print("[c] Check user name and user email")
        print("[n] Configure user name")
        print("[e] Configure user email")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == config_menu.CHECK.value:
            check_user_config()
        elif choice == config_menu.CONFIG_NAME.value:
            configure_user_name()
        elif choice == config_menu.CONFIG_EMAIL.value:
            configure_user_email()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()

def check_user_config():
    try:
        user_name = subprocess.getoutput("git config user.name")
        user_email = subprocess.getoutput("git config user.email")
        print(f"User Name: {user_name}")
        print(f"User Email: {user_email}")
    except Exception as e:
        print(f"Error checking user configuration: {e}")

def configure_user_name():
    user_name = input("Enter your desired user name: ")
    try:
        subprocess.run(["git", "config", "--global", "user.name", user_name])
        print(f"User name set to: {user_name}")
    except Exception as e:
        print(f"Error setting user name: {e}")

def configure_user_email():
    user_email = input("Enter your desired user email: ")
    try:
        subprocess.run(["git", "config", "--global", "user.email", user_email])
        print(f"User email set to: {user_email}")
    except Exception as e:
        print(f"Error setting user email: {e}")
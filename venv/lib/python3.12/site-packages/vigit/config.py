import subprocess
import os

from .utils import YELLOW, GREEN, ENDC, global_menu

from enum import Enum
from simple_term_menu import TerminalMenu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)
    
class config_menu(Enum):
    CHECK = 'See Repos'
    CONFIG_NAME = 'Name Configuration'
    CONFIG_EMAIL = 'Email Configuration'
    MANAGE_BRANCHES = 'Manage Branches'

def configuration():
    while True:
        
        print(f"\n{GREEN}Configuration:{ENDC}")

        menu_options = [
            f"{config_menu.CHECK.value}",
            f"{config_menu.CONFIG_NAME.value}",
            f"{config_menu.CONFIG_EMAIL.value}",
            f"{config_menu.MANAGE_BRANCHES.value}",
            f"{global_menu.BACK.value}",
            f"{global_menu.QUIT.value}",
        ]
        
        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_user_config()
        elif menu_entry_index == 1:
            configure_user_name()
        elif menu_entry_index == 2:
            configure_user_email()
        elif menu_entry_index == 3:
            clear_screen()
            break
        elif menu_entry_index == 4:
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
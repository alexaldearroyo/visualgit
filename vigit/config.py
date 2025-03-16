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
    CHECK = 'See Credentials'
    CONFIG_NAME = 'Name Configuration'
    CONFIG_EMAIL = 'Email Configuration'
    CONFIG_GITHUB_API = 'GitHub API Configuration'

def configuration():
    while True:

        print(f"\n{GREEN}Configuration:{ENDC}")

        menu_options = [
            f"[s] {config_menu.CHECK.value}",
            f"[n] {config_menu.CONFIG_NAME.value}",
            f"[e] {config_menu.CONFIG_EMAIL.value}",
            f"[g] {config_menu.CONFIG_GITHUB_API.value}",
            f"[x] {global_menu.BACK.value}",
            f"[q] {global_menu.QUIT.value}"
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
            configure_github_api()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
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

def configure_github_api():
    print("\nTo use the GitHub API, you need a Personal Access Token (PAT).")
    print("\nSteps to create a token:")
    print("1. Go to: https://github.com/settings/tokens")
    print("2. Click on 'Generate new token (classic)'")
    print("3. Give it a descriptive name (for example: 'VisualGit Token')")
    print("4. IMPORTANT: In permissions, you MUST check the full 'repo' checkbox")
    print("   This will allow you to create and manage repositories from VisualGit")
    print("\nNOTE: If your token already exists but you can't create repositories,")
    print("      you need to create a new one with the 'repo' permissions checked.")

    token = input("\nEnter your GitHub token (it will be stored securely): ")
    try:
        # Save token securely using git config
        subprocess.run(["git", "config", "--global", "github.token", token])
        print(f"\n{GREEN}GitHub token successfully saved.{ENDC}")
    except Exception as e:
        print(f"\n{YELLOW}Error saving GitHub token: {e}{ENDC}")

def invalid_opt():
    print("Invalid option selected. Please try again.")

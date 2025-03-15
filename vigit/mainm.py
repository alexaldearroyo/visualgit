import subprocess
import os

from .checks import is_git_repo, print_not_git_repo, is_connected_to_remote, print_connected_to_remote, print_not_connected_to_remote, print_git_repo
from .utils import YELLOW, GREEN, ENDC

from enum import Enum
from simple_term_menu import TerminalMenu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)


class main_menu(Enum):
    LOCAL = 'Local'
    LOCAL_TO_REMOTE = 'Local to Remote'
    REMOTE_TO_LOCAL = 'Remote to Local'
    MANAGE_REPOS = 'Manage Repos'


def work_in_main():
    while True:

        print(f"\n{GREEN}Work in main: {ENDC}")

        menu_options = [
            f"[l] {main_menu.LOCAL.value}",
            f"[t] {main_menu.LOCAL_TO_REMOTE.value}",
            f"[r] {main_menu.REMOTE_TO_LOCAL.value}",
            f"[m] {main_menu.MANAGE_REPOS.value}",
            "[x] Back to main menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            main_local()
        elif menu_entry_index == 1:
            main_local_to_remote()
        elif menu_entry_index == 2:
            main_remote_to_local()
        elif menu_entry_index == 3:
            main_manage_repos()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            quit()
        else:
            invalid_opt()


# MAIN LOCAL
class main_local_menu(Enum):
    CHECK_LOCAL = 'See Local Repos'
    ADD_LOCAL = 'Add a Local Repo'
    COMMIT_LOCAL = 'Commit to Local Repo'


def main_local():
    while True:

        print(f"\n{GREEN}Main -Local:{ENDC}")

        menu_options = [
            f"[s] {main_local_menu.CHECK_LOCAL.value}",
            f"[a] {main_local_menu.ADD_LOCAL.value}",
            f"[c] {main_local_menu.COMMIT_LOCAL.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_repos()
        elif menu_entry_index == 1:
            create_local_repo()
        elif menu_entry_index == 2:
            commit_to_local_repo()
        elif menu_entry_index == 3:
            clear_screen()
            break
        elif menu_entry_index == 4:
            quit()

def check_local_repos():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "status"])
    except Exception as e:
            print(f"Error executing git status: {e}")

def create_local_repo():
    if is_git_repo():
        print_git_repo()
        return

    try:
        subprocess.run(["git", "init"])
        print("Local repository has been successfully created in the present working directory.")
    except Exception as e:
        print(f"Error while creating local repository: {e}")

def commit_to_local_repo():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])

    except Exception as e:
        print(f"Error making commit: {e}")


# MAIN LOCAL_TO_REMOTE
class main_lr_menu(Enum):
    CHECK_REMOTE = 'See Remote Repos'
    LINK = 'Join Local to Remote'
    PUSH = 'Push Changes to Remote'
    COMMIT_AND_PUSH = 'Commit & Push'


def main_local_to_remote():
    while True:

        print(f"\n{GREEN}Main -Local to remote:{ENDC}")

        menu_options = [
            f"[s] {main_lr_menu.CHECK_REMOTE.value}",
            f"[j] {main_lr_menu.LINK.value}",
            f"[p] {main_lr_menu.PUSH.value}",
            f"[c] {main_lr_menu.COMMIT_AND_PUSH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_remote_repos()
        elif menu_entry_index == 1:
            connect_local_with_remote()
        elif menu_entry_index == 2:
            push_changes_to_remote()
        elif menu_entry_index == 3:
            commit_and_push()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            quit()

def check_remote_repos():
    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return
    try:
        subprocess.run(["git", "remote", "-v"])
    except Exception as e:
        print(f"Error checking remote repository: {e}")

def connect_local_with_remote():
    if not is_git_repo():
        print_not_git_repo()
        return

    if is_connected_to_remote():
        print_connected_to_remote()
        return

    remote_url = input("Enter the remote repository (GitHub) URL: ")
    try:
        subprocess.run(["git", "remote", "add", "origin", remote_url])
        print(f"Connected local repository with remote: {remote_url}")
    except Exception as e:
        print(f"Error connecting with remote: {e}")

def push_changes_to_remote():

    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    try:
        subprocess.run(["git", "push", "-u", "origin", "main"])
    except Exception as e:
        print(f"Error pushing changes to remote: {e}")

def commit_and_push():

    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push", "origin", "main"])
    except Exception as e:
        print(f"Error committing and pushing: {e}")


# MAIN REMOTE_TO_LOCAL
class main_rl_menu(Enum):
    CLONE = 'Join Remote to Local'
    REMOTE_TO_LOCAL = 'Join Remote to Local'
    PULL = 'Yank Changes from Remote'


def main_remote_to_local():
    while True:

        print(f"\n{GREEN}Main -Remote to local:{ENDC}")

        menu_options = [
            f"[s] {main_lr_menu.CHECK_REMOTE.value}",
            f"[j] {main_rl_menu.CLONE.value}",
            f"[y] {main_rl_menu.PULL.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_remote_repos()
        elif menu_entry_index == 1:
            clone_remote_to_local()
        elif menu_entry_index == 2:
            pull_remote_changes()
        elif menu_entry_index == 3:
            clear_screen()
            break
        elif menu_entry_index == 4:
            quit()

def clone_remote_to_local():
    remote_url = input("Enter the remote repository (GitHub) URL to clone: ")
    directory_name = input("Enter the directory name for the cloned repo (leave empty for default): ")
    try:
        if directory_name:
            subprocess.run(["git", "clone", remote_url, directory_name])
        else:
            subprocess.run(["git", "clone", remote_url])
        print(f"Successfully cloned {remote_url} to {directory_name if directory_name else 'current directory'}.")
    except Exception as e:
        print(f"Error cloning remote repository: {e}")

def pull_remote_changes():
    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    try:
        subprocess.run(["git", "pull"])
        print("Successfully pulled changes from remote.")
    except Exception as e:
        print(f"Error pulling changes from remote: {e}")


# MAIN MANAGE_REPOS
class manage_menu(Enum):
    DELETE_LOCAL = 'Delete Local Repo'
    DELETE_REMOTE = 'Delete Remote Repo'

def main_manage_repos():
    while True:

        print(f"\n{GREEN}Main -Manage repos:{ENDC}")

        menu_options = [
            f"[l] {main_local_menu.CHECK_LOCAL.value}",
            f"[r] {main_lr_menu.CHECK_REMOTE.value}",
            f"[d] {manage_menu.DELETE_LOCAL.value}",
            f"[e] {manage_menu.DELETE_REMOTE.value}",
            f"[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_repos()
        elif menu_entry_index == 1:
            check_remote_repos()
        elif menu_entry_index == 2:
            delete_local_repo()
        elif menu_entry_index == 3:
            delete_remote_repo()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            quit()


def delete_local_repo():
    if not is_git_repo():
        print_not_git_repo()
        return

    confirm = input("Are you sure you want to delete the local git repository? (yes/no): ").lower()
    if confirm == 'yes':
        try:
            subprocess.run(["rm", "-rf", ".git"])
            print("Local repository deleted successfully.")
        except Exception as e:
            print(f"Error deleting local repository: {e}")
    else:
        print("Local repository deletion cancelled.")

def delete_remote_repo():
    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    print("To delete a remote repository, you need to do it through the web interface of your Git hosting provider (e.g., GitHub, GitLab).")
    print("This action cannot be performed directly through the git command line for security reasons.")

import subprocess
import os

from .checks import is_git_repo, print_not_git_repo, is_connected_to_remote, print_connected_to_remote, print_not_connected_to_remote, print_git_repo
from .utils import YELLOW, GREEN, ENDC
from .github_ops import create_github_repository
from .constants import MENU_CURSOR, MENU_CURSOR_STYLE

from enum import Enum
from simple_term_menu import TerminalMenu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)


class main_menu(Enum):
    LOCAL = 'Local'
    REMOTE = 'Remote'


def work_in_main():
    while True:

        print(f"\n{GREEN}Work in main: {ENDC}")

        menu_options = [
            f"[l] {main_menu.LOCAL.value}",
            f"[r] {main_menu.REMOTE.value}",
            "[x] Back to main menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            main_local()
        elif menu_entry_index == 1:
            main_remote()
        elif menu_entry_index == 2:
            clear_screen()
            break
        elif menu_entry_index == 3:
            quit()
        else:
            invalid_opt()


# MAIN LOCAL
class main_local_menu(Enum):
    ADD_LOCAL = 'Add a Local Repo'
    COMMIT_LOCAL = 'Commit to Local Repo'
    DELETE_LOCAL = 'Delete Local Repo'


def main_local():
    while True:

        print(f"\n{GREEN}Main -Local:{ENDC}")

        menu_options = [
            f"[a] {main_local_menu.ADD_LOCAL.value}",
            f"[c] {main_local_menu.COMMIT_LOCAL.value}",
            f"[d] {main_local_menu.DELETE_LOCAL.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            create_local_repo()
        elif menu_entry_index == 1:
            commit_to_local_repo()
        elif menu_entry_index == 2:
            delete_local_repo()
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
        # Obtener la ruta absoluta del repositorio
        repo_path = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener el nombre del repositorio (último elemento de la ruta)
        repo_name = repo_path.split('/')[-1]

        # Obtener la rama actual
        current = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener todas las ramas locales
        branches = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener remotos configurados
        remotes = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener un resumen del estado
        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Mostrar la información recopilada
        print(f"\n{GREEN}Local Repository:{ENDC}")
        print(f"Name: {GREEN}{repo_name}{ENDC}")
        print(f"Path: {repo_path}")
        print(f"Current branch: {GREEN}{current}{ENDC}")

        print(f"\n{GREEN}Local Branches:{ENDC}")
        if branches:
            print(branches)
        else:
            print("No local branches")

        print(f"\n{GREEN}Remote Repositories:{ENDC}")
        if remotes:
            print(remotes)
        else:
            print("No remote repositories configured")

        print(f"\n{GREEN}Repository Status:{ENDC}")
        if status:
            print(status)
        else:
            print("The workspace is clean")

        # Also show the last commit
        last_commit = subprocess.run(
            ["git", "log", "-1", "--oneline"],
            capture_output=True,
            text=True
        ).stdout.strip()

        print(f"\n{GREEN}Last Commit:{ENDC}")
        if last_commit:
            print(last_commit)
        else:
            print("No commits in this repository")

    except Exception as e:
        print(f"Error getting repository information: {e}")

def create_local_repo():
    if is_git_repo():
        print_git_repo()
        return

    try:
        subprocess.run(["git", "init"])
        print("Local repository successfully created in the current directory.")
    except Exception as e:
        print(f"Error while creating the repository: {e}")

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


# MAIN REMOTE
class main_remote_menu(Enum):
    ADD_REMOTE = 'Add Remote Repo'
    LINK = 'Join Local to Remote'
    COMMIT_AND_PUSH = 'Commit & Push'
    CLONE = 'Fork Remote to Local'
    PULL = 'Yank Changes from Remote'
    DELETE_REMOTE = 'Delete Remote Repo'

def main_remote():
    while True:
        print(f"\n{GREEN}Main -Remote:{ENDC}")

        menu_options = [
            f"[a] {main_remote_menu.ADD_REMOTE.value}",
            f"[j] {main_remote_menu.LINK.value}",
            f"[p] {main_remote_menu.COMMIT_AND_PUSH.value}",
            f"[f] {main_remote_menu.CLONE.value}",
            f"[y] {main_remote_menu.PULL.value}",
            f"[d] {main_remote_menu.DELETE_REMOTE.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            create_remote_repo()
        elif menu_entry_index == 1:
            connect_local_with_remote()
        elif menu_entry_index == 2:
            commit_and_push()
        elif menu_entry_index == 3:
            clone_remote_to_local()
        elif menu_entry_index == 4:
            pull_remote_changes()
        elif menu_entry_index == 5:
            delete_remote_repo()
        elif menu_entry_index == 6:
            clear_screen()
            break
        elif menu_entry_index == 7:
            quit()

def create_remote_repo():
    if not is_git_repo():
        print_not_git_repo()
        return

    name = input("Name for the GitHub repository: ")
    if not name:
        print("Operation cancelled: repository name not provided.")
        return

    description = input("Description (optional, press Enter to skip): ")

    while True:
        private_input = input("Private repository? (y/n): ").lower()
        if private_input in ['y', 'n']:
            private = private_input == 'y'
            break
        print("Please enter 'y' for private or 'n' for public.")

    remote_url = create_github_repository(name, description, private)
    if remote_url:
        try:
            subprocess.run(["git", "remote", "add", "origin", remote_url])
            print("Local repository successfully connected with GitHub.")
        except Exception as e:
            print(f"Error connecting to the remote repository: {e}")

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

def commit_and_push():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Get current branch
        branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                               capture_output=True, text=True).stdout.strip()

        if not branch:
            print("Error determining the current branch.")
            return

        # First we try to commit
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        commit_result = subprocess.run(["git", "commit", "-m", message])

        # We try to push
        push_result = subprocess.run(["git", "push", "origin", branch], capture_output=True, text=True)

        # If push fails, we offer options
        if push_result.returncode != 0:
            print(f"\n{YELLOW}Could not push directly. The remote and local branches have diverged.{ENDC}")
            print("\nAvailable options:")
            print("1. Pull and then Push (recommended)")
            print("2. Force Push (overwrites remote changes)")
            print("3. Cancel operation")

            choice = input("\nSelect an option (1-3): ")

            if choice == "1":
                # Pull with rebase to keep local commits at the end
                pull_result = subprocess.run(["git", "pull", "--rebase", "origin", branch])
                if pull_result.returncode == 0:
                    # Try push again
                    subprocess.run(["git", "push", "origin", branch])
                    print(f"{GREEN}Changes integrated and pushed successfully!{ENDC}")
                else:
                    print(f"{YELLOW}There were conflicts during the pull. Please resolve conflicts manually.{ENDC}")
            elif choice == "2":
                confirm = input(f"{YELLOW}WARNING! Force push will overwrite remote changes. Are you sure? (y/n): {ENDC}").lower()
                if confirm == 'y':
                    subprocess.run(["git", "push", "--force", "origin", branch])
                    print(f"{GREEN}Force push completed.{ENDC}")
                else:
                    print("Operation cancelled.")
            else:
                print("Operation cancelled.")
        else:
            print(f"{GREEN}Commit and push completed successfully to branch {branch}!{ENDC}")

    except Exception as e:
        print(f"Error during commit and push: {e}")

def check_remote_repos():
    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return
    try:
        subprocess.run(["git", "remote", "-v"])
    except Exception as e:
        print(f"Error checking remote repository: {e}")

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

def delete_remote_repo():
    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    print("To delete a remote repository, you need to do it through the web interface of your Git hosting provider (e.g., GitHub, GitLab).")
    print("This action cannot be performed directly through the git command line for security reasons.")

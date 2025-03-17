import subprocess
import os

from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC, BOLD, BG_PURPLE, BLACK_TEXT, WHITE_TEXT
from .constants import branch_remote_menu, branch_local_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main
from .menu import commit_and_push

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def branch_remote():
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        current = current_branch()
        branch_display = f"{BLACK_TEXT}{BG_PURPLE}{BOLD} Currently on: {current} {ENDC}"
        print(f"\n{GREEN}Branches -Remote{ENDC} {branch_display}")

        menu_options = [
            f"[r] {branch_remote_menu.CHECK_REMOTE_BRANCH.value}",
            f"[l] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[j] {branch_remote_menu.LINK_REMOTE_BRANCH.value}",
            f"[c] {branch_remote_menu.COMMIT_LOCAL_BRANCH.value}",
            f"[p] {branch_remote_menu.PUSH_BRANCH.value}",
            f"[k] {branch_remote_menu.COMMIT_PUSH_BRANCH.value}",
            f"[f] {branch_remote_menu.CLONE_BRANCH.value}",
            f"[y] {branch_remote_menu.PULL_BRANCH.value}",
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
            check_remote_branches()
        elif menu_entry_index == 1:
            check_local_branches()
        elif menu_entry_index == 2:
            connect_local_branch_with_remote()
        elif menu_entry_index == 3:
            commit_in_local_branch()
        elif menu_entry_index == 4:
            push_changes_to_remote_branch()
        elif menu_entry_index == 5:
            commit_and_push_in_branch()
        elif menu_entry_index == 6:
            clone_remote_branch_to_local()
        elif menu_entry_index == 7:
            pull_remote_changes_to_local()
        elif menu_entry_index == 8:
            clear_screen()
            break
        elif menu_entry_index == 9:
            quit()

def check_local_branches():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "branch"])
    except Exception as e:
        print(f"Error checking local branches: {e}")

def check_remote_branches():
    branch = current_branch()

    if not has_commits():
        print_not_commits()
        return
    elif not is_local_branch_connected_to_remote(branch):
        print(f"{YELLOW}The local branch {branch} is not connected to a remote branch. Please connect to remote branch to proceed{ENDC}\n To connect to remote branch: Work in branches -> Remote -> Join local branch to remote")
        return

    try:
        # Use --no-pager to prevent Git from using vi/less and capture the output to display it directly
        result = subprocess.run(["git", "--no-pager", "branch", "-r"],
                               capture_output=True,
                               text=True)

        branches = result.stdout.strip().split('\n')
        for branch in branches:
            print(f"  {branch}")
    except Exception as e:
        print(f"Error al mostrar las ramas remotas: {e}")

def connect_local_branch_with_remote():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    if is_local_branch_connected_to_remote(branch):
        print(f"{YELLOW}The local branch {branch} is already connected to a remote branch.{ENDC}")
        return

    # Verificar si el repositorio está conectado a un remoto
    try:
        remote_exists = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        ).stdout.strip() != ""

        if not remote_exists:
            remote_url = input("Enter the remote repository (GitHub) URL: ")
            subprocess.run(["git", "remote", "add", "origin", remote_url])
            print(f"Connected local repository with remote: {remote_url}")
    except Exception as e:
        print(f"Error connecting with remote: {e}")
        return

    try:
        # Crear la rama en remoto y enlazarla con la local
        # Primero hacemos push de la rama local al remoto
        push_result = subprocess.run(
            ["git", "push", "-u", "origin", branch],
            capture_output=True,
            text=True
        )

        if push_result.returncode == 0:
            print(f"{GREEN}Local branch {branch} successfully pushed and connected to remote.{ENDC}")
        else:
            print(f"{YELLOW}Could not push branch to remote. Error: {push_result.stderr.strip()}{ENDC}")

            # Si falló, intentamos establecer la conexión manualmente
            set_upstream = subprocess.run(
                ["git", "branch", "--set-upstream-to", f"origin/{branch}", branch]
            )

            if set_upstream.returncode == 0:
                print(f"{GREEN}Connected local branch {branch} with remote.{ENDC}")
            else:
                print(f"{YELLOW}Could not connect branch to remote.{ENDC}")
    except Exception as e:
        print(f"Error connecting local branch with remote: {e}")

def commit_in_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])
    except Exception as e:
        print(f"Error committing in local branch: {e}")

def push_changes_to_remote_branch():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    try:
        # Try to do a normal push first
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True
        )

        # If the normal push is successful
        if result.returncode == 0:
            print(f"{GREEN}Changes successfully sent to remote branch {branch}.{ENDC}")
        else:
            # If the push fails, show the error and offer force push
            print(f"{YELLOW}Could not send changes to remote branch.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Ask if they want to do a force push
            force_push = input(f"\nDo you want to force push? {YELLOW}WARNING: This may overwrite changes in the remote repository. This action is potentially destructive.{ENDC} (y/n): ").lower()

            if force_push == 'y':
                print(f"{YELLOW}Executing force push...{ENDC}")
                force_result = subprocess.run(
                    ["git", "push", "--force", "origin", branch],
                    capture_output=True,
                    text=True
                )

                if force_result.returncode == 0:
                    print(f"{GREEN}Force push completed. Changes have been forcibly sent to remote branch {branch}.{ENDC}")
                else:
                    print(f"{YELLOW}Force push failed: {force_result.stderr.strip()}{ENDC}")
            else:
                print("Push operation cancelled.")

    except Exception as e:
        print(f"Error sending changes to remote branch: {e}")

def commit_and_push_in_branch():
    # Call the main commit_and_push function which now works with the current branch
    commit_and_push()

def clone_remote_branch_to_local():
    remote_branch = input("Enter the name of the remote branch you want to clone: ")
    try:
        subprocess.run(["git", "checkout", "--track", f"origin/{remote_branch}"])
        print(f"Cloned and switched to the remote branch {remote_branch}")
    except Exception as e:
        print(f"Error cloning remote branch: {e}")

def pull_remote_changes_to_local():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    try:
        # Try to do a normal pull first
        result = subprocess.run(
            ["git", "pull", "origin", branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # If the normal pull is successful
        if result.returncode == 0:
            print(f"{GREEN}Remote changes successfully incorporated into local branch {branch}.{ENDC}")
        else:
            # If the pull fails, show the error and offer advanced options
            print(f"{YELLOW}Could not incorporate remote changes.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Ask what strategy they want to use
            print("\nAvailable options:")
            print("1. Rebase (repositions your changes on top of remote changes)")
            print("2. Force pull (discards uncommitted local changes)")
            print("3. Cancel operation")

            choice = input("\nSelect an option (1-3): ")

            if choice == "1":
                print(f"{YELLOW}Executing pull with rebase...{ENDC}")
                rebase_result = subprocess.run(
                    ["git", "pull", "--rebase", "origin", branch],
                    capture_output=True,
                    text=True
                )

                if rebase_result.returncode == 0:
                    print(f"{GREEN}Pull with rebase completed successfully.{ENDC}")
                else:
                    print(f"{YELLOW}Pull with rebase failed: {rebase_result.stderr.strip()}{ENDC}")
                    print("You may need to resolve conflicts manually.")

            elif choice == "2":
                confirm = input(f"{YELLOW}WARNING: This will discard all uncommitted local changes. Are you sure? (y/n): {ENDC}").lower()
                if confirm == "y":
                    # Save current work
                    subprocess.run(["git", "stash", "push", "-u"])
                    # Reset local changes
                    subprocess.run(["git", "reset", "--hard", f"origin/{branch}"])
                    print(f"{GREEN}Local changes have been reset to the state of the remote repository.{ENDC}")
                    print("Your uncommitted changes have been saved in git stash.")
                else:
                    print("Operation cancelled.")

            else:
                print("Operation cancelled.")

    except Exception as e:
        print(f"Error incorporating remote changes: {e}")

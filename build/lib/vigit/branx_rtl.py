import subprocess
from enum import Enum
from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC
from .constants import branch_rl_menu, branch_lr_menu, branch_local_menu
from .checks import is_git_repo, print_not_git_repo, current_branch

# BRANCHES REMOTE_TO_LOCAL
class branch_rl_menu(Enum):
    CLONE_BRANCH = 'Fork Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch to Local'

def branch_remote_to_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Remote to local{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Branches -Remote to local:{ENDC}")

        menu_options = [
            f"[s] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[l] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[j] {branch_rl_menu.CLONE_BRANCH.value}",
            f"[y] {branch_rl_menu.PULL_BRANCH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_remote_branches()
        elif menu_entry_index == 1:
            check_local_branches()
        elif menu_entry_index == 2:
            clone_remote_branch_to_local()
        elif menu_entry_index == 3:
            pull_remote_changes_to_local()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            quit()
        else:
            invalid_opt()

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

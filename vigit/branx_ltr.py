import subprocess
from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC
from .constants import branch_lr_menu, branch_local_menu
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main
from .mainm import commit_and_push

def branch_local_to_remote():
    if is_current_branch_main():
        print(f"{YELLOW}You are now in main. Go to a branch to proceed.{ENDC}\nTo go to a branch: Quick actions -> Go to branch")
        return

    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Local to remote{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Branches -Local to remote:{ENDC}")

        menu_options = [
            f"[s] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[j] {branch_lr_menu.LINK_REMOTE_BRANCH.value}",
            f"[c] {branch_lr_menu.COMMIT_LOCAL_BRANCH.value}",
            f"[p] {branch_lr_menu.PUSH_BRANCH.value}",
            f"[b] {branch_lr_menu.COMMIT_PUSH_BRANCH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_branches()
        elif menu_entry_index == 1:
            check_remote_branches()
        elif menu_entry_index == 2:
            connect_local_branch_with_remote()
        elif menu_entry_index == 3:
            commit_in_local_branch()
        elif menu_entry_index == 4:
            push_changes_to_remote_branch()
        elif menu_entry_index == 5:
            commit_and_push_in_branch()
        elif menu_entry_index == 6:
            clear_screen()
            break
        elif menu_entry_index == 7:
            quit()
        else:
            invalid_opt()

def check_remote_branches():
    branch = current_branch()

    if not has_commits():
        print_not_commits()
        return
    elif not is_local_branch_connected_to_remote(branch):
        print(f"{YELLOW}The local branch {branch} is not connected to a remote branch. Please connect to remote branch to proceed{ENDC}\n To connect to remote branch: Work in branches -> Local -> Link local branch to remote")
        return

    try:
        # Use --no-pager to prevent Git from using vi/less and capture the output to display it directly
        result = subprocess.run(["git", "--no-pager", "branch", "-r"],
                               capture_output=True,
                               text=True)

        branches = result.stdout.strip().split('\n')
        print("\nRamas remotas:")
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

    remote_url = input("Enter the remote repository (GitHub) URL: ")
    try:
        subprocess.run(["git", "branch", "--set-upstream-to", f"origin/{branch}", branch])
        print(f"Connected local branch {branch} with remote: {remote_url}")
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

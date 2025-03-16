import subprocess
from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC
from .constants import manage_branch_menu, branch_remote_menu, branch_local_menu
from .checks import is_git_repo, print_not_git_repo, current_branch, is_current_branch_main
from .branx_local import check_local_branches, go_to_branch, go_to_main, create_local_branch
from .branx_remote import check_remote_branches, connect_local_branch_with_remote
from .mainm import clear_screen

def manage_branches():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Manage branches{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Manage branches:{ENDC}")

        menu_options = [
            f"[a] {manage_branch_menu.ADD_BRANCH.value}",
            f"[j] {manage_branch_menu.LINK_BRANCH.value}",
            f"[l] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[r] {branch_remote_menu.CHECK_REMOTE_BRANCH.value}",
            f"[f] {manage_branch_menu.MERGE.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {branch_local_menu.GOTO_MAIN.value}",
            f"[d] {manage_branch_menu.DELETE_LOCAL_BRANCH.value}",
            f"[e] {manage_branch_menu.DELETE_REMOTE_BRANCH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            create_local_branch()
        elif menu_entry_index == 1:
            connect_local_branch_with_remote()
        elif menu_entry_index == 2:
            check_local_branches()
        elif menu_entry_index == 3:
            check_remote_branches()
        elif menu_entry_index == 4:
            merge_branch_with_main()
        elif menu_entry_index == 5:
            go_to_branch()
        elif menu_entry_index == 6:
            go_to_main()
        elif menu_entry_index == 7:
            delete_local_branch()
        elif menu_entry_index == 8:
            delete_remote_branch()
        elif menu_entry_index == 9:
            clear_screen()
            break
        elif menu_entry_index == 10:
            quit()

def merge_branch_with_main():
    if not is_git_repo():
        print_not_git_repo()
        return
    if is_current_branch_main():
        print(f"{YELLOW}You are already on the main branch. Go to another branch to proceed.{ENDC}\nTo go to another branch: Quick actions -> Go to branch")
        return

    branch = current_branch()
    if not branch or branch == "main":
        print("You are on the main branch or the current branch could not be determined.")
        return

    try:
        # Go to the main branch
        subprocess.run(["git", "checkout", "main"])

        # Try to do a normal merge first
        result = subprocess.run(
            ["git", "merge", branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # If the normal merge is successful
        if result.returncode == 0:
            print(f"{GREEN}Branch {branch} successfully merged with main.{ENDC}")
        else:
            # If the merge fails, show the error and offer options
            print(f"{YELLOW}Could not merge branch {branch} with main.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Offer options to resolve
            print("\nAvailable options:")
            print("1. Force merge (ours strategy - prioritizes main changes)")
            print("2. Force merge (theirs strategy - prioritizes branch changes)")
            print("3. Cancel operation")

            choice = input("\nSelect an option (1-3): ")

            if choice == "1":
                print(f"{YELLOW}Executing forced merge (ours)...{ENDC}")
                ours_result = subprocess.run(
                    ["git", "merge", "-X", "ours", branch],
                    capture_output=True,
                    text=True
                )

                if ours_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Main changes have been prioritized.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {ours_result.stderr.strip()}{ENDC}")

            elif choice == "2":
                print(f"{YELLOW}Executing forced merge (theirs)...{ENDC}")
                theirs_result = subprocess.run(
                    ["git", "merge", "-X", "theirs", branch],
                    capture_output=True,
                    text=True
                )

                if theirs_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Changes from branch {branch} have been prioritized.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {theirs_result.stderr.strip()}{ENDC}")

            else:
                print("Merge operation cancelled.")
                # Return to the original branch
                subprocess.run(["git", "checkout", branch])

    except Exception as e:
        print(f"Error merging branch with main: {e}")
        # Try to return to the original branch in case of error
        try:
            subprocess.run(["git", "checkout", branch])
        except:
            pass

def delete_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    # Show existing branches
    print("\nAvailable local branches:")
    check_local_branches()

    branch = input("\nEnter the name of the branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch.{ENDC}\nIf you want to delete the repository: Work in local -> Local -> Manage repos -> Delete local repo")
        return

    # Check if the branch exists
    try:
        branch_exists = subprocess.run(
            ["git", "show-ref", "--verify", f"refs/heads/{branch}"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not branch_exists:
            print(f"{YELLOW}The branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying branch existence: {e}")
        return

    # Check if it's the current branch
    current = current_branch()
    if current == branch:
        print(f"{YELLOW}You cannot delete the branch you are currently on.{ENDC}\nSwitch to another branch first using 'Go to Branch' or 'Go to Main'.")
        return

    # Try to delete the branch normally
    try:
        result = subprocess.run(
            ["git", "branch", "-d", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            # If it fails, probably has unmerged changes
            print(f"{YELLOW}Could not delete branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Ask if they want to force delete
            force_delete = input("\nDo you want to force deletion? This action is irreversible and you will lose all unmerged changes. (y/n): ").lower()

            if force_delete == 'y':
                force_result = subprocess.run(["git", "branch", "-D", branch])
                if force_result.returncode == 0:
                    print(f"{GREEN}The branch '{branch}' has been forcibly deleted.{ENDC}")
                else:
                    print(f"{YELLOW}Could not forcibly delete the branch: {force_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error deleting local branch: {e}")

def delete_remote_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    # Show available remote branches
    print("\nAvailable remote branches:")
    check_remote_branches()

    branch = input("\nEnter the name of the remote branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch of the remote repository.{ENDC}")
        return

    # Verify if the remote branch exists
    try:
        remote_branches = subprocess.run(
            ["git", "ls-remote", "--heads", "origin"],
            capture_output=True,
            text=True
        ).stdout

        if f"refs/heads/{branch}" not in remote_branches:
            print(f"{YELLOW}The remote branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying remote branch existence: {e}")
        return

    # Ask for confirmation
    confirm = input(f"\nAre you sure you want to delete the remote branch '{branch}'? This action is irreversible. (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

    # Delete the remote branch
    try:
        result = subprocess.run(
            ["git", "push", "origin", "--delete", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The remote branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            print(f"{YELLOW}Could not delete remote branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error deleting remote branch: {e}")

import subprocess
import sys
import os

from .utils import YELLOW, GREEN, ENDC
from .mainm import commit_to_local_repo
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main

from enum import Enum
from simple_term_menu import TerminalMenu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)


class branch_menu(Enum):
    BRANCH_LOCAL = 'Local'
    BRANCH_LOCAL_TO_REMOTE = 'Local to Remote'
    BRANCH_REMOTE_TO_LOCAL = 'Remote to Local'
    MANAGE_BRANCHES = 'Manage Branches'


def work_in_branches():
    current = current_branch()
    while True:

        print(f"\n{GREEN}Work in branches{ENDC} (Currently on: {current}):")

        menu_options = [
            f"[l] {branch_menu.BRANCH_LOCAL.value}",
            f"[t] {branch_menu.BRANCH_LOCAL_TO_REMOTE.value}",
            f"[r] {branch_menu.BRANCH_REMOTE_TO_LOCAL.value}",
            f"[m] {branch_menu.MANAGE_BRANCHES.value}",
            f"[a] Advanced operations",
            f"[x] Back to main menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            branch_local()
        elif menu_entry_index == 1:
            branch_local_to_remote()
        elif menu_entry_index == 2:
            branch_remote_to_local()
        elif menu_entry_index == 3:
            manage_branches()
        elif menu_entry_index == 4:
            advanced_operations()
        elif menu_entry_index == 5:
            clear_screen()
            break
        elif menu_entry_index == 6:
            sys.exit("Exiting VisualGit...\n")


# BRANCHES LOCAL
class branch_local_menu(Enum):
    CHECK_LOCAL_BRANCH = 'See Local Branches'
    ADD_LOCAL_BRANCH = 'Add a Local Branch'
    GOTO_BRANCH = 'Go to Branch'
    GOTO_MAIN = 'Go to Main'

def branch_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Local{ENDC} (Currently on: {current}):")
        else:
            print("\nBranches -Local:")

        options = [
            f"[s] See Local Branches",
            f"[a] Add a Local Branch",
            f"[c] Commit to Current Branch",
            f"[b] Go to Branch",
            f"[g] Go to Main",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_branches()
        elif menu_entry_index == 1:
            create_local_branch()
        elif menu_entry_index == 2:
            commit_to_local_repo()
        elif menu_entry_index == 3:
            go_to_branch()
        elif menu_entry_index == 4:
            go_to_main()
        elif menu_entry_index == 5:
            clear_screen()
            break
        elif menu_entry_index == 6:
            quit()

def check_local_branches():
    if not is_git_repo():
        print_not_git_repo()
        return
    elif not has_commits():
        print_not_commits()
        return
    try:
        # Use --no-pager to prevent Git from using vi/less and capture the output to display it directly
        result = subprocess.run(["git", "--no-pager", "branch"],
                               capture_output=True,
                               text=True)

        branches = result.stdout.strip().split('\n')
        print("\nRamas locales:")
        for branch in branches:
            print(f"  {branch}")
    except Exception as e:
        print(f"Error displaying local branches: {e}")

def create_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return
    elif not has_commits():
        print_not_commits()
        return

    branch_name = input("Enter the name of the new branch: ")
    try:
        subprocess.run(["git", "branch", branch_name])
        print(f"Branch {branch_name} created successfully.")
    except Exception as e:
        print(f"Error creating branch {branch_name}: {e}")

def go_to_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        result = subprocess.run(["git", "branch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        branches = result.stdout.strip().split('\n')
        if branches:
            print("Local branches:")
            for idx, branch in enumerate(branches, 1):
                print(f"{idx}. {branch}")
            choice = int(input("Select a branch to switch to (by number): "))
            if 1 <= choice <= len(branches):
                selected_branch = branches[choice - 1].replace('*', '').strip()  # Remove the '*' which indicates the current branch
                subprocess.run(["git", "checkout", selected_branch])
            else:
                print("Invalid choice.")
        else:
            print("No local branches found. Create one to proceed.")
    except Exception as e:
        print(f"Error switching branches: {e}")

def go_to_main():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "checkout", "main"])
    except Exception as e:
        print(f"Error switching to main branch: {e}")

def go_to_branch_force():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        result = subprocess.run(["git", "branch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        branches = result.stdout.strip().split('\n')

        if branches:
            print("Local branches:")
            for idx, branch in enumerate(branches, 1):
                print(f"{idx}. {branch}")

            choice = int(input("Select a branch to switch to (by number): "))

            if 1 <= choice <= len(branches):
                selected_branch = branches[choice - 1].replace('*', '').strip()  # Remove the '*' which indicates the current branch

                # Check if there are uncommitted changes
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    stdout=subprocess.PIPE,
                    text=True
                )

                if status_result.stdout.strip():
                    print(f"{YELLOW}You have uncommitted changes that will be lost when switching branches.{ENDC}")
                    force_option = input("What would you like to do?\n1. Save changes to stash and switch\n2. Discard changes and switch\n3. Cancel\nSelect option (1-3): ")

                    if force_option == "1":
                        # Save to stash and switch
                        subprocess.run(["git", "stash", "push", "-u", "-m", f"Automatic changes before switching to {selected_branch}"])
                        subprocess.run(["git", "checkout", selected_branch])
                        print(f"{GREEN}Changes saved to stash and switched to branch {selected_branch}.{ENDC}")
                        print("To recover your changes, use 'git stash pop' when you return to this branch.")
                    elif force_option == "2":
                        # Force switch discarding changes
                        subprocess.run(["git", "checkout", "-f", selected_branch])
                        print(f"{GREEN}Switched to branch {selected_branch}. Uncommitted changes have been discarded.{ENDC}")
                    else:
                        print("Operation cancelled.")
                else:
                    # No changes, switch normally
                    subprocess.run(["git", "checkout", selected_branch])
                    print(f"{GREEN}Switched to branch {selected_branch}.{ENDC}")
            else:
                print("Invalid option.")
        else:
            print("No local branches found. Create one to continue.")
    except Exception as e:
        print(f"Error switching branches: {e}")

# BRANCHES LOCAL_TO_REMOTE
class branch_lr_menu(Enum):
    CHECK_REMOTE_BRANCH = 'See Remote Branches'
    LINK_REMOTE_BRANCH = 'Join Local Branch to Remote'
    COMMIT_LOCAL_BRANCH = 'Commit to Local Branch'
    PUSH_BRANCH = 'Push Changes to Remote Branch'
    COMMIT_PUSH_BRANCH = 'Commit & Push in Branch'

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
    if not is_git_repo():
        print_not_git_repo()
        return

    branch = current_branch()
    if not branch:
        print("Error determining the current branch.")
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push", "origin", branch])
        print(f"Changes committed and pushed to branch {branch}")
    except Exception as e:
        print(f"Error committing and pushing in branch: {e}")


# BRANCHES REMOTE_TO_LOCAL
class branch_rl_menu(Enum):
    CLONE_BRANCH = 'Join Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'

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


# BRANCHES MANAGE_BRANCHES
class manage_branch_menu(Enum):
    MERGE = 'Merge One Branch with Main'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'
    DELETE_LOCAL_BRANCH = 'Delete Local Branch'
    DELETE_REMOTE_BRANCH = 'Delete Remote Branch'


def manage_branches():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Manage branches{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Manage branches:{ENDC}")

        menu_options = [
            f"[l] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[r] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[o] {manage_branch_menu.MERGE.value}",
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
            check_local_branches()
        elif menu_entry_index == 1:
            check_remote_branches()
        elif menu_entry_index == 2:
            merge_branch_with_main()
        elif menu_entry_index == 3:
            go_to_branch()
        elif menu_entry_index == 4:
            go_to_main()
        elif menu_entry_index == 5:
            delete_local_branch()
        elif menu_entry_index == 6:
            delete_remote_branch()
        elif menu_entry_index == 7:
            clear_screen()
            break
        elif menu_entry_index == 8:
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

# New section for advanced operations

def advanced_operations():
    while True:
        print(f"\n{GREEN}Advanced Operations{ENDC}")
        print(f"{YELLOW}WARNING: Some of these operations can be destructive.{ENDC}")

        menu_options = [
            "Reset (undo changes at specific levels)",
            "Clean (remove untracked files)",
            "Force push (forcefully send changes)",
            "Stash (temporarily save changes)",
            "Cherry-pick (select specific commits)",
            "Interactive rebase (reorganize/edit commits)",
            "Return to main menu"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Select an operation:")
        choice = terminal_menu.show()

        if choice == 0:
            reset_operations()
        elif choice == 1:
            clean_untracked_files()
        elif choice == 2:
            force_push()
        elif choice == 3:
            stash_operations()
        elif choice == 4:
            cherry_pick_commits()
        elif choice == 5:
            interactive_rebase()
        elif choice == 6:
            clear_screen()
            break

def reset_operations():
    print(f"\n{GREEN}Reset Operations{ENDC}")
    print(f"{YELLOW}WARNING: These operations can be destructive.{ENDC}")

    menu_options = [
        "Soft reset (preserves changes in staging area)",
        "Mixed reset (preserves changes in files but removes them from staging area)",
        "Hard reset (discards all local changes)",
        "Return to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select reset type:")
    choice = terminal_menu.show()

    if choice == 3:  # Return to previous menu
        return

    # Get the commit to reset to
    print("\nReset options:")
    print("1. Reset to the last commit")
    print("2. Reset to a specific number of commits back")
    print("3. Reset to a specific commit hash")

    reset_option = input("Select an option (1-3): ")

    reset_target = ""

    if reset_option == "1":
        reset_target = "HEAD~1"
    elif reset_option == "2":
        num_commits = input("How many commits back? ")
        try:
            reset_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Invalid number. Operation cancelled.")
            return
    elif reset_option == "3":
        # Show recent commits for reference
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
        reset_target = input("\nEnter the commit hash: ")
    else:
        print("Invalid option. Operation cancelled.")
        return

    # Confirm the operation
    confirm = input(f"{YELLOW}This operation can be destructive. Are you sure? (y/n): {ENDC}").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return


    # Execute the corresponding reset
    reset_type = ["--soft", "--mixed", "--hard"][choice]
    try:
        result = subprocess.run(
            ["git", "reset", reset_type, reset_target],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Reset {reset_type} completed successfully.{ENDC}")
            if reset_type == "--hard":
                print("All local changes have been discarded.")
            elif reset_type == "--soft":
                print("Changes have been preserved in the staging area.")
            else:  # mixed
                print("Changes have been preserved in files but removed from the staging area.")
        else:
            print(f"{YELLOW}Error executing reset: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during reset: {e}")

def clean_untracked_files():
    print(f"\n{GREEN}Clean untracked files{ENDC}")

    # Show untracked files
    print("\nUntracked files:")
    subprocess.run(["git", "ls-files", "--others", "--exclude-standard"])

    menu_options = [
        "Interactive mode (select files to delete)",
        "Delete all untracked files",
        "Delete untracked files and directories",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an option:")
    choice = terminal_menu.show()

    if choice == 3:  # Go back
        return

    # Confirm the operation
    if choice == 0:
        print("Starting interactive mode...")
        subprocess.run(["git", "clean", "-i"])
    else:
        # For options 1 and 2, ask for explicit confirmation
        clean_message = "all untracked files"
        clean_command = ["git", "clean", "-f"]

        if choice == 1:
            clean_message = "all untracked files"
        elif choice == 2:
            clean_message = "all untracked files and directories"
            clean_command = ["git", "clean", "-fd"]

        confirm = input(f"{YELLOW}Are you sure you want to delete {clean_message}? This action cannot be undone. (y/n): {ENDC}").lower()
        if confirm == "y":
            try:
                result = subprocess.run(clean_command, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"{GREEN}Cleaning completed successfully.{ENDC}")
                else:
                    print(f"{YELLOW}Error during cleaning: {result.stderr.strip()}{ENDC}")
            except Exception as e:
                print(f"Error during cleaning: {e}")
        else:
            print("Operation cancelled.")

def force_push():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    print(f"\n{GREEN}Force Push{ENDC}")
    print(f"{YELLOW}WARNING: This operation may overwrite changes in the remote repository.{ENDC}")

    # Offer options for different types of force push
    menu_options = [
        "Normal force push (--force)",
        "Safe force push (--force-with-lease)",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select the type of force push:")
    choice = terminal_menu.show()

    if choice == 2:  # Go back
        return

    # Confirm the operation
    warning_message = "This action may permanently overwrite remote changes."
    if choice == 0:
        confirm = input(f"{YELLOW}Normal force push: {warning_message} Are you sure? (y/n): {ENDC}").lower()
        push_option = "--force"
    else:  # choice == 1
        confirm = input(f"{YELLOW}Safe force push: Will only overwrite if there are no new changes in remote. Continue? (y/n): {ENDC}").lower()
        push_option = "--force-with-lease"

    if confirm != "y":
        print("Operation cancelled.")
        return

    # Execute the force push
    try:
        result = subprocess.run(
            ["git", "push", push_option, "origin", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Force push completed. Changes have been forcibly sent to remote branch {branch}.{ENDC}")
        else:
            print(f"{YELLOW}Force push failed: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during force push: {e}")

def stash_operations():
    print(f"\n{GREEN}Stash Operations{ENDC}")

    menu_options = [
        "Save changes to stash",
        "List saved stashes",
        "Apply stash (keeping in list)",
        "Apply and remove stash",
        "Delete specific stash",
        "Delete all stashes",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an operation:")
    choice = terminal_menu.show()

    if choice == 0:  # Save to stash
        message = input("Descriptive message for the stash (optional): ")
        try:
            if message:
                result = subprocess.run(["git", "stash", "push", "-m", message], capture_output=True, text=True)
            else:
                result = subprocess.run(["git", "stash", "push"], capture_output=True, text=True)

            if result.returncode == 0:
                if "No local changes to save" in result.stdout:
                    print("No local changes to save in stash.")
                else:
                    print(f"{GREEN}Changes successfully saved to stash.{ENDC}")
            else:
                print(f"{YELLOW}Error saving to stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 1:  # List stashes
        try:
            result = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
            if result.stdout.strip():
                print("\nSaved stashes:")
                print(result.stdout)
            else:
                print("No saved stashes.")
        except Exception as e:
            print(f"Error listing stashes: {e}")

    elif choice in [2, 3]:  # Apply stash
        # First list available stashes
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No saved stashes.")
                return

            print("\nAvailable stashes:")
            print(stash_list)

            stash_index = input("\nEnter the stash index (0 for most recent, 1 for next, etc.): ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Invalid index. Operation cancelled.")
                return

            if choice == 2:  # Apply keeping
                result = subprocess.run(["git", "stash", "apply", stash_ref], capture_output=True, text=True)
                success_message = "Stash applied successfully and kept in the list."
            else:  # choice == 3, apply and drop
                result = subprocess.run(["git", "stash", "pop", stash_ref], capture_output=True, text=True)
                success_message = "Stash applied successfully and removed from the list."

            if result.returncode == 0:
                print(f"{GREEN}{success_message}{ENDC}")
            else:
                print(f"{YELLOW}Error applying stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 4:  # Delete specific stash
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No saved stashes.")
                return

            print("\nAvailable stashes:")
            print(stash_list)

            stash_index = input("\nEnter the index of the stash to delete: ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Invalid index. Operation cancelled.")
                return

            confirm = input(f"{YELLOW}Are you sure you want to delete this stash? This action cannot be undone. (y/n): {ENDC}").lower()
            if confirm != "y":
                print("Operation cancelled.")
                return

            result = subprocess.run(["git", "stash", "drop", stash_ref], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{GREEN}Stash deleted successfully.{ENDC}")
            else:
                print(f"{YELLOW}Error deleting stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 5:  # Delete all stashes
        confirm = input(f"{YELLOW}Are you sure you want to delete ALL stashes? This action cannot be undone. (y/n): {ENDC}").lower()
        if confirm != "y":
            print("Operation cancelled.")
            return

        try:
            result = subprocess.run(["git", "stash", "clear"], capture_output=True, text=True)
            print(f"{GREEN}All stashes have been deleted.{ENDC}")
        except Exception as e:
            print(f"Error deleting stashes: {e}")

    elif choice == 6:  # Go back
        return

def cherry_pick_commits():
    print(f"\n{GREEN}Cherry-pick (select specific commits){ENDC}")

    # Show latest commits to select from
    print("\nLatest available commits:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "20"])
    except Exception as e:
        print(f"Error showing commits: {e}")
        return

    commit_hash = input("\nEnter the hash of the commit you want to apply: ")
    if not commit_hash:
        print("Operation cancelled.")
        return

    # Options for cherry-pick
    menu_options = [
        "Normal cherry-pick (create new commit)",
        "Cherry-pick without creating commit (--no-commit)",
        "Cherry-pick and edit commit message (--edit)",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an option:")
    choice = terminal_menu.show()

    if choice == 3:  # Go back
        return

    # Prepare command according to option
    cherry_pick_cmd = ["git", "cherry-pick"]
    if choice == 1:
        cherry_pick_cmd.append("--no-commit")
    elif choice == 2:
        cherry_pick_cmd.append("--edit")

    cherry_pick_cmd.append(commit_hash)

    # Execute cherry-pick
    try:
        result = subprocess.run(cherry_pick_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{GREEN}Cherry-pick completed successfully.{ENDC}")
            if choice == 1:
                print("Changes have been applied but no commit has been created. You can modify them and then commit.")
        else:
            print(f"{YELLOW}Error during cherry-pick: {result.stderr.strip()}{ENDC}")

            # Offer options in case of conflict
            if "conflict" in result.stderr:
                print("\nConflicts detected. Available options:")
                conflict_options = [
                    "Continue manually (resolve conflicts in editor)",
                    "Abort cherry-pick and return to previous state",
                    "Back to menu"
                ]

                conflict_menu = TerminalMenu(conflict_options, title="What do you want to do?")
                conflict_choice = conflict_menu.show()

                if conflict_choice == 0:
                    print("Continue resolving conflicts manually in your editor.")
                    print("After resolving them, use 'git add' for the modified files and 'git cherry-pick --continue'.")
                elif conflict_choice == 1:
                    abort_result = subprocess.run(["git", "cherry-pick", "--abort"], capture_output=True, text=True)
                    if abort_result.returncode == 0:
                        print(f"{GREEN}Cherry-pick aborted. Previous state has been restored.{ENDC}")
                    else:
                        print(f"{YELLOW}Error aborting cherry-pick: {abort_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during cherry-pick: {e}")

def interactive_rebase():
    print(f"\n{GREEN}Interactive Rebase{ENDC}")
    print(f"{YELLOW}WARNING: This operation rewrites commit history.{ENDC}")

    # Show recent commits for reference
    print("\nRecent commits:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
    except Exception as e:
        print(f"Error displaying commits: {e}")
        return

    # Rebase options
    print("\nSpecify how many commits you want to include in the rebase:")
    print("1. Last N commits")
    print("2. From a specific commit")
    print("3. Return to previous menu")

    rebase_option = input("Select an option (1-3): ")

    if rebase_option == "3" or not rebase_option:
        return

    rebase_target = ""
    if rebase_option == "1":
        num_commits = input("How many commits back? ")
        try:
            rebase_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Invalid number. Operation cancelled.")
            return
    elif rebase_option == "2":
        rebase_target = input("Enter the base commit hash: ")
    else:
        print("Invalid option. Operation cancelled.")
        return

    # Extra confirmation due to destructive nature
    confirm = input(f"{YELLOW}Interactive rebase will modify commit history. This operation can cause problems if commits have already been shared. Are you sure? (y/n): {ENDC}").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return

    # Execute interactive rebase
    print("\nThe editor will open for interactive rebase. Instructions:")
    print("- pick: keep the commit as is")
    print("- reword: keep the commit but change its message")
    print("- edit: keep the commit but pause to modify it")
    print("- squash: combine with previous commit (keeps both messages)")
    print("- fixup: combine with previous commit (discards its message)")
    print("- drop: remove the commit")
    print("\nSave and close the editor to continue with the rebase.")

    input("\nPress Enter to continue...")

    try:
        # The -i flag indicates interactive rebase
        result = subprocess.run(["git", "rebase", "-i", rebase_target])

        # The result will depend on user interaction with the editor
        if result.returncode == 0:
            print(f"{GREEN}Interactive rebase completed successfully.{ENDC}")
        else:
            print(f"{YELLOW}Interactive rebase did not complete successfully. There may be conflicts to resolve.{ENDC}")
    except Exception as e:
        print(f"Error during interactive rebase: {e}")

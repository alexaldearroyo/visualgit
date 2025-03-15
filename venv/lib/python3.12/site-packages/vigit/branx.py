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
            clear_screen()
            break
        elif menu_entry_index == 5:
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
        subprocess.run(["git", "branch"])
    except Exception as e:
        print(f"Error checking local branches: {e}")

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
        subprocess.run(["git", "branch", "-r"])
    except Exception as e:
        print(f"Error checking remote branches: {e}")

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
        subprocess.run(["git", "push", "origin", branch])
    except Exception as e:
        print(f"Error pushing changes to remote branch: {e}")

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


# BRANCHES REMOTE_TO LOCAL
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
        subprocess.run(["git", "pull", "origin", branch, "--allow-unrelated-histories"])
        print(f"Pulled changes from remote to local branch {branch}")
    except Exception as e:
        print(f"Error pulling changes from remote: {e}")


# BRANCHES MANAGE_BRANCHES
class manage_branch_menu(Enum):
    MERGE = 'Merge Branch with Main'
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
            f"[s] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[r] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[m] {manage_branch_menu.MERGE.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[gm] {branch_local_menu.GOTO_MAIN.value}",
            f"[dl] {manage_branch_menu.DELETE_LOCAL_BRANCH.value}",
            f"[dr] {manage_branch_menu.DELETE_REMOTE_BRANCH.value}",
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
        print(f"{YELLOW}You are now in main. Go to a branch to proceed.{ENDC}\nTo go to a branch: Quick actions -> Go to branch")
        return

    branch = current_branch()
    if not branch or branch == "main":
        print("You are either on the main branch or couldn't determine the current branch.")
        return

    try:
        subprocess.run(["git", "checkout", "main"])
        subprocess.run(["git", "merge", branch, "--allow-unrelated-histories"])
        print(f"Merged branch {branch} with main.")
    except Exception as e:
        print(f"Error merging branch with main: {e}")


def delete_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    check_local_branches()

    branch = input("Enter the name of the branch to delete: ")
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch.{ENDC}\nIf you want to to delete repository: Work in local -> Local -> Manage repos -> Delete local repo")
        return

    try:
        subprocess.run(["git", "branch", "-d", branch])
    except Exception as e:
        print(f"Error deleting local branch: {e}")


def delete_remote_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    branch = input("Enter the name of the remote branch to delete: ")
    if branch == "main":
        print("You cannot delete the main branch from remote.")
        return

    try:
        subprocess.run(["git", "push", "origin", "--delete", branch])
        print(f"Deleted remote branch {branch}.")
    except Exception as e:
        print(f"Error deleting remote branch: {e}")

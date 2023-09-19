import subprocess
from checks import *
import sys

from utils import *
from mainm import *

from enum import Enum


class branch_menu(Enum):
    BRANCH_LOCAL = 'l'
    BRANCH_LOCAL_TO_REMOTE = 'lr'
    BRANCH_REMOTE_TO_LOCAL = 'rl'
    MANAGE_BRANCHES = 'm'


def work_in_branches():
    current = current_branch()
    while True:
        print(f"\n{GREEN}Work in branches{ENDC} (Currently on: {current}):")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[rl] Remote to local")
        print("[m] Manage branches")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == branch_menu.BRANCH_LOCAL.value:
            branch_local()
        elif choice == branch_menu.BRANCH_LOCAL_TO_REMOTE.value:
            branch_local_to_remote()
        elif choice == branch_menu.BRANCH_REMOTE_TO_LOCAL.value:
            branch_remote_to_local()
        elif choice == branch_menu.MANAGE_BRANCHES.value:
            manage_branches()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            sys.exit("Exiting VisualGit...\n")
        else:
            print("Invalid choice. Please select a valid option")


# BRANCHES LOCAL
class branch_local_menu(Enum):
    CHECK_LOCAL_BRANCH = 'cl'
    ADD_LOCAL_BRANCH = 'a'
    GOTO_BRANCH = 'g'
    GOTO_MAIN = 'gm'

def branch_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Local{ENDC} (Currently on: {current}):")
        else:
            print("\nBranches -Local:")
        print("[cl] Check local branches")
        print("[a] Add a local branch")
        print("[c] Commit in current branch")
        print("[g] Go to branch")
        print("[gm] Go to main")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == branch_local_menu.CHECK_LOCAL_BRANCH.value:
            check_local_branches()
        elif choice == branch_local_menu.ADD_LOCAL_BRANCH.value:
            create_local_branch()
        elif choice == main_local_menu.COMMIT_LOCAL.value:
            commit_to_local_repo()
        elif choice == branch_local_menu.GOTO_BRANCH.value:
            go_to_branch()
        elif choice == branch_local_menu.GOTO_MAIN.value:
            go_to_main()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()

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
    CHECK_REMOTE_BRANCH = 'cr'
    LINK_REMOTE_BRANCH = 'l'
    COMMIT_LOCAL_BRANCH = 'm'
    PUSH_BRANCH = 'p'
    COMMIT_PUSH_BRANCH = 'cb'
# test
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
        print("[cl] Check local branches")
        print("[cr] Check remote branches")
        print("[l] Link local branch to remote")
        print("[m] Commit in local branch")
        print("[p] Push changes to remote branch")
        print("[cb] Commit & Push in branch")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == branch_local_menu.CHECK_LOCAL_BRANCH.value:
            check_local_branches()
        elif choice == branch_lr_menu.CHECK_REMOTE_BRANCH.value:
            check_remote_branches()
        elif choice == branch_lr_menu.LINK_REMOTE_BRANCH.value:
            connect_local_branch_with_remote()
        elif choice == branch_lr_menu.COMMIT_LOCAL_BRANCH.value:
            commit_in_local_branch()
        elif choice == branch_lr_menu.PUSH_BRANCH.value:
            push_changes_to_remote_branch()
        elif choice == branch_lr_menu.COMMIT_PUSH_BRANCH.value:
            commit_and_push_in_branch()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
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
    CLONE_BRANCH = 'c'
    PULL_BRANCH = 'p'

def branch_remote_to_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Remote to local{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Branches -Remote to local:{ENDC}")
        print("[cr] Check remote branches")
        print("[cl] Check local branches")
        print("[c] Clone remote branch to local")
        print("[p] Pull remote branch changes to local")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == branch_lr_menu.CHECK_REMOTE_BRANCH.value:
            check_remote_branches()
        elif choice == branch_local_menu.CHECK_LOCAL_BRANCH.value:
            check_local_branches()
        elif choice == branch_rl_menu.CLONE_BRANCH.value:
            clone_remote_branch_to_local()
        elif choice == branch_rl_menu.PULL_BRANCH.value:
            pull_remote_changes_to_local()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
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
    MERGE = 'm'
    PULL_BRANCH = 'p'
    DELETE_LOCAL_BRANCH = 'dl'
    DELETE_REMOTE_BRANCH = 'dr'


def manage_branches():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Manage branches{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Manage branches:{ENDC}")
        print("[cl] Check local branches")
        print("[cr] Check remote branches")
        print("[m] Merge branch with main")
        print("[g] Go to branch")
        print("[gm] Go to main")
        print("[dl] Delete local branch")
        print("[dr] Delete remote branch")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == branch_local_menu.CHECK_LOCAL_BRANCH.value:
            check_local_branches()
        elif choice == branch_lr_menu.CHECK_REMOTE_BRANCH.value:
            check_remote_branches()
        elif choice == manage_branch_menu.MERGE.value:
            merge_branch_with_main()
        elif choice == branch_local_menu.GOTO_BRANCH.value:
            go_to_branch()
        elif choice == branch_local_menu.GOTO_MAIN.value:
            go_to_main()
        elif choice == manage_branch_menu.DELETE_LOCAL_BRANCH.value:
            delete_local_branch()
        elif choice == manage_branch_menu.DELETE_REMOTE_BRANCH.value:
            delete_remote_branch()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()


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
    
    list_local_branches()

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
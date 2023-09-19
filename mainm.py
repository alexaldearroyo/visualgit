import subprocess
from checks import *

from utils import *

from enum import Enum

# //test
class main_menu(Enum):
    LOCAL = 'l'
    LOCAL_TO_REMOTE = 'lr'
    REMOTE_TO_LOCAL = 'rl'
    MANAGE_REPOS = 'm'


def work_in_main():
    while True:
        print(f"\n{GREEN}Work in main:{ENDC}")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[rl] Remote to local")
        print("[m] Manage repos")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_menu.LOCAL.value:
            main_local()
        elif choice == main_menu.LOCAL_TO_REMOTE.value:
            main_local_to_remote()
        elif choice == main_menu.REMOTE_TO_LOCAL.value:
            main_remote_to_local()
        elif choice == main_menu.MANAGE_REPOS.value:
            main_manage_repos()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()


# MAIN LOCAL
class main_local_menu(Enum):
    CHECK_LOCAL = 'cl'
    ADD_LOCAL = 'a'
    COMMIT_LOCAL = 'c'


def main_local():
    while True:
        print(f"\n{GREEN}Main -Local:{ENDC}")
        print("[cl] Check local repos")
        print("[a] Add a local repo")
        print("[c] Commit to local repo")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_local_menu.CHECK_LOCAL.value:
            check_local_repos()
        elif choice == main_local_menu.ADD_LOCAL.value:
            create_local_repo()
        elif choice == main_local_menu.COMMIT_LOCAL.value:
            commit_to_local_repo()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()

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
    CHECK_REMOTE = 'cr'
    LINK = 'l'
    PUSH = 'p'
    COMMIT_AND_PUSH = 'cp'


def main_local_to_remote():
    while True:
        print(f"\n{GREEN}Main -Local to remote:{ENDC}")
        print("[cr] Check remote repos")
        print("[l] Link local repo with remote")
        print("[p] Push changes to remote")
        print("[cp] Commit & Push")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_lr_menu.CHECK_REMOTE.value:
            check_remote_repos()
        elif choice == main_lr_menu.LINK.value:
            connect_local_with_remote()
        elif choice == main_lr_menu.PUSH.value:
            push_changes_to_remote()
        elif choice == main_lr_menu.COMMIT_AND_PUSH.value:
            commit_and_push()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt

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
    CLONE = 'c'
    REMOTE_TO_LOCAL = 'rl'
    PULL = 'p'


def main_remote_to_local():
    while True:
        print(f"\n{GREEN}Main -Remote to local:{ENDC}")
        print("[cr] Check remote repos")
        print("[c] Clone remote repo to local")
        print("[p] Pull remote changes to local")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_lr_menu.CHECK_REMOTE.value:
            check_remote_repos()
        elif choice == main_rl_menu.CLONE.value:
            clone_remote_to_local()
        elif choice == main_rl_menu.PULL.value:
            pull_remote_changes()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()

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
    DELETE_LOCAL = 'dl'
    DELETE_REMOTE = 'dr'

def main_manage_repos():
    while True:
        print(f"\n{GREEN}Main -Manage repos:{ENDC}")
        print("[cl] Check local repos")
        print("[cr] Check remote repos")
        print("[dl] Delete local repo")
        print("[dr] Delete remote repo")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_local_menu.CHECK_LOCAL.value:
            check_local_repos()
        elif choice == main_lr_menu.CHECK_REMOTE.value:
            check_remote_repos()
        elif choice == manage_menu.DELETE_LOCAL.value:
            delete_local_repo()
        elif choice == manage_menu.DELETE_REMOTE.value:
            delete_remote_repo()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()

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


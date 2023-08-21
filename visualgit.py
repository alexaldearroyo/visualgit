import subprocess
import os
import sys

YELLOW = '\033[93m'
ENDC = '\033[0m'

def is_git_installed():
    try:
        result = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except Exception as e:
        pass
    return False
def is_git_repo():
    return os.path.exists('.git')
def print_git_repo():
    print(f"{YELLOW}The present working directory is already a git repository. No need to create one.{ENDC}")
def print_not_git_repo():
    print(f"{YELLOW}The present working directory is not a git repository, please create one to proceed.{ENDC}")
def is_connected_to_remote():
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False
def print_connected_to_remote():
    print(f"{YELLOW}The local repository is already connected to a remote repository.{ENDC}")
def print_not_connected_to_remote():
    print(f"{YELLOW}The local repository is not connected to a remote repository. Please connect it to proceed.{ENDC}")    


print("\nVISUAL GIT")
print("-"*30)


def main():
    if not is_git_installed():
        print("Git is not installed. You need to install git to use VisualGit.")
        return
        
    while True:
        print("\n[m] Work in main")
        print("[b] Work in branches")
        print("[l] Check log")
        print("[c] Configuration")
        print("[q] Quit program\n")

        choice = input("Please select an option: ")

        if choice == "m":
            work_in_main()
        elif choice == "b":
            work_in_branches()
        elif choice == "l":
            check_log()
        elif choice == "c":
            configuration()
        elif choice == "q":
            print("Exiting VisualGit...\n")
            break
        else:
            print("Invalid choice. Please select a valid option.")

# MAIN
def work_in_main():
    while True:
        print("\nWork in main:")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[rl] Remote to local")
        print("[m] Manage repos")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == "l":
            main_local()
        elif choice == "lr":
            main_local_to_remote()
        elif choice == "rl":
            main_remote_to_local()
        elif choice == "m":
            main_manage_repos()
        elif choice == "x":
            break
        elif choice == "q":
            sys.exit("Exiting VisualGit...\n")
        else:
            print("Invalid choice. Please select a valid option")

# MAIN -LOCAL
def main_local():
    while True:
        print("\nMain -Local:")
        print("[c] Check local repos")
        print("[a] Create a local repo")
        print("[m] Commit to local repo")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == "c":
            check_local_repos()
        elif choice == "a":
            create_local_repo()
        elif choice == "m":
            commit_to_local_repo()
        elif choice == "x":
            break
        elif choice == "q":
            sys.exit("Exiting VisualGit...\n")
        else:
            print("Invalid choice. Please select a valid option")

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
def main_local_to_remote():
    while True:
        print("\nMain -Local to remote:")
        print("[c] Check remote repos")
        print("[l] Link local repo with remote")
        print("[p] Push changes to remote")
        print("[cp] Commit & Push")
        print("[x] Back to previous menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == "c":
            check_remote_repos()
        elif choice == "l":
            connect_local_with_remote()
        elif choice == "p":
            push_changes_to_remote()
        elif choice == "cp":
            commit_and_push()
        elif choice == "x":
            break
        elif choice == "q":
            sys.exit("Exiting VisualGit...\n")
        else:
            print("Invalid choice. Please select a valid option")

    print("Transferring from local to remote...")

def check_remote_repos():
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
def main_remote_to_local():
    print("Transferring from remote to local...")


# MAIN MANAGE_REPOS
def main_manage_repos():
    print("Managing repositories...")


# BRANCHES
def work_in_branches():
    while True:
        print("\nWorking in branches:")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[m] Manage branches")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == "l":
            branch_local()
        elif choice == "lr":
            branch_local_to_remote()
        elif choice == "m":
            manage_branches()
        elif choice == "x":
            break
        elif choice == "q":
            sys.exit("Exiting VisualGit...\n")
        else:
            print("Invalid choice. Please select a valid option")

def branch_local():
    print("Working locally in branches...")

def branch_local_to_remote():
    print("Transferring from local branch to remote...")

def manage_branches():
    print("Managing branches...")


def check_log():
    subprocess.run(["git", "log"])

def configuration():
    # Aquí puedes agregar la funcionalidad para la configuración
    print("Configuration...")

if __name__ == "__main__":
    main()

import subprocess

def is_git_installed():
    try:
        result = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except Exception as e:
        pass
    return False

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
        print("[x] Exit\n")

        choice = input("Please select an option: ")

        if choice == "m":
            work_in_main()
        elif choice == "b":
            work_in_branches()
        elif choice == "l":
            check_log()
        elif choice == "c":
            configuration()
        elif choice == "x":
            print("Exiting VisualGit...\n")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def work_in_main():
    while True:
        print("\nWork in main:")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[rl] Remote to local")
        print("[m] Manage repos")
        print("[x] Back to main menu")

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
        else:
            print("Invalid choice. Please select a valid option")


def main_local():
    print("Working locally...")

def main_local_to_remote():
    print("Transferring from local to remote...")

def main_remote_to_local():
    print("Transferring from remote to local...")

def main_manage_repos():
    print("Managing repositories...")

def work_in_branches():
    while True:
        print("\nWorking in branches:")
        print("[l] Local")
        print("[lr] Local to remote")
        print("[m] Manage branches")
        print("[x] Back to main menu")

        choice = input("\nPlease select an option: ")

        if choice == "l":
            branch_local()
        elif choice == "lr":
            branch_local_to_remote()
        elif choice == "m":
            manage_branches()
        elif choice == "x":
            break
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

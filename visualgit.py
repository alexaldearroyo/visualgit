def main():
    while True:
        print("\nVISUAL GIT")
        print("-"*30)
        print("[m] Work in main")
        print("[b] Work in branches")
        print("[c] Configuration")
        print("[x] Exit\n")

        choice = input("Please select an option: ")

        if choice == "m":
            work_in_main()
        elif choice == "b":
            work_in_branches()
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
        print("[mr] Manage repos")
        print("[b] Back to main menu")

        choice = input("Please select an option: ")

        if choice == "1":
            local()
        elif choice == "lr":
            local_to_remote()
        elif choice == "rl":
            remote_to_local()
        elif choice == "mr":
            manage_repos()
        elif choice == "b":
            break
        else:
            print("Invalid choice. Please select a valid option")

def work_in_branches():
    # Aquí puedes agregar la funcionalidad para trabajar en branches
    print("Working in branches...")

def configuration():
    # Aquí puedes agregar la funcionalidad para la configuración
    print("Configuration...")

if __name__ == "__main__":
    main()

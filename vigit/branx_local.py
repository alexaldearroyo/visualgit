import subprocess
import os
from simple_term_menu import TerminalMenu
from .utils import BLUE, GREEN, ENDC, YELLOW, RED, WHITE, BG_BLUE, BOLD, BG_PURPLE, BLACK_TEXT
from .constants import branch_local_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo, has_commits, print_not_commits, current_branch
from .show_menu import get_single_keypress

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def branch_local():
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        current = current_branch()
        branch_display = f"{BLACK_TEXT}{BG_PURPLE}{BOLD} Currently on: {current} {ENDC}"
        print(f"\n{GREEN}Local branches{ENDC} {branch_display}")

        menu_options = [
            f"[s] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[a] {branch_local_menu.ADD_LOCAL_BRANCH.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {branch_local_menu.GOTO_MAIN.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
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
        for branch in branches:
            print(f"  {branch}")
    except Exception as e:
        print(f"Error displaying local branches: {e}")

def create_local_branch():
    """Crea una nueva rama local y opcionalmente se mueve a ella"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Add Local Branch:{ENDC}")

        # Obtener las ramas actuales para mostrarlas como referencia
        current_branch = subprocess.run(
            ["git", "--no-pager","branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        print(f"\n{YELLOW}Current branch: {current_branch}{ENDC}")

        print(f"\n{BLUE}Existing branches:{ENDC}")
        subprocess.run(["git", "--no-pager", "branch", "--color=always"], check=True)

        # Solicitar el nombre de la nueva rama
        print(f"\n{YELLOW}Enter the name for the new branch (leave empty to cancel):{ENDC}")
        branch_name = input("> ").strip()

        if not branch_name:
            print(f"\n{YELLOW}Operation cancelled.{ENDC}")
            return

        return create_branch_with_name(branch_name)

    except Exception as e:
        print(f"Error creating branch: {e}")

def create_branch_with_name(branch_name, switch_to_branch=False):
    """Crea una nueva rama local con el nombre especificado y opcionalmente se mueve a ella"""
    if not is_git_repo():
        print_not_git_repo()
        return False

    try:
        # Verificar si la rama ya existe
        existing_branches = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True,
            check=True
        ).stdout

        branch_exists = any(line.strip().replace("*", "").strip() == branch_name for line in existing_branches.split('\n') if line)

        if branch_exists:
            print(f"\n{RED}A branch with the name '{branch_name}' already exists.{ENDC}")
            return False

        # Obtener la rama actual para informar
        current_branch = subprocess.run(
            ["git", "--no-pager","branch", "--show-current"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        # Crear la nueva rama
        print(f"\n{YELLOW}Creating new branch: {branch_name}...{ENDC}")
        subprocess.run(["git", "branch", branch_name], check=True)
        print(f"\n{GREEN}Branch '{branch_name}' created successfully.{ENDC}")

        # Cambiar automáticamente a la rama o preguntar según el parámetro
        if switch_to_branch:
            print(f"\n{YELLOW}Switching to branch: {branch_name}...{ENDC}")
            subprocess.run(["git", "checkout", branch_name], check=True)
            print(f"\n{GREEN}Switched to branch '{branch_name}' successfully.{ENDC}")
            return True
        else:
            # Preguntar si quiere moverse a la nueva rama
            print(f"\n{YELLOW}Do you want to switch to the new branch '{branch_name}'? (y/n):{ENDC}")
            switch_choice = get_single_keypress().lower()

            if switch_choice == 'y':
                print(f"\n{YELLOW}Switching to branch: {branch_name}...{ENDC}")
                subprocess.run(["git", "checkout", branch_name], check=True)
                print(f"\n{GREEN}Switched to branch '{branch_name}' successfully.{ENDC}")
                return True
            else:
                print(f"\n{YELLOW}Staying on current branch: {current_branch}{ENDC}")
                return True

    except Exception as e:
        print(f"Error creating branch: {e}")
        return False

def create_branch_and_switch(branch_name=None):
    """Crea una nueva rama local y cambia automáticamente a ella"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        if not branch_name:
            print(f"\n{BLUE}Create Branch and Switch:{ENDC}")

            # Obtener las ramas actuales para mostrarlas como referencia
            current_branch = subprocess.run(
                ["git", "--no-pager","branch", "--show-current"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            print(f"\n{YELLOW}Current branch: {current_branch}{ENDC}")

            print(f"\n{BLUE}Existing branches:{ENDC}")
            subprocess.run(["git", "--no-pager", "branch", "--color=always"], check=True)

            # Solicitar el nombre de la nueva rama
            print(f"\n{YELLOW}Enter the name for the new branch (leave empty to cancel):{ENDC}")
            branch_name = input("> ").strip()

            if not branch_name:
                print(f"\n{YELLOW}Operation cancelled.{ENDC}")
                return

        return create_branch_with_name(branch_name, switch_to_branch=True)

    except Exception as e:
        print(f"Error creating and switching to branch: {e}")
        return False

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

                # Try to checkout the branch
                checkout_result = subprocess.run(
                    ["git", "checkout", selected_branch],
                    capture_output=True,
                    text=True
                )

                # Check if checkout was successful
                if checkout_result.returncode != 0:
                    print(f"{YELLOW}Could not switch to branch {selected_branch}: {checkout_result.stderr.strip()}{ENDC}")

                    # Check if the error is due to uncommitted local changes
                    if "local changes" in checkout_result.stderr or "cambios locales" in checkout_result.stderr:
                        # Handle uncommitted changes
                        commit_choice = input(f"\nDo you want to commit your changes before switching branches? (y/n): ").lower()

                        if commit_choice == 'y' or commit_choice == 's':
                            # Commit the changes
                            commit_msg = input(f"\nCommit message: ")

                            # Add all changes
                            add_result = subprocess.run(
                                ["git", "add", "."],
                                capture_output=True,
                                text=True
                            )

                            if add_result.returncode != 0:
                                print(f"{YELLOW}Error adding changes: {add_result.stderr.strip()}{ENDC}")
                                return

                            # Commit
                            commit_result = subprocess.run(
                                ["git", "commit", "-m", commit_msg],
                                capture_output=True,
                                text=True
                            )

                            if commit_result.returncode != 0:
                                print(f"{YELLOW}Error committing changes: {commit_result.stderr.strip()}{ENDC}")
                                return

                            print(f"{GREEN}Commit successful.{ENDC}")

                            # Try to switch to the branch again
                            checkout_result = subprocess.run(
                                ["git", "checkout", selected_branch],
                                capture_output=True,
                                text=True
                            )

                            if checkout_result.returncode != 0:
                                print(f"{YELLOW}Still unable to switch to branch {selected_branch}: {checkout_result.stderr.strip()}{ENDC}")
                                return

                            # Show information about the branch after checkout
                            print(f"{GREEN}Successfully switched to branch {selected_branch}.{ENDC}")

                            # Show additional branch information
                            try:
                                # Last commit on this branch
                                last_commit = subprocess.run(
                                    ["git", "log", "-1", "--oneline"],
                                    capture_output=True,
                                    text=True
                                ).stdout.strip()

                                # Branch tracking info
                                tracking_info = subprocess.run(
                                    ["git", "for-each-ref", "--format='%(upstream:short)'", f"refs/heads/{selected_branch}"],
                                    capture_output=True,
                                    text=True
                                ).stdout.strip().replace("'", "")

                                print(f"{GREEN}Last commit:{ENDC} {last_commit if last_commit else 'No commits yet'}")

                                if tracking_info:
                                    print(f"{GREEN}Tracking:{ENDC} {tracking_info}")
                                else:
                                    print(f"{YELLOW}Not tracking any remote branch{ENDC}")
                            except Exception as e:
                                # If we can't get additional info, just continue
                                pass
                        else:
                            print(f"{YELLOW}Operation canceled. You must commit or stash your changes before switching branches.{ENDC}")
                else:
                    # Show information about the branch after checkout
                    print(f"{GREEN}Successfully switched to branch {selected_branch}.{ENDC}")

                    # Show additional branch information
                    try:
                        # Last commit on this branch
                        last_commit = subprocess.run(
                            ["git", "log", "-1", "--oneline"],
                            capture_output=True,
                            text=True
                        ).stdout.strip()

                        # Branch tracking info
                        tracking_info = subprocess.run(
                            ["git", "for-each-ref", "--format='%(upstream:short)'", f"refs/heads/{selected_branch}"],
                            capture_output=True,
                            text=True
                        ).stdout.strip().replace("'", "")

                        print(f"{GREEN}Last commit:{ENDC} {last_commit if last_commit else 'No commits yet'}")

                        if tracking_info:
                            print(f"{GREEN}Tracking:{ENDC} {tracking_info}")
                        else:
                            print(f"{YELLOW}Not tracking any remote branch{ENDC}")
                    except Exception as e:
                        # If we can't get additional info, just continue
                        pass
            else:
                print("Invalid choice.")
        else:
            print("No local branches found. Create one to proceed.")
    except ValueError:
        print("Please enter a valid number.")
    except Exception as e:
        print(f"Error switching branches: {e}")

def go_to_main():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Try to checkout main branch
        checkout_result = subprocess.run(
            ["git", "checkout", "main"],
            capture_output=True,
            text=True
        )

        # Check if checkout was successful
        if checkout_result.returncode != 0:
            print(f"{YELLOW}Could not switch to main branch: {checkout_result.stderr.strip()}{ENDC}")

            # Check if the error is due to uncommitted local changes
            if "local changes" in checkout_result.stderr or "cambios locales" in checkout_result.stderr:
                # Handle uncommitted changes
                commit_choice = input(f"\nDo you want to commit your changes before switching branches? (y/n): ").lower()

                if commit_choice == 'y' or commit_choice == 's':
                    # Commit the changes
                    commit_msg = input(f"\nCommit message: ")

                    # Add all changes
                    add_result = subprocess.run(
                        ["git", "add", "."],
                        capture_output=True,
                        text=True
                    )

                    if add_result.returncode != 0:
                        print(f"{YELLOW}Error adding changes: {add_result.stderr.strip()}{ENDC}")
                        return

                    # Commit
                    commit_result = subprocess.run(
                        ["git", "commit", "-m", commit_msg],
                        capture_output=True,
                        text=True
                    )

                    if commit_result.returncode != 0:
                        print(f"{YELLOW}Error committing changes: {commit_result.stderr.strip()}{ENDC}")
                        return

                    print(f"{GREEN}Commit successful.{ENDC}")

                    # Try to switch to the branch again
                    checkout_result = subprocess.run(
                        ["git", "checkout", "main"],
                        capture_output=True,
                        text=True
                    )

                    if checkout_result.returncode != 0:
                        print(f"{YELLOW}Still unable to switch to main branch: {checkout_result.stderr.strip()}{ENDC}")
                        return

                    # Show information about the branch after checkout
                    print(f"{GREEN}Successfully switched to main branch.{ENDC}")

                    # Show additional branch information
                    try:
                        # Last commit on this branch
                        last_commit = subprocess.run(
                            ["git", "log", "-1", "--oneline"],
                            capture_output=True,
                            text=True
                        ).stdout.strip()

                        # Branch tracking info
                        tracking_info = subprocess.run(
                            ["git", "for-each-ref", "--format='%(upstream:short)'", "refs/heads/main"],
                            capture_output=True,
                            text=True
                        ).stdout.strip().replace("'", "")

                        print(f"{GREEN}Last commit:{ENDC} {last_commit if last_commit else 'No commits yet'}")

                        if tracking_info:
                            print(f"{GREEN}Tracking:{ENDC} {tracking_info}")
                        else:
                            print(f"{YELLOW}Not tracking any remote branch{ENDC}")
                    except Exception as e:
                        # If we can't get additional info, just continue
                        pass
                else:
                    print(f"{YELLOW}Operation canceled. You must commit or stash your changes before switching branches.{ENDC}")
        else:
            # Show information about the branch after checkout
            print(f"{GREEN}Successfully switched to main branch.{ENDC}")

            # Show additional branch information
            try:
                # Last commit on this branch
                last_commit = subprocess.run(
                    ["git", "log", "-1", "--oneline"],
                    capture_output=True,
                    text=True
                ).stdout.strip()

                # Branch tracking info
                tracking_info = subprocess.run(
                    ["git", "for-each-ref", "--format='%(upstream:short)'", "refs/heads/main"],
                    capture_output=True,
                    text=True
                ).stdout.strip().replace("'", "")

                print(f"{GREEN}Last commit:{ENDC} {last_commit if last_commit else 'No commits yet'}")

                if tracking_info:
                    print(f"{GREEN}Tracking:{ENDC} {tracking_info}")
                else:
                    print(f"{YELLOW}Not tracking any remote branch{ENDC}")
            except Exception as e:
                # If we can't get additional info, just continue
                pass
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

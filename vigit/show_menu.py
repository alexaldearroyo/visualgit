import subprocess
from simple_term_menu import TerminalMenu
from .utils import GREEN, ENDC, BLUE, YELLOW
from .constants import show_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo

def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def general_view():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Get the absolute path of the repository
        repo_path = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Get the repository name (last element of the path)
        repo_name = repo_path.split('/')[-1]


        # Get all local branches
        branches = subprocess.run(
            ["git", "branch", "--color=always"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Get configured remotes
        remotes = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Get all remote branches
        remote_branches = subprocess.run(
            ["git", "branch", "-r", "--color=always"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Get a status summary
        status = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Display the collected information
        print(f"{BLUE}Local Repository:{ENDC}")
        print(f"{YELLOW}Name:{ENDC} {repo_name}")
        print(f"{YELLOW}Path:{ENDC} {repo_path}")

        print(f"\n{BLUE}Local Branches:{ENDC}")
        if branches:
            print(branches)
        else:
            print("No local branches")

        print(f"\n{BLUE}Remote Repository:{ENDC}")
        if remotes:
            print(remotes)
        else:
            print("No remote repositories joined to local repository")

        print(f"\n{BLUE}Remote Branches:{ENDC}")
        if remote_branches:
            print(remote_branches)
        else:
            print("No remote branches available")

        print()

    except Exception as e:
        print(f"Error getting repository information: {e}")

def show_status_long():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Capturar la salida del comando git status
        result = subprocess.run(
            ["git", "status"],
            capture_output=True,
            text=True,
            check=True
        )
        status = result.stdout.strip()

        if status:
            # Usar el comando directamente para preservar colores
            subprocess.run(["git", "status"], check=True)
        else:
            print("Working tree clean")
        print()
    except Exception as e:
        print(f"Error getting status: {e}")

    # Do not show Overall Status or Last Commit after displaying git status

def show_history():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Commit History:{ENDC}\n")
        # Mostrar el historial de commits con formato más detallado
        subprocess.run([
            "git", "log",
            "--pretty=format:%C(yellow)%h %C(blue)%ad%C(auto)%d %C(reset)%s %C(cyan)[%an]",
            "--date=short",
            "--graph",
            "--all"
        ], check=True)
        print()
    except Exception as e:
        print(f"Error retrieving commit history: {e}")

def show_menu_options():
    from .constants import show_menu

    while True:
        print(f"{GREEN}SHOW{ENDC}")
        print(f"\n{BLUE}Overall Status:{ENDC}")
        # Mostrar automáticamente el status antes de mostrar las opciones del menú
        if is_git_repo():
            try:
                # Capturar la salida para verificar si hay cambios
                result = subprocess.run(
                    ["git", "status", "-s"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                status = result.stdout.strip()

                # print(f"\n{GREEN}Status (short format):{ENDC}")
                if status:
                    # Ejecutar directamente para preservar colores
                    subprocess.run(["git", "status", "-s"], check=True)
                else:
                    print("Working tree clean")
                print()
            except Exception as e:
                print(f"Error getting status: {e}")
        else:
            print_not_git_repo()

        last_commit = subprocess.run(
            ["git", "log", "-1", "--pretty=format:%C(yellow)● %h %C(blue)► %C(white)%s %C(magenta)(%cr)", "--color=always"],
            capture_output=True,
            text=True
        ).stdout.strip()

        print(f"{BLUE}Last Commit:{ENDC}")
        if last_commit:
            print(last_commit)

        print()
        menu_options = [
            f"[v] {show_menu.GENERAL_VIEW.value}",
            f"[s] {show_menu.SHOW_STATUS.value}",
            f"[h] {show_menu.SHOW_HISTORY.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            general_view()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            input(f"{GREEN}Press Enter to return to the menu...{ENDC}")
            clear_screen()
            continue
        elif menu_entry_index == 1:
            show_status_long()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            input(f"{GREEN}Press Enter to return to the menu...{ENDC}")
            clear_screen()
            continue
        elif menu_entry_index == 2:
            show_history()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            input(f"{GREEN}Press Enter to return to the menu...{ENDC}")
            clear_screen()
            continue
        elif menu_entry_index == 3:
            clear_screen()
            break
        elif menu_entry_index == 4:
            quit()
        else:
            print("Invalid option. Please try again.")

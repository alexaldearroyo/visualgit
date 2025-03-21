import subprocess
import sys
import os

from simple_term_menu import TerminalMenu
from .utils import BLUE, YELLOW, GREEN, ENDC, DARK_BLUE, ORANGE
from .constants import local_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo
from .show_menu import general_view, show_status_long, show_local_repo, show_branches, get_single_keypress
from .add_menu import add_all_files, add_tracked_files, add_local_branch
from .menu import commit_to_local_repo

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def local_menu_options():
    """Muestra el menú de opciones para operaciones locales"""
    is_repo = is_git_repo()

    while True:
        print(f"{GREEN}LOCAL{ENDC}")

        # Solo mostrar status y último commit si estamos en un repositorio git
        if is_repo:
            print(f"\n{BLUE}Overall Status:{ENDC}")
            try:
                # Capturar la salida para verificar si hay cambios
                result = subprocess.run(
                    ["git", "status", "-s"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                status = result.stdout.strip()

                if status:
                    # Ejecutar directamente para preservar colores
                    subprocess.run(["git", "status", "-s"], check=True)
                else:
                    print("Working tree clean")
            except Exception as e:
                print(f"Error getting status: {e}")

            # Obtener el último commit
            try:
                # Primero verificar si hay commits
                has_commits = subprocess.run(
                    ["git", "rev-parse", "--verify", "HEAD"],
                    capture_output=True,
                    text=True
                ).returncode == 0

                if has_commits:
                    result = subprocess.run(
                        ["git", "log", "-1", "--pretty=format:%C(yellow)● %h %C(blue)► %C(white)%s %C(magenta)(%cr)", "--color=always"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    last_commit = result.stdout.strip()

                    if last_commit:
                        print(f"\n{BLUE}Last Commit:{ENDC}")
                        print(last_commit)
                        print()  # Añadir línea en blanco después del commit
                else:
                    print(f"\n{YELLOW}No commits yet in this repository.{ENDC}")
                    print()  # Añadir línea en blanco
            except Exception as e:
                # No mostrar el error, solo manejar silenciosamente esta situación
                print(f"\n{YELLOW}No commit history available.{ENDC}")
                print()  # Añadir línea en blanco
        else:
            # Mensaje amigable para indicar que no estamos en un repositorio
            print(f"\n{YELLOW}Not in a Git repository. You can create one with 'Add Local Repo'.{ENDC}\n")

        # Opciones de menú diferentes según si estamos en un repo o no
        if is_repo:
            menu_options = [
                f"[v] {local_menu.GENERAL_VIEW.value}",
                f"[s] {local_menu.SHOW_STATUS.value}",
                f"[l] {local_menu.SHOW_LOCAL_REPO.value}",
                f"[b] {local_menu.SHOW_BRANCHES.value}",
                f"[a] {local_menu.ADD_ALL_FILES.value}",
                f"[t] {local_menu.ADD_TRACKED_FILES.value}",
                f"[n] {local_menu.ADD_LOCAL_BRANCH.value}",
                f"[c] {local_menu.COMMIT_LOCAL.value}",
                "[␣] Back to previous menu",
                "[q] Quit program"
            ]
            accept_keys = ("enter", "v", "s", "l", "b", "a", "t", "n", "c", " ", "q")
        else:
            # Solo mostrar mensajes cuando no estamos en un repo
            print(f"{YELLOW}You need to create a local repository first.{ENDC}")
            print(f"{GREEN}Press any key to return to the main menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            return

        # Creamos el menú con las teclas aceptadas adecuadas
        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=accept_keys
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        # Si se presionó la barra espaciadora, volvemos al menú anterior
        if chosen_key == " ":
            clear_screen()
            return

        # Procesamos la selección del menú
        if menu_entry_index == 0 or chosen_key == "v":
            general_view()
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "s":
            show_status_long()
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "l":
            show_local_repo()
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "b":
            show_branches()
            clear_screen()
            continue
        elif menu_entry_index == 4 or chosen_key == "a":
            add_all_files()
            clear_screen()
            continue
        elif menu_entry_index == 5 or chosen_key == "t":
            add_tracked_files()
            clear_screen()
            continue
        elif menu_entry_index == 6 or chosen_key == "n":
            add_local_branch()
            clear_screen()
            continue
        elif menu_entry_index == 7 or chosen_key == "c":
            commit_to_local_repo()
            clear_screen()
            continue
        elif menu_entry_index == 8:
            clear_screen()
            return
        elif menu_entry_index == 9 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

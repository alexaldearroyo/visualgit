import subprocess
import sys
import termios
import tty

from simple_term_menu import TerminalMenu
from .utils import GREEN, ENDC, BLUE, RED, YELLOW
from .constants import add_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo

def get_single_keypress():
    """Captura un solo carácter del usuario sin necesidad de presionar Enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)  # Lee un solo carácter
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def clear_screen():
    """Clear the terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def add_tracked_files(ask_for_enter=True):
    """Añade archivos al índice de Git (git add)"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Add Tracked Files:{ENDC}")

        # Obtener archivos no rastreados
        untracked_files = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip().split('\n')

        # Obtener archivos modificados
        modified_files = subprocess.run(
            ["git", "ls-files", "--modified"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip().split('\n')

        # Combinar y filtrar archivos vacíos
        files_to_add = [f for f in untracked_files + modified_files if f]

        if not files_to_add:
            print(f"\n{YELLOW}No files to add. Working tree clean.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Mostrar lista de archivos para añadir
        print(f"\n{YELLOW}Select files to add (space to select, enter to confirm):{ENDC}")

        # Preparar opciones de menú con archivos y opciones adicionales
        menu_options = files_to_add + ["[Add all files]", "[Cancel]"]

        terminal_menu = TerminalMenu(
            menu_options,
            title="",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            multi_select=True,
            show_multi_select_hint=True,
            clear_screen=False
        )

        selected_indices = terminal_menu.show()

        # Si no se seleccionó nada o se seleccionó Cancelar
        if not selected_indices or (len(selected_indices) == 1 and selected_indices[0] == len(menu_options) - 1):
            print(f"\n{YELLOW}Operation cancelled.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Si se seleccionó "Add all files"
        if len(selected_indices) == 1 and selected_indices[0] == len(menu_options) - 2:
            print(f"\n{YELLOW}Adding all files...{ENDC}")
            subprocess.run(["git", "add", "."], check=True)
            print(f"\n{GREEN}All files have been added successfully.{ENDC}")
        else:
            # Filtrar las opciones que no son archivos (Add all, Cancel)
            selected_files = [menu_options[idx] for idx in selected_indices if idx < len(files_to_add)]

            if selected_files:
                print(f"\n{YELLOW}Adding selected files...{ENDC}")
                for file in selected_files:
                    print(f"  Adding: {file}")
                    subprocess.run(["git", "add", file], check=True)
                print(f"\n{GREEN}Selected file(s) have been added successfully.{ENDC}")
            else:
                print(f"\n{YELLOW}No files were selected.{ENDC}")

        # Solo mostrar mensaje y esperar tecla si se solicita explícitamente
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
        # Si no, simplemente retornar para volver al menú
    except Exception as e:
        print(f"Error adding files: {e}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def add_all_files(ask_for_enter=True):
    """Añade todos los archivos al índice de Git (git add .)"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Add All Files:{ENDC}")

        # Verificar si hay archivos para añadir
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        modified = subprocess.run(
            ["git", "ls-files", "--modified"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        if not untracked and not modified:
            print(f"\n{YELLOW}No files to add. Working tree clean.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Añadir todos los archivos sin preguntar
        print(f"\n{YELLOW}Adding all files...{ENDC}")
        subprocess.run(["git", "add", "."], check=True)
        print(f"\n{GREEN}All files have been added successfully.{ENDC}")

        # Solo mostrar mensaje y esperar tecla si se solicita explícitamente
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
        # Si no, simplemente retornar para volver al menú
    except Exception as e:
        print(f"Error adding files: {e}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def add_menu_options():
    """Muestra el menú de opciones para añadir archivos"""
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        print(f"{GREEN}ADD{ENDC}")

        # Mostrar archivos no rastreados
        print(f"\n{RED}Untracked files:{ENDC}")
        try:
            untracked = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            if untracked:
                print(untracked)
            else:
                print("No untracked files")
        except Exception as e:
            print(f"Error getting untracked files: {e}")

        # Mostrar archivos modificados
        print(f"\n{BLUE}Modified files:{ENDC}")
        try:
            modified = subprocess.run(
                ["git", "ls-files", "--modified"],
                capture_output=True,
                text=True,
                check=True
            ).stdout.strip()

            if modified:
                print(modified)
            else:
                print("No modified files")
        except Exception as e:
            print(f"Error getting modified files: {e}")

        menu_options = [
            f"[a] {add_menu.ADD_ALL_FILES.value}",
            f"[t] {add_menu.ADD_TRACKED_FILES.value}",
            "[k] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"\nPlease select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "a", "t", "k", "q")
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            add_all_files(ask_for_enter=True)
            clear_screen()
            continue
        elif menu_entry_index == 1:
            add_tracked_files(ask_for_enter=True)
            clear_screen()
            continue
        elif menu_entry_index == 2:
            clear_screen()
            return
        elif menu_entry_index == 3:
            quit()
        else:
            print("Invalid option. Please try again.")

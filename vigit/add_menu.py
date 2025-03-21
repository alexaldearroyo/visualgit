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

def add_expanded_files(ask_for_enter=True):
    """Añade todos los archivos, incluidos los no rastreados, al índice de Git (git add --all)"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Add Expanded Files:{ENDC}")

        # Ejecutar git add --all
        print(f"\n{YELLOW}Adding all files, including untracked files...{ENDC}")
        subprocess.run(["git", "add", "--all"], check=True)
        print(f"\n{GREEN}All files have been added successfully.{ENDC}")

        # Mostrar qué archivos se han añadido
        print(f"\n{BLUE}Added files:{ENDC}")
        subprocess.run(["git", "status", "-s"], check=True)

        # Solo mostrar mensaje y esperar tecla si se solicita explícitamente
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error adding files: {e}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def add_local_branch(ask_for_enter=False):
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
            return

        # Crear la nueva rama
        print(f"\n{YELLOW}Creating new branch: {branch_name}...{ENDC}")
        subprocess.run(["git", "branch", branch_name], check=True)
        print(f"\n{GREEN}Branch '{branch_name}' created successfully.{ENDC}")

        # Preguntar si quiere moverse a la nueva rama
        print(f"\n{YELLOW}Do you want to switch to the new branch '{branch_name}'? (y/n):{ENDC}")
        switch_choice = get_single_keypress().lower()

        if switch_choice == 'y':
            print(f"\n{YELLOW}Switching to branch: {branch_name}...{ENDC}")
            subprocess.run(["git", "checkout", branch_name], check=True)
            print(f"\n{GREEN}Switched to branch '{branch_name}' successfully.{ENDC}")
        else:
            print(f"\n{YELLOW}Staying on current branch: {current_branch}{ENDC}")

    except Exception as e:
        print(f"Error creating branch: {e}")

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

                if status:
                    # Ejecutar directamente para preservar colores
                    subprocess.run(["git", "status", "-s"], check=True)
                else:
                    print("Working tree clean")
            except Exception as e:
                print(f"Error getting status: {e}")

        # Obtener el último commit si es un repositorio git
        if is_git_repo():
            try:
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
            except Exception as e:
                print(f"Error getting last commit: {e}")

        menu_options = [
            f"[a] {add_menu.ADD_ALL_FILES.value}",
            f"[t] {add_menu.ADD_TRACKED_FILES.value}",
            f"[x] {add_menu.ADD_EXPANDED_FILES.value}",
            f"[b] {add_menu.ADD_LOCAL_BRANCH.value}",
            "[␣] Back to previous menu",
            "[q] Quit program"
        ]

        # Creamos el menú con la barra espaciadora como tecla aceptada
        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "a", "t", "x", "b", " ", "q")
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        # Si se presionó la barra espaciadora, volvemos al menú anterior
        if chosen_key == " ":
            clear_screen()
            return

        # Procesamos la selección normal del menú
        if menu_entry_index == 0 or chosen_key == "a":
            add_all_files(ask_for_enter=True)
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "t":
            add_tracked_files(ask_for_enter=True)
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "x":
            add_expanded_files(ask_for_enter=True)
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "b":
            add_local_branch()
            clear_screen()
            continue
        elif menu_entry_index == 4:
            clear_screen()
            return
        elif menu_entry_index == 5 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

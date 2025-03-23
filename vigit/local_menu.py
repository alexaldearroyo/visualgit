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
                "[c] Commits ►",
                "[␣] Back to previous menu",
                "[q] Quit program"
            ]
            accept_keys = ("enter", "c", " ", "q")
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
        if menu_entry_index == 0 or chosen_key == "c":
            # clear_screen()
            commits_submenu()
            # clear_screen()
            continue
        elif menu_entry_index == 1:
            clear_screen()
            return
        elif menu_entry_index == 2 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

def commits_submenu():
    """Muestra el submenú de opciones para commits"""
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        # clear_screen()
        print(f"{GREEN}COMMITS{ENDC}")

        menu_options = [
            "[c] Commit All changes",
            "[t] Commit Tracked Changes",
            "[a] Commit All Changes of Tracked Files",
            "[e] Edit Last Commit",
            "[0] Commit with empty changes",
            "[g] Go to commit",
            "[␣] Back to previous menu",
            "[q] Quit program"
        ]
        accept_keys = ("enter", "c", "t", "a", "e", "0", "g", " ", "q")

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=accept_keys
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        if chosen_key == " ":
            clear_screen()
            return

        if menu_entry_index == 0 or chosen_key == "c":
            commit_all_changes()
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "t":
            commit_tracked_changes()
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "a":
            commit_tracked_files()
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "e":
            edit_last_commit()
            clear_screen()
            continue
        elif menu_entry_index == 4 or chosen_key == "0":
            commit_empty()
            clear_screen()
            continue
        elif menu_entry_index == 5 or chosen_key == "g":
            go_to_commit()
            clear_screen()
            continue
        elif menu_entry_index == 6:
            clear_screen()
            return
        elif menu_entry_index == 7 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

def commit_all_changes():
    """Ejecuta 'git add .' y realiza un commit con el mensaje proporcionado por el usuario"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}COMMIT ALL CHANGES{ENDC}")

    try:
        # Ejecutar git add .
        subprocess.run(["git", "add", "."], check=True)

        # Mostrar los archivos que se van a hacer commit
        print(f"\n{BLUE}Files staged for commit:{ENDC}")
        subprocess.run(["git", "status", "-s"], check=True)

        # Solicitar mensaje de commit
        print(f"\n{YELLOW}Enter commit message (<enter> to cancel):{ENDC}")
        commit_msg = input("> ")

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_msg:
            print(f"\n{YELLOW}Commit cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el commit
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        print(f"\n{GREEN}Changes committed successfully!{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during commit process: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

def commit_tracked_changes():
    """Permite seleccionar archivos específicos para añadir y realizar un commit"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}COMMIT TRACKED CHANGES{ENDC}")

    try:
        # Obtener lista de archivos con cambios
        result = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True
        )

        # Procesar la salida para obtener nombres de archivos
        changed_files = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                # Extraer el nombre del archivo (después del espacio)
                status = line[:2].strip()
                file_name = line[3:].strip()
                changed_files.append((status, file_name))

        if not changed_files:
            print(f"\n{YELLOW}No changes detected in the repository.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Crear menú de selección múltiple
        print(f"\n{BLUE}Select files to commit (use space to toggle selection, enter to confirm):{ENDC}\n")

        menu_entries = []
        for status, file_name in changed_files:
            # Formatear el estado con colores
            status_colored = status
            if 'M' in status:
                status_display = f"{YELLOW}M{ENDC}"
            elif 'A' in status:
                status_display = f"{GREEN}A{ENDC}"
            elif 'D' in status:
                status_display = f"{ORANGE}D{ENDC}"
            elif '?' in status:
                status_display = f"{BLUE}?{ENDC}"
            else:
                status_display = status

            menu_entries.append(f"{status_display} {file_name}")

        terminal_menu = TerminalMenu(
            menu_entries,
            title="Files with changes:",
            multi_select=True,
            show_multi_select_hint=True,
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )

        selected_indices = terminal_menu.show()

        # Si no hay selección, volver al menú
        if selected_indices is None or len(selected_indices) == 0:
            print(f"\n{YELLOW}No files selected. Operation cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Añadir los archivos seleccionados
        selected_files = [changed_files[idx][1] for idx in selected_indices]

        print(f"\n{BLUE}Adding selected files:{ENDC}")
        for file in selected_files:
            print(f" - {file}")
            subprocess.run(["git", "add", file], check=True)

        # Mostrar los archivos que se van a hacer commit
        print(f"\n{BLUE}Files staged for commit:{ENDC}")
        subprocess.run(["git", "status", "-s"], check=True)

        # Solicitar mensaje de commit
        print(f"\n{YELLOW}Enter commit message (<enter> to cancel):{ENDC}")
        commit_msg = input("> ")

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_msg:
            print(f"\n{YELLOW}Commit cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el commit
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        print(f"\n{GREEN}Changes committed successfully!{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during commit process: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

def commit_tracked_files():
    """Ejecuta 'git commit -a' para hacer commit de todos los archivos tracked modificados"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}COMMIT ALL CHANGES OF TRACKED FILES{ENDC}")

    try:
        # Mostrar los archivos modificados que están siendo rastreados
        print(f"\n{BLUE}Tracked files with changes:{ENDC}")
        subprocess.run(["git", "diff", "--name-status"], check=True)

        # Solicitar mensaje de commit
        print(f"\n{YELLOW}Enter commit message (<enter> to cancel):{ENDC}")
        commit_msg = input("> ")

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_msg:
            print(f"\n{YELLOW}Commit cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el commit con la opción -a
        subprocess.run(["git", "commit", "-a", "-m", commit_msg], check=True)

        print(f"\n{GREEN}Changes committed successfully!{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during commit process: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

def edit_last_commit():
    """Ejecuta 'git commit --amend' para editar el último commit"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}EDIT LAST COMMIT{ENDC}")

    try:
        # Verificar si hay commits para enmendar
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"\n{YELLOW}No commits yet in this repository. Cannot amend.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Mostrar el último commit que se va a editar
        print(f"\n{BLUE}Current Last Commit:{ENDC}")
        subprocess.run(
            ["git", "log", "-1", "--pretty=format:%h - %s (%cr)", "--abbrev-commit"],
            check=True
        )
        print()

        # Solicitar el nuevo mensaje de commit
        print(f"\n{YELLOW}Enter new commit message (<enter> to cancel):{ENDC}")
        commit_msg = input("> ")

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_msg:
            print(f"\n{YELLOW}Amendment cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el commit con la opción --amend
        subprocess.run(["git", "commit", "--amend", "-m", commit_msg], check=True)

        print(f"\n{GREEN}Last commit amended successfully!{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during commit amendment: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

def commit_empty():
    """Ejecuta 'git commit --allow-empty' para hacer un commit sin cambios"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}COMMIT WITH EMPTY CHANGES{ENDC}")

    try:
        # Solicitar mensaje de commit
        print(f"\n{YELLOW}Enter commit message (<enter> to cancel):{ENDC}")
        commit_msg = input("> ")

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_msg:
            print(f"\n{YELLOW}Commit cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el commit con la opción --allow-empty
        subprocess.run(["git", "commit", "--allow-empty", "-m", commit_msg], check=True)

        print(f"\n{GREEN}Empty commit created successfully!{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during empty commit: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

def go_to_commit():
    """Ejecuta 'git checkout <commit>' para ir a un commit específico"""
    if not is_git_repo():
        print_not_git_repo()
        return

    clear_screen()
    print(f"{GREEN}GO TO COMMIT{ENDC}")

    try:
        # Verificar si hay commits
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"\n{YELLOW}No commits yet in this repository.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Mostrar algunos commits recientes para referencia
        print(f"\n{BLUE}Recent commits (for reference):{ENDC}")
        subprocess.run(
            ["git", "log", "--oneline", "--max-count=5"],
            check=True
        )
        print()

        # Solicitar hash del commit
        print(f"\n{YELLOW}Enter commit hash (<enter> to cancel):{ENDC}")
        commit_hash = input("> ").strip()

        # Si el usuario presiona Enter sin escribir nada, cancelar
        if not commit_hash:
            print(f"\n{YELLOW}Operation cancelled.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Verificar si el commit existe
        commit_exists = subprocess.run(
            ["git", "cat-file", "-e", f"{commit_hash}^{{commit}}"],
            capture_output=True
        ).returncode == 0

        if not commit_exists:
            print(f"\n{YELLOW}Commit {commit_hash} not found.{ENDC}")
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            return

        # Realizar el checkout al commit
        result = subprocess.run(
            ["git", "checkout", commit_hash],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"\n{GREEN}Successfully checked out commit {commit_hash}{ENDC}")

            # Verificar si estamos en un estado detached HEAD
            is_detached = subprocess.run(
                ["git", "symbolic-ref", "-q", "HEAD"],
                capture_output=True
            ).returncode != 0

            if is_detached:
                print(f"\n{YELLOW}You are not in any branch (detached HEAD state){ENDC}")
                print(f"\n{BLUE}What you can do now:{ENDC}")
                print(f"- {GREEN}Branches > Go to branch{ENDC} to checkout without saving changes")
                print(f"- {GREEN}Add > Branch{ENDC} to checkout in a new branch with saved changes")
        else:
            print(f"\n{YELLOW}Error checking out commit: {result.stderr.strip()}{ENDC}")

        print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()
    except Exception as e:
        print(f"\n{YELLOW}Error during checkout: {e}{ENDC}")
        print(f"{GREEN}Press any key to return to the menu...{ENDC}")
        get_single_keypress()

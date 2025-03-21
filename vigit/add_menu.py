import subprocess
import sys
import termios
import tty

from simple_term_menu import TerminalMenu
from .utils import GREEN, ENDC, BLUE, RED, YELLOW
from .constants import add_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo
from .github_ops import create_github_repository, get_github_token, get_github_username

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

def add_local_repo(ask_for_enter=True):
    """Inicializa un nuevo repositorio Git (git init)"""
    try:
        print(f"\n{BLUE}Add Local Repo:{ENDC}")

        # Verificar si ya estamos en un repositorio git
        is_already_repo = False
        try:
            subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                check=True
            )
            is_already_repo = True
            print(f"\n{YELLOW}This directory is already a Git repository.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return
        except:
            # No es un repositorio git, podemos continuar
            pass

        print(f"\n{YELLOW}Initializing new Git repository in the current directory...{ENDC}")
        subprocess.run(["git", "init"], check=True)
        print(f"\n{GREEN}Git repository initialized successfully.{ENDC}")

        # Verificar si hay archivos que podrían ser añadidos
        status = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.strip()

        if status:
            print(f"\n{BLUE}Files that can be added to the repository:{ENDC}")
            subprocess.run(["git", "status", "-s"], check=True)

            # Preguntar si quiere añadir todos los archivos
            print(f"\n{YELLOW}Do you want to add all files to the repository? (y/n):{ENDC}")
            add_all_choice = get_single_keypress().lower()

            if add_all_choice == 'y':
                print(f"\n{YELLOW}Adding all files...{ENDC}")
                subprocess.run(["git", "add", "."], check=True)
                print(f"\n{GREEN}All files have been added successfully.{ENDC}")

                # Preguntar si quiere hacer el commit inicial
                print(f"\n{YELLOW}Do you want to make an initial commit? (y/n):{ENDC}")
                commit_choice = get_single_keypress().lower()

                if commit_choice == 'y':
                    print(f"\n{YELLOW}Enter a commit message (leave empty for default 'Initial commit'):{ENDC}")
                    commit_message = input("> ").strip()

                    if not commit_message:
                        commit_message = "Initial commit"

                    print(f"\n{YELLOW}Creating initial commit...{ENDC}")
                    subprocess.run(["git", "commit", "-m", commit_message], check=True)
                    print(f"\n{GREEN}Initial commit created successfully.{ENDC}")
        else:
            print(f"\n{YELLOW}No files found in the directory to add to the repository.{ENDC}")

        # Mostrar mensaje final y esperar que el usuario presione una tecla
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

    except Exception as e:
        print(f"Error initializing repository: {e}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def add_empty_repo(ask_for_enter=True):
    """Inicializa un nuevo repositorio Git bare (vacío) con git init --bare"""
    try:
        print(f"\n{BLUE}Add Empty Repo:{ENDC}")

        # Solicitar nombre para el repositorio
        print(f"\n{YELLOW}Enter the name for the empty repository (leave empty to cancel):{ENDC}")
        repo_name = input("> ").strip()

        if not repo_name:
            print(f"\n{YELLOW}Operation cancelled.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Añadir la extensión .git si no la tiene
        if not repo_name.endswith('.git'):
            repo_name = f"{repo_name}.git"

        # Verificar si el directorio ya existe
        import os
        if os.path.exists(repo_name):
            print(f"\n{RED}A directory with the name '{repo_name}' already exists.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Crear el repositorio bare
        print(f"\n{YELLOW}Initializing new bare Git repository in '{repo_name}'...{ENDC}")
        subprocess.run(["git", "init", "--bare", repo_name], check=True)
        print(f"\n{GREEN}Empty Git repository initialized successfully in '{repo_name}'.{ENDC}")

        # Mostrar mensaje final y esperar que el usuario presione una tecla
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

    except Exception as e:
        print(f"Error initializing empty repository: {e}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def add_remote_repo(ask_for_enter=True):
    """Crea un nuevo repositorio remoto en GitHub"""
    try:
        print(f"\n{BLUE}Add Remote Repo:{ENDC}")

        # Verificar si tenemos token de GitHub
        token = get_github_token()
        if not token:
            print(f"\n{YELLOW}GitHub token not found. Please configure one in the configuration menu.{ENDC}")
            print(f"{YELLOW}Go to: Configuration > GitHub API Configuration{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Obtener nombre de usuario de GitHub
        username = get_github_username()
        if username:
            print(f"\n{BLUE}GitHub User:{ENDC} {username}")

        # Solicitar nombre para el repositorio
        print(f"\n{YELLOW}Enter the name for the remote repository (leave empty to cancel):{ENDC}")
        repo_name = input("> ").strip()

        if not repo_name:
            print(f"\n{YELLOW}Operation cancelled.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Solicitar descripción (opcional)
        print(f"\n{YELLOW}Enter a description for the repository (optional):{ENDC}")
        description = input("> ").strip()

        # Preguntar si el repositorio debe ser privado
        print(f"\n{YELLOW}Make the repository private? (y/n):{ENDC}")
        private_choice = get_single_keypress().lower()
        private = private_choice == 'y'

        print(f"\n{YELLOW}Creating remote repository '{repo_name}' on GitHub...{ENDC}")
        repo_url = create_github_repository(repo_name, description, private)

        if repo_url:
            print(f"\n{GREEN}Remote repository created successfully.{ENDC}")
            print(f"{GREEN}Repository URL: {repo_url}{ENDC}")

            # Si estamos en un repositorio local, preguntar si quiere conectarlo
            if is_git_repo():
                print(f"\n{YELLOW}Do you want to connect your local repository to this remote? (y/n):{ENDC}")
                connect_choice = get_single_keypress().lower()

                if connect_choice == 'y':
                    print(f"\n{YELLOW}Connecting to remote repository...{ENDC}")
                    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
                    print(f"\n{GREEN}Remote repository connected successfully.{ENDC}")

                    # Preguntar si quiere hacer push
                    print(f"\n{YELLOW}Do you want to push your current branch to the remote? (y/n):{ENDC}")
                    push_choice = get_single_keypress().lower()

                    if push_choice == 'y':
                        current_branch = subprocess.run(
                            ["git", "branch", "--show-current"],
                            capture_output=True,
                            text=True,
                            check=True
                        ).stdout.strip()

                        print(f"\n{YELLOW}Pushing to remote repository...{ENDC}")
                        subprocess.run(["git", "push", "-u", "origin", current_branch], check=True)
                        print(f"\n{GREEN}Successfully pushed to remote repository.{ENDC}")

        # Mostrar mensaje final y esperar que el usuario presione una tecla
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

    except Exception as e:
        print(f"Error creating remote repository: {e}")
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
    is_repo = is_git_repo()

    while True:
        print(f"{GREEN}ADD{ENDC}")

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
        else:
            # Mensaje amigable para indicar que no estamos en un repositorio
            print(f"\n{YELLOW}Not in a Git repository. You can create one with 'Add Local Repo'.{ENDC}\n")

        # Opciones de menú diferentes según si estamos en un repo o no
        if is_repo:
            menu_options = [
                f"[a] {add_menu.ADD_ALL_FILES.value}",
                f"[t] {add_menu.ADD_TRACKED_FILES.value}",
                f"[x] {add_menu.ADD_EXPANDED_FILES.value}",
                f"[b] {add_menu.ADD_LOCAL_BRANCH.value}",
                f"[l] {add_menu.ADD_LOCAL_REPO.value}",
                f"[r] {add_menu.ADD_REMOTE_REPO.value}",
                f"[0] {add_menu.ADD_EMPTY_REPO.value}",
                "[␣] Back to previous menu",
                "[q] Quit program"
            ]
            accept_keys = ("enter", "a", "t", "x", "b", "l", "r", "0", " ", "q")
        else:
            # Solo mostrar la opción para crear un repo y salir cuando no estamos en un repo
            menu_options = [
                f"[l] {add_menu.ADD_LOCAL_REPO.value}",
                f"[r] {add_menu.ADD_REMOTE_REPO.value}",
                f"[0] {add_menu.ADD_EMPTY_REPO.value}",
                "[␣] Back to previous menu",
                "[q] Quit program"
            ]
            accept_keys = ("enter", "l", "r", "0", " ", "q")

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

        # Procesamos la selección según si estamos en un repo o no
        if is_repo:
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
            elif menu_entry_index == 4 or chosen_key == "l":
                add_local_repo(ask_for_enter=True)
                clear_screen()
                # Verificar si ahora estamos en un repo después de crear uno
                is_repo = is_git_repo()
                continue
            elif menu_entry_index == 5 or chosen_key == "r":
                add_remote_repo(ask_for_enter=True)
                clear_screen()
                continue
            elif menu_entry_index == 6 or chosen_key == "0":
                add_empty_repo(ask_for_enter=True)
                clear_screen()
                continue
            elif menu_entry_index == 7:
                clear_screen()
                return
            elif menu_entry_index == 8 or chosen_key == "q":
                quit()
            else:
                print("Invalid option. Please try again.")
        else:
            if menu_entry_index == 0 or chosen_key == "l":
                add_local_repo(ask_for_enter=True)
                clear_screen()
                # Verificar si ahora estamos en un repo después de crear uno
                is_repo = is_git_repo()
                continue
            elif menu_entry_index == 1 or chosen_key == "r":
                add_remote_repo(ask_for_enter=True)
                clear_screen()
                continue
            elif menu_entry_index == 2 or chosen_key == "0":
                add_empty_repo(ask_for_enter=True)
                clear_screen()
                continue
            elif menu_entry_index == 3:
                clear_screen()
                return
            elif menu_entry_index == 4 or chosen_key == "q":
                quit()
            else:
                print("Invalid option. Please try again.")

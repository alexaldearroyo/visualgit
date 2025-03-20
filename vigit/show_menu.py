import subprocess
import sys
import termios
import tty

from simple_term_menu import TerminalMenu
from .utils import GREEN, ENDC, BLUE, YELLOW
from .constants import show_menu, MENU_CURSOR, MENU_CURSOR_STYLE, history_menu, differences_menu
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

def show_tracking_history(ask_for_enter=True):
    """Muestra un historial de commits con estadísticas de archivos modificados"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Tracking History with Statistics:{ENDC}\n")
        # Mostrar el historial de commits con estadísticas de archivos modificados
        subprocess.run([
            "git", "log",
            "--graph",
            "--stat",
            "--pretty=format:%C(yellow)%h%Creset%C(auto)%d%Creset %C(blue)|%Creset %C(cyan)%an%Creset %C(blue)| %Creset%C(magenta)%ar%Creset%n%n%C(blue)► %C(white)%s%Creset%n",
            "--decorate=short",
            "--date=relative"
        ], check=True)
        print()
    except Exception as e:
        print(f"Error retrieving tracking history: {e}")

def show_history():
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        print(f"{GREEN}SHOW | HISTORY{ENDC}")

        menu_options = [
            f"[h] {history_menu.DETAILED_HISTORY.value}",
            f"[x] {history_menu.EXPANDED_HISTORY.value}",
            f"[t] {history_menu.TRACKING_HISTORY.value}",
            f"[d] {history_menu.DIFFERENCES_HISTORY.value}",
            "[k] Back to previous menu",
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
            show_detailed_history()
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 1:
            show_expanded_history()
            clear_screen()
            continue
        elif menu_entry_index == 2:
            show_tracking_history()
            clear_screen()
            continue
        elif menu_entry_index == 3:
            show_differences_history()
            clear_screen()
            continue
        elif menu_entry_index == 4:
            clear_screen()
            return
        elif menu_entry_index == 5:
            quit()
        else:
            print("Invalid option. Please try again.")

def show_expanded_history(ask_for_enter=True):
    """Muestra un historial gráfico expandido de commits"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Expanded Commit History:{ENDC}\n")
        # Mostrar el historial de commits con formato gráfico expandido
        subprocess.run([
            "git", "log",
            "--graph",
            "--all",
            "--pretty=format:%C(yellow)%h%Creset%C(auto)%d%Creset %C(cyan)%an%Creset %C(magenta)%ar%Creset%n  %C(white)%s%Creset",
            "--decorate=short",
            "--date=relative"
        ], check=True)
        print()
    except Exception as e:
        print(f"Error retrieving expanded commit history: {e}")

def show_detailed_history(ask_for_enter=True):
    """Muestra un historial detallado de commits en orden cronológico"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Detailed Commit History:{ENDC}\n")
        # Mostrar el historial de commits con el formato específico
        subprocess.run([
            "git", "--no-pager", "log",
            "--reverse",
            "--pretty=format:%C(yellow)● %h%Creset%C(auto)%d%Creset%C(blue) ► %C(white)%s%Creset %C(blue)| %C(cyan)%an%Creset %C(blue)| %C(magenta)%ad%Creset",
            "--decorate=short",
            "--date=format:%Y-%m-%d %H:%M",
            "--date=relative"
        ], check=True)
        print("\n")
    except Exception as e:
        print(f"Error retrieving detailed commit history: {e}")

def show_differences_history(ask_for_enter=True):
    """Muestra un historial detallado de commits con diferencias y estadísticas"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences Commit History:{ENDC}\n")
        # Comando completo usando subprocess.run con shell=True para mantener el pipeline
        subprocess.run(
            "git log --color=always --stat -p --pretty=format:\"%C(white)$(printf '%.0s-' {1..30})%Creset%n%C(yellow)● %h%Creset%C(auto)%d%Creset%n%C(blue)► %C(white)%s%Creset %C(blue)| %C(cyan)%an%Creset %C(blue)| %C(magenta)%ad%Creset\" --date=format:'%Y-%m-%d %H:%M%n' | diff-so-fancy | less -R",
            shell=True,
            check=True
        )
        print("\n")
    except Exception as e:
        print(f"Error retrieving differences commit history: {e}")

def show_differences_non_staged(ask_for_enter=True):
    """Muestra las diferencias de los archivos no staged"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences of non staged files:{ENDC}\n")
        # Ejecutar el comando git diff con diff-so-fancy
        subprocess.run(
            "git diff | diff-so-fancy",
            shell=True,
            check=True
        )
        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving differences: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_staged(ask_for_enter=True):
    """Muestra las diferencias de los archivos staged (añadidos)"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences of Added files:{ENDC}\n")
        # Ejecutar el comando git diff --staged con diff-so-fancy
        subprocess.run(
            "git diff --staged | diff-so-fancy",
            shell=True,
            check=True
        )
        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving staged differences: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_committed(ask_for_enter=True):
    """Muestra las diferencias del directorio de trabajo respecto al último commit (HEAD)"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences with HEAD:{ENDC}\n")
        # Ejecutar el comando git diff HEAD con diff-so-fancy
        subprocess.run(
            "git diff HEAD | diff-so-fancy",
            shell=True,
            check=True
        )
        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving HEAD differences: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_between_commits(ask_for_enter=True):
    """Muestra las diferencias entre dos commits"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Obtener la lista de commits recientes para elegir
        print(f"\n{BLUE}Select commits to compare differences:{ENDC}\n")

        # Mostrar los commits recientes para referencia
        print(f"{YELLOW}Recent commits:{ENDC}")
        subprocess.run(
            ["git", "--no-pager", "log", "--oneline", "--max-count=10"],
            check=True
        )
        print()

        # Solicitar el commit base (más antiguo)
        print(f"{YELLOW}Enter base commit hash (older):{ENDC} ", end="")
        base_commit = input().strip()

        # Solicitar el commit de comparación (más reciente)
        print(f"{YELLOW}Enter comparison commit hash (newer or HEAD):{ENDC} ", end="")
        compare_commit = input().strip()

        if not base_commit or not compare_commit:
            print("Error: You need to provide both commit hashes.")
            return

        print(f"\n{BLUE}Differences between commits {base_commit} and {compare_commit}:{ENDC}\n")

        # Ejecutar el comando para mostrar las diferencias entre los dos commits
        subprocess.run(
            f"git diff {base_commit}..{compare_commit} | diff-so-fancy",
            shell=True,
            check=True
        )

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving commit differences: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_between_branches(ask_for_enter=True):
    """Muestra las diferencias entre dos ramas"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Obtener la lista de ramas para elegir
        print(f"\n{BLUE}Select branches to compare differences:{ENDC}\n")

        # Mostrar todas las ramas (locales y remotas) para referencia
        print(f"{YELLOW}Local branches:{ENDC}")
        subprocess.run(
            ["git", "--no-pager", "branch"],
            check=True
        )
        print()

        print(f"{YELLOW}Remote branches:{ENDC}")
        subprocess.run(
            ["git", "--no-pager", "branch", "-r"],
            check=True
        )
        print()

        # Solicitar la primera rama
        print(f"{YELLOW}Enter first branch name:{ENDC} ", end="")
        first_branch = input().strip()

        # Solicitar la segunda rama
        print(f"{YELLOW}Enter second branch name:{ENDC} ", end="")
        second_branch = input().strip()

        if not first_branch or not second_branch:
            print("Error: You need to provide both branch names.")
            return

        print(f"\n{BLUE}Differences between branches {first_branch} and {second_branch}:{ENDC}\n")

        # Ejecutar el comando para mostrar las diferencias entre las dos ramas
        subprocess.run(
            f"git diff {first_branch}..{second_branch} | diff-so-fancy",
            shell=True,
            check=True
        )

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving branch differences: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_local_repo(ask_for_enter=True):
    """Muestra información básica del repositorio local"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Local Repository Information:{ENDC}")

        # Obtener la ruta absoluta del repositorio
        repo_path = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener el nombre del repositorio (último elemento de la ruta)
        repo_name = repo_path.split('/')[-1]

        # Obtener la rama actual
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Mostrar solo la información básica
        print(f"{YELLOW}Repository Name:{ENDC} {repo_name}")
        print(f"{YELLOW}Repository Path:{ENDC} {repo_path}")
        print(f"{YELLOW}Current Branch:{ENDC} {current_branch}")

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving repository information: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences():
    """Muestra el submenú de diferencias"""
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        print(f"{GREEN}SHOW | DIFFERENCES{ENDC}")

        menu_options = [
            f"[d] {differences_menu.NON_STAGED_DIFFERENCES.value}",
            f"[a] {differences_menu.STAGED_DIFFERENCES.value}",
            f"[c] {differences_menu.COMMIT_TO_COMMIT_DIFFERENCES.value}",
            f"[b] {differences_menu.BRANCH_TO_BRANCH_DIFFERENCES.value}",
            "[k] Back to previous menu",
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
            show_differences_non_staged()
            clear_screen()
            continue
        elif menu_entry_index == 1:
            show_differences_staged()
            clear_screen()
            continue
        elif menu_entry_index == 2:
            show_differences_between_commits()
            clear_screen()
            continue
        elif menu_entry_index == 3:
            show_differences_between_branches()
            clear_screen()
            continue
        elif menu_entry_index == 4:
            clear_screen()
            return
        elif menu_entry_index == 5:
            quit()
        else:
            print("Invalid option. Please try again.")

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
            f"[v] {show_menu.GENERAL_VIEW.value}",
            f"[s] {show_menu.SHOW_STATUS.value}",
            f"[d] {show_menu.SHOW_DIFFERENCES.value}",
            f"[h] {show_menu.SHOW_HISTORY.value}",
            f"[l] {show_menu.SHOW_LOCAL_REPO.value}",
            "[k] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "h", "g", "s", "d", "l", "k", "q", "H")
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            general_view()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 1:
            show_status_long()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 2:
            show_differences()
            # Ya no pedimos presionar Enter después de volver del sub-menú History
            clear_screen()
            continue
        elif menu_entry_index == 3:
            show_history()
            # Ya no pedimos presionar Enter después de volver del sub-menú History
            clear_screen()
            continue
        elif menu_entry_index == 4:
            show_local_repo()
            clear_screen()
            continue
        elif menu_entry_index == 5:
            clear_screen()
            return
        elif menu_entry_index == 6:
            quit()
        else:
            print("Invalid option. Please try again.")

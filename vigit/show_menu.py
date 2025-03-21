import subprocess
import sys
import termios
import tty
import re

from simple_term_menu import TerminalMenu
from .utils import CYAN, DARK_BLUE, GREEN, ENDC, BLUE, ORANGE, RED, WHITE, YELLOW, BOLD, UNDERLINE, global_menu, quit, invalid_opt, run_git_diff
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

        print(f"{BLUE}Detailed Status:{ENDC}")
        if status:
            # Usar el comando directamente para preservar colores
            subprocess.run(["git", "status"], check=True)
        else:
            print("Working tree clean")
        print()

        # # Mostrar el último commit después del status
        # print(f"{BLUE}Last Commit:{ENDC}")

        # # Verificar si hay commits antes de intentar mostrar el último
        # has_commits = subprocess.run(
        #     ["git", "rev-parse", "--verify", "HEAD"],
        #     capture_output=True,
        #     text=True
        # ).returncode == 0

        # if has_commits:
        #     # Mostrar solo el último commit con formato similar al de show_detailed_history
        #     subprocess.run([
        #         "git", "--no-pager", "log",
        #         "-1",  # Solo mostrar el último commit
        #         "--pretty=format:%C(yellow)● %h%Creset%C(auto)%d%Creset%C(blue) ► %C(white)%s%Creset %C(blue)| %C(cyan)%an%Creset %C(blue)| %C(magenta)%ad%Creset",
        #         "--decorate=short",
        #         "--date=relative"
        #     ], check=True)
        #     print("\n")
        # else:
        #     print(f"{YELLOW}No commits yet in this repository.{ENDC}\n")
    except Exception as e:
        print(f"Error getting status: {e}")

    # Do not show Overall Status or Last Commit after displaying git status

def show_tracking_history(ask_for_enter=True):
    """Muestra un historial de commits con estadísticas de archivos modificados"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Tracking History of modified files:{ENDC}\n")

        # Verificar si hay commits antes de intentar mostrar el historial
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"{YELLOW}No commits yet in this repository.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

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
        print(f"{YELLOW}No tracking history available.{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

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
            "[␣] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "h", "x", "t", "d", " ", "q")
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        # Si se presionó la barra espaciadora, volvemos al menú anterior
        if chosen_key == " ":
            clear_screen()
            return

        # Procesamos la selección normal del menú
        if menu_entry_index == 0 or chosen_key == "h":
            show_detailed_history()
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "x":
            show_expanded_history()
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "t":
            show_tracking_history()
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "d":
            show_differences_history()
            clear_screen()
            continue
        elif menu_entry_index == 4:
            clear_screen()
            return
        elif menu_entry_index == 5 or chosen_key == "q":
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

        # Verificar si hay commits antes de intentar mostrar el historial
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"{YELLOW}No commits yet in this repository.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Mostrar el historial de commits con formato gráfico expandido
        subprocess.run([
            "git", "--no-pager", "log",
            "--graph",
            "--all",
            "--pretty=format:%C(yellow)%h%Creset%C(auto)%d%Creset %C(cyan)%an%Creset %C(magenta)%ar%Creset%n  %C(white)%s%Creset",
            "--decorate=short",
            "--date=relative"
        ], check=True)
        print()

        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"{YELLOW}No expanded commit history available.{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_detailed_history(ask_for_enter=True):
    """Muestra un historial detallado de commits en orden cronológico"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Detailed Commit History:{ENDC}\n")

        # Verificar si hay commits antes de intentar mostrar el historial
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"{YELLOW}No commits yet in this repository.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

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
        print(f"{YELLOW}No commit history available.{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_history(ask_for_enter=True):
    """Muestra un historial detallado de commits con diferencias y estadísticas"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences History of Commits:{ENDC}\n")

        # Verificar si hay commits antes de intentar mostrar el historial
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"{YELLOW}No commits yet in this repository.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Comando completo usando subprocess.run con shell=True para mantener el pipeline
        subprocess.run([
            "git", "log",
            "--color=always",
            "--stat",
            "-p",
            "--pretty=format:%C(white)$(printf '%.0s-' {1..30})%Creset%n%C(yellow)● %h%Creset%C(auto)%d%Creset%n%C(blue)► %C(white)%s%Creset %C(blue)| %C(cyan)%an%Creset %C(blue)| %C(magenta)%ad%Creset",
            "--date=format:%Y-%m-%d %H:%M%n | diff-so-fancy | less -R"
        ], shell=True, check=True)
        print("\n")

    except Exception as e:
        print(f"{YELLOW}No differences history available.{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_non_staged(ask_for_enter=True):
    """Muestra las diferencias de los archivos no staged"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences of non staged files:{ENDC}\n")

        # Verificar si hay diferencias no staged
        has_differences = subprocess.run(
            ["git", "diff", "--quiet"],
            capture_output=True
        ).returncode != 0

        if not has_differences:
            print(f"{YELLOW}No differences found. Working tree clean.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

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
    """Muestra las diferencias de los archivos staged"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences of Added files:{ENDC}\n")

        # Verificar si hay diferencias staged
        has_differences = subprocess.run(
            ["git", "diff", "--staged", "--quiet"],
            capture_output=True
        ).returncode != 0

        if not has_differences:
            print(f"{YELLOW}No staged differences found. No files have been added.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

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
    """Muestra las diferencias con HEAD"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Differences with HEAD:{ENDC}\n")

        # Verificar si el repo está vacío (sin commits)
        is_empty_repo = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True
        ).returncode != 0

        if is_empty_repo:
            print(f"{YELLOW}No commits yet in this repository. Cannot compare with HEAD.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Verificar si hay diferencias con HEAD
        has_differences = subprocess.run(
            ["git", "diff", "HEAD", "--quiet"],
            capture_output=True
        ).returncode != 0

        if not has_differences:
            print(f"{YELLOW}No differences with HEAD found. Working tree matches the last commit.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

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
    """Muestra las diferencias entre dos commits seleccionados"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Select commits to compare differences:{ENDC}\n")

        # Obtener commits en color (últimos 10)
        result = subprocess.run(
            ["git", "--no-pager", "log", "--oneline", "--color", "--decorate", "--max-count=10"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0 or not result.stdout.strip():
            print(f"{YELLOW}No commits yet in this repository. Cannot compare differences between commits.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        commits = result.stdout.strip().split("\n")
        commit_hashes = [commit.split()[0] for commit in commits]

        print(f"{YELLOW}Recent commits:{ENDC}")
        for idx, commit in enumerate(commits):
            parts = commit.split(" ", 1)
            if len(parts) == 2:
                print(f"{idx + 1}. {parts[0]} {DARK_BLUE}▶{ENDC} {parts[1]}")
            else:
                print(f"{idx + 1}. {commit}")

        print(f"\n{YELLOW}Select base commit (older):{ENDC}")
        base_idx = int(input("Enter number: ")) - 1
        base_commit = commit_hashes[base_idx]

        print(f"\n{YELLOW}Select compare commit (newer):{ENDC}")
        for idx, commit in enumerate(commits):
            if idx != base_idx:
                print(f"{idx + 1}. {commit}")

        compare_idx = int(input("Enter number: ")) - 1
        compare_commit = commit_hashes[compare_idx]

        print(f"\n{BLUE}Differences between commits {base_commit} and {compare_commit}:{ENDC}\n")

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
        print(f"{YELLOW}Error comparing commits: {e}{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_differences_between_branches(ask_for_enter=True):
    """Muestra las diferencias entre dos ramas seleccionadas"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Select branches to compare differences:{ENDC}\n")

        # Verificar si hay commits
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not has_commits:
            print(f"{YELLOW}No commits yet in this repository. Cannot compare differences between branches.{ENDC}")
            if ask_for_enter:
                print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
                get_single_keypress()
            return

        # Obtener ramas locales y remotas
        result_local = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True
        )
        result_remote = subprocess.run(
            ["git", "branch", "-r"],
            capture_output=True,
            text=True
        )

        local_raw = result_local.stdout.strip().split("\n")
        current_branch = None
        local_branches = []

        for b in local_raw:
            if b.startswith("* "):
                branch_name = b[2:].strip()
                current_branch = branch_name
                local_branches.append(f"* {branch_name}")
            else:
                local_branches.append(f"  {b.strip()}")

        remote_branches = [f"  {b.strip()}" for b in result_remote.stdout.strip().split("\n")]

        # Unir ambas listas con índice global
        all_branches = local_branches + remote_branches
        print(f"{YELLOW}Local branches:{ENDC}")
        for idx, b in enumerate(local_branches):
            print(f"{idx + 1}. {GREEN if b.startswith('*') else ''}{b}{ENDC}")

        print(f"\n{YELLOW}Remote branches:{ENDC}")
        for i, b in enumerate(remote_branches, start=len(local_branches) + 1):
            print(f"{i}. {CYAN}{b}{ENDC}")

        # Input usuario
        first_idx = int(input(f"\n{YELLOW}Select first branch (by number):{ENDC} ")) - 1
        first_branch = all_branches[first_idx].strip("* ").strip()

        print()
        for idx, b in enumerate(all_branches):
            if idx != first_idx:
                print(f"{idx + 1}. {b}")

        second_idx = int(input(f"\n{YELLOW}Select second branch:{ENDC} ")) - 1
        second_branch = all_branches[second_idx].strip("* ").strip()

        print(f"\n{BLUE}Differences between branches {first_branch} and {second_branch}:{ENDC}\n")

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
        print(f"{YELLOW}Error comparing branches: {e}{ENDC}")
        if ask_for_enter:
            print(f"\n{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_local_repo(ask_for_enter=True):
    """Muestra información básica del repositorio local"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"{BLUE}Local Repository Information:{ENDC}\n")

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

        # Obtener todas las ramas locales
        all_branches = subprocess.run(
            ["git", "branch", "--color=always"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Mostrar información básica
        print(f"{YELLOW}Repository Name:{ENDC} {repo_name}")
        print(f"{YELLOW}Repository Path:{ENDC} {repo_path}")
        print(f"{YELLOW}Current Branch:{ENDC} {current_branch}")

        # Mostrar todas las ramas locales
        print(f"\n{YELLOW}Local Branches:{ENDC}")
        if all_branches:
            print(all_branches)
        else:
            print("No local branches found.")

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving repository information: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_remote_repo(ask_for_enter=True):
    """Muestra información sobre los repositorios remotos"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"\n{BLUE}Remote Repository Information:{ENDC}")

        # Obtener información detallada del remoto
        remote_info = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Obtener todas las ramas remotas
        remote_branches = subprocess.run(
            ["git", "branch", "-r", "--color=always"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Mostrar información del remoto
        print(f"\n{YELLOW}Remote URLs:{ENDC}")
        if remote_info:
            print(remote_info)
        else:
            print("No remote repositories configured")

        # Mostrar ramas remotas
        print(f"\n{YELLOW}Remote Branches:{ENDC}")
        if remote_branches:
            print(remote_branches)
        else:
            print("No remote branches available")

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving remote repository information: {e}")
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

def show_branches(ask_for_enter=True):
    """Muestra información detallada sobre todas las ramas del repositorio"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        print(f"{BLUE}All Branches Information:{ENDC}")

        # Obtener rama actual
        current_branch = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True
        ).stdout.strip()

        # Mostrar la rama actual
        print(f"\n{YELLOW}Current Branch:{ENDC} {current_branch}")

        # Mostrar todas las ramas locales
        print(f"\n{YELLOW}Local Branches:{ENDC}")
        result = subprocess.Popen(
            ["git", "--no-pager", "branch", "--color=always", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Procesa la salida en tiempo real
        for line in result.stdout:
            # Resalta los commit_hash en naranja, agrega un círculo a la izquierda y el símbolo ► en azul
            colored_line = re.sub(
                r'([a-f0-9]{7,40})\s(.*)',  # Captura el commit_hash y el mensaje de commit
                f'{ORANGE}● \\1{DARK_BLUE} ► {ENDC}\\2',  # Aplica colores y formatea la salida
                line
            )
            print(colored_line, end='')

        # Espera a que el proceso termine
        result.wait()

        # Mostrar todas las ramas remotas
        print(f"\n{YELLOW}Remote Branches:{ENDC}")
        result = subprocess.Popen(
            ["git", "--no-pager", "branch", "-r", "--color=always", "-v"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Procesa la salida en tiempo real
        for line in result.stdout:
            # Resalta los commit_hash en naranja, agrega un círculo a la izquierda y el símbolo ► en azul oscuro
            colored_line = re.sub(
                r'([a-f0-9]{7,40})\s(.*)',  # Captura el commit_hash y el mensaje de commit
                f'{ORANGE}● \\1{DARK_BLUE} ► {ENDC}\\2',  # Aplica colores y formatea la salida
                line
            )
            print(colored_line, end='')

        # Espera a que el proceso termine
        result.wait()

        # Mostrar ramas fusionadas
        print(f"\n{YELLOW}Merged Branches:{ENDC}")
        subprocess.run(
            ["git", "--no-pager", "branch", "--color=always", "--merged"],
            check=True
        )

        # Mostrar ramas no fusionadas
        print(f"\n{YELLOW}Non Merged Branches:{ENDC}")
        subprocess.run(
            ["git", "--no-pager", "branch", "--color=always", "--no-merged"],
            check=True
        )

        print()
        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
    except Exception as e:
        print(f"Error retrieving branches information: {e}")
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
            "[␣] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "d", "a", "c", "b", " ", "q")
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        # Si se presionó la barra espaciadora, volvemos al menú anterior
        if chosen_key == " ":
            clear_screen()
            return

        # Procesamos la selección normal del menú
        if menu_entry_index == 0 or chosen_key == "d":
            show_differences_non_staged()
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "a":
            show_differences_staged()
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "c":
            show_differences_between_commits()
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "b":
            show_differences_between_branches()
            clear_screen()
            continue
        elif menu_entry_index == 4:
            clear_screen()
            return
        elif menu_entry_index == 5 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

def show_status_short(ask_for_enter=True):
    """Muestra un status corto (-s) y el último commit"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Capturar la salida del comando git status -s
        result = subprocess.run(
            ["git", "status", "-s"],
            capture_output=True,
            text=True,
            check=True
        )
        status = result.stdout.strip()

        print(f"\n{BLUE}Status:{ENDC}")
        if status:
            # Usar el comando directamente para preservar colores
            subprocess.run(["git", "status", "-s"], check=True)
        else:
            print("Working tree clean")
        print()

        # Mostrar el último commit después del status
        print(f"{BLUE}Last Commit:{ENDC}")

        # Verificar si hay commits antes de intentar mostrar el último
        has_commits = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True
        ).returncode == 0

        if has_commits:
            # Mostrar solo el último commit con formato similar al de show_detailed_history
            subprocess.run([
                "git", "--no-pager", "log",
                "-1",  # Solo mostrar el último commit
                "--pretty=format:%C(yellow)● %h%Creset%C(auto)%d%Creset%C(blue) ► %C(white)%s%Creset %C(blue)| %C(cyan)%an%Creset %C(blue)| %C(magenta)%ad%Creset",
                "--decorate=short",
                "--date=relative"
            ], check=True)
            print("\n")
        else:
            print(f"{YELLOW}No commits yet in this repository.{ENDC}\n")

        if ask_for_enter:
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()

    except Exception as e:
        print(f"Error getting status: {e}")

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

        menu_options = [
            f"[v] {show_menu.GENERAL_VIEW.value}",
            f"[s] {show_menu.SHOW_STATUS.value}",
            f"[d] {show_menu.SHOW_DIFFERENCES.value}",
            f"[h] {show_menu.SHOW_HISTORY.value}",
            f"[l] {show_menu.SHOW_LOCAL_REPO.value}",
            f"[r] {show_menu.SHOW_REMOTE_REPO.value}",
            f"[b] {show_menu.SHOW_BRANCHES.value}",
            "[␣] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title=f"Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE,
            accept_keys=("enter", "v", "s", "d", "h", "l", "r", "b", " ", "q")
        )

        menu_entry_index = terminal_menu.show()
        chosen_key = terminal_menu.chosen_accept_key

        # Si se presionó la barra espaciadora, volvemos al menú anterior
        if chosen_key == " ":
            clear_screen()
            return

        # Procesamos la selección normal del menú
        if menu_entry_index == 0 or chosen_key == "v":
            general_view()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 1 or chosen_key == "s":
            show_status_long()
            # Prevents returning to the "Show" menu which would display the "Overall Status" again
            print(f"{GREEN}Press any key to return to the menu...{ENDC}")
            get_single_keypress()
            clear_screen()
            continue
        elif menu_entry_index == 2 or chosen_key == "d":
            show_differences()
            # Ya no pedimos presionar Enter después de volver del sub-menú History
            clear_screen()
            continue
        elif menu_entry_index == 3 or chosen_key == "h":
            show_history()
            # Ya no pedimos presionar Enter después de volver del sub-menú History
            clear_screen()
            continue
        elif menu_entry_index == 4 or chosen_key == "l":
            show_local_repo()
            clear_screen()
            continue
        elif menu_entry_index == 5 or chosen_key == "r":
            show_remote_repo()
            clear_screen()
            continue
        elif menu_entry_index == 6 or chosen_key == "b":
            show_branches()
            clear_screen()
            continue
        elif menu_entry_index == 7:
            clear_screen()
            return
        elif menu_entry_index == 8 or chosen_key == "q":
            quit()
        else:
            print("Invalid option. Please try again.")

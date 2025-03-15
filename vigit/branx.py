import subprocess
import sys
import os

from .utils import YELLOW, GREEN, ENDC
from .mainm import commit_to_local_repo
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main

from enum import Enum
from simple_term_menu import TerminalMenu

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)


class branch_menu(Enum):
    BRANCH_LOCAL = 'Local'
    BRANCH_LOCAL_TO_REMOTE = 'Local to Remote'
    BRANCH_REMOTE_TO_LOCAL = 'Remote to Local'
    MANAGE_BRANCHES = 'Manage Branches'


def work_in_branches():
    current = current_branch()
    while True:

        print(f"\n{GREEN}Work in branches{ENDC} (Currently on: {current}):")

        menu_options = [
            f"[l] {branch_menu.BRANCH_LOCAL.value}",
            f"[t] {branch_menu.BRANCH_LOCAL_TO_REMOTE.value}",
            f"[r] {branch_menu.BRANCH_REMOTE_TO_LOCAL.value}",
            f"[m] {branch_menu.MANAGE_BRANCHES.value}",
            f"[a] Operaciones avanzadas",
            f"[x] Back to main menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            branch_local()
        elif menu_entry_index == 1:
            branch_local_to_remote()
        elif menu_entry_index == 2:
            branch_remote_to_local()
        elif menu_entry_index == 3:
            manage_branches()
        elif menu_entry_index == 4:
            advanced_operations()
        elif menu_entry_index == 5:
            clear_screen()
            break
        elif menu_entry_index == 6:
            sys.exit("Exiting VisualGit...\n")


# BRANCHES LOCAL
class branch_local_menu(Enum):
    CHECK_LOCAL_BRANCH = 'See Local Branches'
    ADD_LOCAL_BRANCH = 'Add a Local Branch'
    GOTO_BRANCH = 'Go to Branch'
    GOTO_MAIN = 'Go to Main'

def branch_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Local{ENDC} (Currently on: {current}):")
        else:
            print("\nBranches -Local:")

        options = [
            f"[s] See Local Branches",
            f"[a] Add a Local Branch",
            f"[c] Commit to Current Branch",
            f"[b] Go to Branch",
            f"[g] Go to Main",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(options, title="Please select an option:")
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
        print("\nRamas locales:")
        for branch in branches:
            print(f"  {branch}")
    except Exception as e:
        print(f"Error al mostrar las ramas locales: {e}")

def create_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return
    elif not has_commits():
        print_not_commits()
        return

    branch_name = input("Enter the name of the new branch: ")
    try:
        subprocess.run(["git", "branch", branch_name])
        print(f"Branch {branch_name} created successfully.")
    except Exception as e:
        print(f"Error creating branch {branch_name}: {e}")

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
                subprocess.run(["git", "checkout", selected_branch])
            else:
                print("Invalid choice.")
        else:
            print("No local branches found. Create one to proceed.")
    except Exception as e:
        print(f"Error switching branches: {e}")

def go_to_main():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "checkout", "main"])
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
            print("Ramas locales:")
            for idx, branch in enumerate(branches, 1):
                print(f"{idx}. {branch}")

            choice = int(input("Selecciona una rama para cambiar (por número): "))

            if 1 <= choice <= len(branches):
                selected_branch = branches[choice - 1].replace('*', '').strip()  # Quitar el '*' que indica la rama actual

                # Verificar si hay cambios sin confirmar
                status_result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    stdout=subprocess.PIPE,
                    text=True
                )

                if status_result.stdout.strip():
                    print(f"{YELLOW}Tienes cambios sin confirmar que se perderán al cambiar de rama.{ENDC}")
                    force_option = input("¿Qué deseas hacer?\n1. Guardar cambios en stash y cambiar\n2. Descartar cambios y cambiar\n3. Cancelar\nSelecciona opción (1-3): ")

                    if force_option == "1":
                        # Guardar en stash y cambiar
                        subprocess.run(["git", "stash", "push", "-u", "-m", f"Cambios automáticos antes de cambiar a {selected_branch}"])
                        subprocess.run(["git", "checkout", selected_branch])
                        print(f"{GREEN}Cambios guardados en stash y cambiado a rama {selected_branch}.{ENDC}")
                        print("Para recuperar tus cambios, usa 'git stash pop' cuando vuelvas a esta rama.")
                    elif force_option == "2":
                        # Forzar el cambio descartando cambios
                        subprocess.run(["git", "checkout", "-f", selected_branch])
                        print(f"{GREEN}Cambiado a rama {selected_branch}. Los cambios sin confirmar han sido descartados.{ENDC}")
                    else:
                        print("Operación cancelada.")
                else:
                    # No hay cambios, cambiar normalmente
                    subprocess.run(["git", "checkout", selected_branch])
                    print(f"{GREEN}Cambiado a rama {selected_branch}.{ENDC}")
            else:
                print("Opción inválida.")
        else:
            print("No se encontraron ramas locales. Crea una para continuar.")
    except Exception as e:
        print(f"Error al cambiar de rama: {e}")


# BRANCHES LOCAL_TO_REMOTE
class branch_lr_menu(Enum):
    CHECK_REMOTE_BRANCH = 'See Remote Branches'
    LINK_REMOTE_BRANCH = 'Join Local Branch to Remote'
    COMMIT_LOCAL_BRANCH = 'Commit to Local Branch'
    PUSH_BRANCH = 'Push Changes to Remote Branch'
    COMMIT_PUSH_BRANCH = 'Commit & Push in Branch'

def branch_local_to_remote():
    if is_current_branch_main():
        print(f"{YELLOW}You are now in main. Go to a branch to proceed.{ENDC}\nTo go to a branch: Quick actions -> Go to branch")
        return

    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Local to remote{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Branches -Local to remote:{ENDC}")

        menu_options = [
            f"[s] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[j] {branch_lr_menu.LINK_REMOTE_BRANCH.value}",
            f"[c] {branch_lr_menu.COMMIT_LOCAL_BRANCH.value}",
            f"[p] {branch_lr_menu.PUSH_BRANCH.value}",
            f"[b] {branch_lr_menu.COMMIT_PUSH_BRANCH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_branches()
        elif menu_entry_index == 1:
            check_remote_branches()
        elif menu_entry_index == 2:
            connect_local_branch_with_remote()
        elif menu_entry_index == 3:
            commit_in_local_branch()
        elif menu_entry_index == 4:
            push_changes_to_remote_branch()
        elif menu_entry_index == 5:
            commit_and_push_in_branch()
        elif menu_entry_index == 6:
            clear_screen()
            break
        elif menu_entry_index == 7:
            quit()
        else:
            invalid_opt()

def check_remote_branches():
    branch = current_branch()

    if not has_commits():
        print_not_commits()
        return
    elif not is_local_branch_connected_to_remote(branch):
        print(f"{YELLOW}The local branch {branch} is not connected to a remote branch. Please connect to remote branch to proceed{ENDC}\n To connect to remote branch: Work in branches -> Local -> Link local branch to remote")
        return

    try:
        # Use --no-pager to prevent Git from using vi/less and capture the output to display it directly
        result = subprocess.run(["git", "--no-pager", "branch", "-r"],
                               capture_output=True,
                               text=True)

        branches = result.stdout.strip().split('\n')
        print("\nRamas remotas:")
        for branch in branches:
            print(f"  {branch}")
    except Exception as e:
        print(f"Error al mostrar las ramas remotas: {e}")

def connect_local_branch_with_remote():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    if is_local_branch_connected_to_remote(branch):
        print(f"{YELLOW}The local branch {branch} is already connected to a remote branch.{ENDC}")
        return

    remote_url = input("Enter the remote repository (GitHub) URL: ")
    try:
        subprocess.run(["git", "branch", "--set-upstream-to", f"origin/{branch}", branch])
        print(f"Connected local branch {branch} with remote: {remote_url}")
    except Exception as e:
        print(f"Error connecting local branch with remote: {e}")

def commit_in_local_branch():

    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])
    except Exception as e:
        print(f"Error committing in local branch: {e}")

def push_changes_to_remote_branch():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    try:
        # Intentar hacer un push normal primero
        result = subprocess.run(
            ["git", "push", "origin", branch],
            capture_output=True,
            text=True
        )

        # Si el push normal es exitoso
        if result.returncode == 0:
            print(f"{GREEN}Cambios enviados correctamente a la rama remota {branch}.{ENDC}")
        else:
            # Si el push falla, mostrar el error y ofrecer force push
            print(f"{YELLOW}No se pudieron enviar los cambios a la rama remota.{ENDC}")
            print(f"Razón: {result.stderr.strip()}")

            # Preguntar si quiere hacer un force push
            force_push = input(f"\n¿Quieres forzar el push? {YELLOW}ADVERTENCIA: Esto puede sobrescribir cambios en el repositorio remoto. Esta acción es potencialmente destructiva.{ENDC} (s/n): ").lower()

            if force_push == 's':
                print(f"{YELLOW}Ejecutando force push...{ENDC}")
                force_result = subprocess.run(
                    ["git", "push", "--force", "origin", branch],
                    capture_output=True,
                    text=True
                )

                if force_result.returncode == 0:
                    print(f"{GREEN}Force push completado. Los cambios han sido enviados forzosamente a la rama remota {branch}.{ENDC}")
                else:
                    print(f"{YELLOW}El force push falló: {force_result.stderr.strip()}{ENDC}")
            else:
                print("Operación de push cancelada.")

    except Exception as e:
        print(f"Error enviando cambios a la rama remota: {e}")

def commit_and_push_in_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    branch = current_branch()
    if not branch:
        print("Error determining the current branch.")
        return

    try:
        subprocess.run(["git", "add", "."])
        message = input("Enter commit message: ")
        subprocess.run(["git", "commit", "-m", message])
        subprocess.run(["git", "push", "origin", branch])
        print(f"Changes committed and pushed to branch {branch}")
    except Exception as e:
        print(f"Error committing and pushing in branch: {e}")


# BRANCHES REMOTE_TO_LOCAL
class branch_rl_menu(Enum):
    CLONE_BRANCH = 'Join Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'

def branch_remote_to_local():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Branches -Remote to local{ENDC} (Currently on: {current}):")
        else:
            print(f"\n{GREEN}Branches -Remote to local:{ENDC}")

        menu_options = [
            f"[s] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[l] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[j] {branch_rl_menu.CLONE_BRANCH.value}",
            f"[y] {branch_rl_menu.PULL_BRANCH.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_remote_branches()
        elif menu_entry_index == 1:
            check_local_branches()
        elif menu_entry_index == 2:
            clone_remote_branch_to_local()
        elif menu_entry_index == 3:
            pull_remote_changes_to_local()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            quit()
        else:
            invalid_opt()

def clone_remote_branch_to_local():
    remote_branch = input("Enter the name of the remote branch you want to clone: ")
    try:
        subprocess.run(["git", "checkout", "--track", f"origin/{remote_branch}"])
        print(f"Cloned and switched to the remote branch {remote_branch}")
    except Exception as e:
        print(f"Error cloning remote branch: {e}")

def pull_remote_changes_to_local():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    try:
        # Intentar hacer un pull normal primero
        result = subprocess.run(
            ["git", "pull", "origin", branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # Si el pull normal es exitoso
        if result.returncode == 0:
            print(f"{GREEN}Cambios remotos incorporados correctamente a la rama local {branch}.{ENDC}")
        else:
            # Si el pull falla, mostrar el error y ofrecer opciones avanzadas
            print(f"{YELLOW}No se pudieron incorporar los cambios remotos.{ENDC}")
            print(f"Razón: {result.stderr.strip()}")

            # Preguntar qué estrategia quiere usar
            print("\nOpciones disponibles:")
            print("1. Rebase (reposiciona tus cambios encima de los remotos)")
            print("2. Force pull (descarta cambios locales no confirmados)")
            print("3. Cancelar operación")

            choice = input("\nSelecciona una opción (1-3): ")

            if choice == "1":
                print(f"{YELLOW}Ejecutando pull con rebase...{ENDC}")
                rebase_result = subprocess.run(
                    ["git", "pull", "--rebase", "origin", branch],
                    capture_output=True,
                    text=True
                )

                if rebase_result.returncode == 0:
                    print(f"{GREEN}Pull con rebase completado correctamente.{ENDC}")
                else:
                    print(f"{YELLOW}El pull con rebase falló: {rebase_result.stderr.strip()}{ENDC}")
                    print("Puede que necesites resolver conflictos manualmente.")

            elif choice == "2":
                confirm = input(f"{YELLOW}ADVERTENCIA: Esto descartará todos los cambios locales no confirmados. ¿Estás seguro? (s/n): {ENDC}").lower()
                if confirm == "s":
                    # Guardar trabajo actual
                    subprocess.run(["git", "stash", "push", "-u"])
                    # Resetear cambios locales
                    subprocess.run(["git", "reset", "--hard", f"origin/{branch}"])
                    print(f"{GREEN}Los cambios locales han sido reseteados al estado del repositorio remoto.{ENDC}")
                    print("Tus cambios no confirmados se han guardado en git stash.")
                else:
                    print("Operación cancelada.")

            else:
                print("Operación cancelada.")

    except Exception as e:
        print(f"Error al incorporar cambios remotos: {e}")


# BRANCHES MANAGE_BRANCHES
class manage_branch_menu(Enum):
    MERGE = 'Merge Branch with Main'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'
    DELETE_LOCAL_BRANCH = 'Delete Local Branch'
    DELETE_REMOTE_BRANCH = 'Delete Remote Branch'


def manage_branches():
    while True:
        current = current_branch()
        if current:
            print(f"\n{GREEN}Gestionar ramas{ENDC} (Actualmente en: {current}):")
        else:
            print(f"\n{GREEN}Gestionar ramas:{ENDC}")

        menu_options = [
            f"[s] {branch_local_menu.CHECK_LOCAL_BRANCH.value}",
            f"[r] {branch_lr_menu.CHECK_REMOTE_BRANCH.value}",
            f"[m] {manage_branch_menu.MERGE.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[gf] Ir a rama (forzado)",
            f"[gm] {branch_local_menu.GOTO_MAIN.value}",
            f"[dl] {manage_branch_menu.DELETE_LOCAL_BRANCH.value}",
            f"[dr] {manage_branch_menu.DELETE_REMOTE_BRANCH.value}",
            "[x] Volver al menú anterior",
            "[q] Salir del programa"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Por favor, selecciona una opción:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            check_local_branches()
        elif menu_entry_index == 1:
            check_remote_branches()
        elif menu_entry_index == 2:
            merge_branch_with_main()
        elif menu_entry_index == 3:
            go_to_branch()
        elif menu_entry_index == 4:
            go_to_branch_force()
        elif menu_entry_index == 5:
            go_to_main()
        elif menu_entry_index == 6:
            delete_local_branch()
        elif menu_entry_index == 7:
            delete_remote_branch()
        elif menu_entry_index == 8:
            clear_screen()
            break
        elif menu_entry_index == 9:
            quit()

def merge_branch_with_main():
    if not is_git_repo():
        print_not_git_repo()
        return
    if is_current_branch_main():
        print(f"{YELLOW}Ya estás en la rama main. Ve a otra rama para proceder.{ENDC}\nPara ir a otra rama: Acciones rápidas -> Ir a rama")
        return

    branch = current_branch()
    if not branch or branch == "main":
        print("Estás en la rama main o no se pudo determinar la rama actual.")
        return

    try:
        # Ir a la rama main
        subprocess.run(["git", "checkout", "main"])

        # Intentar hacer un merge normal primero
        result = subprocess.run(
            ["git", "merge", branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # Si el merge normal es exitoso
        if result.returncode == 0:
            print(f"{GREEN}Rama {branch} fusionada correctamente con main.{ENDC}")
        else:
            # Si el merge falla, mostrar el error y ofrecer opciones
            print(f"{YELLOW}No se pudo fusionar la rama {branch} con main.{ENDC}")
            print(f"Razón: {result.stderr.strip()}")

            # Ofrecer opciones para resolver
            print("\nOpciones disponibles:")
            print("1. Merge forzado (estrategia ours - prioriza cambios de main)")
            print("2. Merge forzado (estrategia theirs - prioriza cambios de la rama)")
            print("3. Cancelar operación")

            choice = input("\nSelecciona una opción (1-3): ")

            if choice == "1":
                print(f"{YELLOW}Ejecutando merge forzado (ours)...{ENDC}")
                ours_result = subprocess.run(
                    ["git", "merge", "-X", "ours", branch],
                    capture_output=True,
                    text=True
                )

                if ours_result.returncode == 0:
                    print(f"{GREEN}Merge forzado completado. Se han priorizado los cambios de main.{ENDC}")
                else:
                    print(f"{YELLOW}El merge forzado falló: {ours_result.stderr.strip()}{ENDC}")

            elif choice == "2":
                print(f"{YELLOW}Ejecutando merge forzado (theirs)...{ENDC}")
                theirs_result = subprocess.run(
                    ["git", "merge", "-X", "theirs", branch],
                    capture_output=True,
                    text=True
                )

                if theirs_result.returncode == 0:
                    print(f"{GREEN}Merge forzado completado. Se han priorizado los cambios de la rama {branch}.{ENDC}")
                else:
                    print(f"{YELLOW}El merge forzado falló: {theirs_result.stderr.strip()}{ENDC}")

            else:
                print("Operación de merge cancelada.")
                # Volver a la rama original
                subprocess.run(["git", "checkout", branch])

    except Exception as e:
        print(f"Error al fusionar rama con main: {e}")
        # Intentar volver a la rama original en caso de error
        try:
            subprocess.run(["git", "checkout", branch])
        except:
            pass


def delete_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    # Show existing branches
    print("\nAvailable local branches:")
    check_local_branches()

    branch = input("\nEnter the name of the branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch.{ENDC}\nIf you want to delete the repository: Work in local -> Local -> Manage repos -> Delete local repo")
        return

    # Check if the branch exists
    try:
        branch_exists = subprocess.run(
            ["git", "show-ref", "--verify", f"refs/heads/{branch}"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not branch_exists:
            print(f"{YELLOW}The branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying branch existence: {e}")
        return

    # Check if it's the current branch
    current = current_branch()
    if current == branch:
        print(f"{YELLOW}You cannot delete the branch you are currently on.{ENDC}\nSwitch to another branch first using 'Go to Branch' or 'Go to Main'.")
        return

    # Try to delete the branch normally
    try:
        result = subprocess.run(
            ["git", "branch", "-d", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            # If it fails, probably has unmerged changes
            print(f"{YELLOW}Could not delete branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Ask if they want to force delete
            force_delete = input("\nDo you want to force deletion? This action is irreversible and you will lose all unmerged changes. (y/n): ").lower()

            if force_delete == 'y':
                force_result = subprocess.run(["git", "branch", "-D", branch])
                if force_result.returncode == 0:
                    print(f"{GREEN}The branch '{branch}' has been forcibly deleted.{ENDC}")
                else:
                    print(f"{YELLOW}Could not forcibly delete the branch: {force_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error deleting local branch: {e}")


def delete_remote_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    # Show available remote branches
    print("\nAvailable remote branches:")
    check_remote_branches()

    branch = input("\nEnter the name of the remote branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch of the remote repository.{ENDC}")
        return

    # Verify if the remote branch exists
    try:
        remote_branches = subprocess.run(
            ["git", "ls-remote", "--heads", "origin"],
            capture_output=True,
            text=True
        ).stdout

        if f"refs/heads/{branch}" not in remote_branches:
            print(f"{YELLOW}The remote branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying remote branch existence: {e}")
        return

    # Ask for confirmation
    confirm = input(f"\nAre you sure you want to delete the remote branch '{branch}'? This action is irreversible. (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

    # Delete the remote branch
    try:
        result = subprocess.run(
            ["git", "push", "origin", "--delete", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The remote branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            print(f"{YELLOW}Could not delete remote branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error deleting remote branch: {e}")

# Nueva sección para operaciones avanzadas

def advanced_operations():
    while True:
        print(f"\n{GREEN}Operaciones avanzadas{ENDC}")
        print(f"{YELLOW}ADVERTENCIA: Algunas de estas operaciones pueden ser destructivas.{ENDC}")

        menu_options = [
            "Reset (deshacer cambios a niveles específicos)",
            "Clean (eliminar archivos no rastreados)",
            "Force push (enviar cambios forzadamente)",
            "Stash (guardar cambios temporalmente)",
            "Cherry-pick (seleccionar commits específicos)",
            "Rebase interactivo (reorganizar/editar commits)",
            "Volver al menú principal"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Selecciona una operación:")
        choice = terminal_menu.show()

        if choice == 0:
            reset_operations()
        elif choice == 1:
            clean_untracked_files()
        elif choice == 2:
            force_push()
        elif choice == 3:
            stash_operations()
        elif choice == 4:
            cherry_pick_commits()
        elif choice == 5:
            interactive_rebase()
        elif choice == 6:
            clear_screen()
            break

def reset_operations():
    print(f"\n{GREEN}Operaciones de Reset{ENDC}")
    print(f"{YELLOW}ADVERTENCIA: Estas operaciones pueden ser destructivas.{ENDC}")

    menu_options = [
        "Soft reset (conserva cambios en el área de preparación)",
        "Mixed reset (conserva cambios en archivos pero los saca del área de preparación)",
        "Hard reset (descarta todos los cambios locales)",
        "Volver al menú anterior"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Selecciona el tipo de reset:")
    choice = terminal_menu.show()

    if choice == 3:  # Volver atrás
        return

    # Obtener el commit al que hacer reset
    print("\nOpciones de reset:")
    print("1. Reset al último commit")
    print("2. Reset a un número específico de commits atrás")
    print("3. Reset a un hash de commit específico")

    reset_option = input("Selecciona una opción (1-3): ")

    reset_target = ""
    if reset_option == "1":
        reset_target = "HEAD~1"
    elif reset_option == "2":
        num_commits = input("¿Cuántos commits atrás? ")
        try:
            reset_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Número inválido. Operación cancelada.")
            return
    elif reset_option == "3":
        # Mostrar últimos commits para referencia
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
        reset_target = input("\nIngresa el hash del commit: ")
    else:
        print("Opción inválida. Operación cancelada.")
        return

    # Confirmar la operación
    confirm = input(f"{YELLOW}Esta operación puede ser destructiva. ¿Estás seguro? (s/n): {ENDC}").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    # Ejecutar el reset correspondiente
    reset_type = ["--soft", "--mixed", "--hard"][choice]
    try:
        result = subprocess.run(
            ["git", "reset", reset_type, reset_target],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Reset {reset_type} completado correctamente.{ENDC}")
            if reset_type == "--hard":
                print("Todos los cambios locales han sido descartados.")
            elif reset_type == "--soft":
                print("Los cambios se han conservado en el área de preparación.")
            else:  # mixed
                print("Los cambios se han conservado en los archivos pero se han sacado del área de preparación.")
        else:
            print(f"{YELLOW}Error al ejecutar reset: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error durante el reset: {e}")

def clean_untracked_files():
    print(f"\n{GREEN}Limpiar archivos no rastreados{ENDC}")

    # Mostrar archivos no rastreados
    print("\nArchivos no rastreados:")
    subprocess.run(["git", "ls-files", "--others", "--exclude-standard"])

    menu_options = [
        "Modo interactivo (seleccionar archivos a eliminar)",
        "Eliminar todos los archivos no rastreados",
        "Eliminar archivos no rastreados y directorios",
        "Volver al menú anterior"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Selecciona una opción:")
    choice = terminal_menu.show()

    if choice == 3:  # Volver atrás
        return

    # Confirmar la operación
    if choice == 0:
        print("Iniciando modo interactivo...")
        subprocess.run(["git", "clean", "-i"])
    else:
        # Para opciones 1 y 2, pedir confirmación explícita
        clean_message = "todos los archivos no rastreados"
        clean_command = ["git", "clean", "-f"]

        if choice == 1:
            clean_message = "todos los archivos no rastreados"
        elif choice == 2:
            clean_message = "todos los archivos no rastreados y directorios"
            clean_command = ["git", "clean", "-fd"]

        confirm = input(f"{YELLOW}¿Estás seguro de que quieres eliminar {clean_message}? Esta acción no se puede deshacer. (s/n): {ENDC}").lower()
        if confirm == "s":
            try:
                result = subprocess.run(clean_command, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"{GREEN}Limpieza completada correctamente.{ENDC}")
                else:
                    print(f"{YELLOW}Error durante la limpieza: {result.stderr.strip()}{ENDC}")
            except Exception as e:
                print(f"Error durante la limpieza: {e}")
        else:
            print("Operación cancelada.")

def force_push():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    print(f"\n{GREEN}Force Push{ENDC}")
    print(f"{YELLOW}ADVERTENCIA: Esta operación puede sobrescribir cambios en el repositorio remoto.{ENDC}")

    # Ofrecer opciones para diferentes tipos de force push
    menu_options = [
        "Force push normal (--force)",
        "Force push seguro (--force-with-lease)",
        "Volver al menú anterior"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Selecciona el tipo de force push:")
    choice = terminal_menu.show()

    if choice == 2:  # Volver atrás
        return

    # Confirmar la operación
    warning_message = "Esta acción puede sobrescribir cambios remotos permanentemente."
    if choice == 0:
        confirm = input(f"{YELLOW}Force push normal: {warning_message} ¿Estás seguro? (s/n): {ENDC}").lower()
        push_option = "--force"
    else:  # choice == 1
        confirm = input(f"{YELLOW}Force push seguro: Solo sobrescribirá si no hay cambios nuevos en remoto. ¿Continuar? (s/n): {ENDC}").lower()
        push_option = "--force-with-lease"

    if confirm != "s":
        print("Operación cancelada.")
        return

    # Ejecutar el force push
    try:
        result = subprocess.run(
            ["git", "push", push_option, "origin", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Force push completado. Los cambios han sido enviados forzosamente a la rama remota {branch}.{ENDC}")
        else:
            print(f"{YELLOW}El force push falló: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error durante el force push: {e}")

def stash_operations():
    print(f"\n{GREEN}Operaciones con Stash{ENDC}")

    menu_options = [
        "Guardar cambios en stash",
        "Listar stashes guardados",
        "Aplicar stash (conservando en la lista)",
        "Aplicar y eliminar stash",
        "Eliminar stash específico",
        "Eliminar todos los stashes",
        "Volver al menú anterior"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Selecciona una operación:")
    choice = terminal_menu.show()

    if choice == 0:  # Guardar en stash
        message = input("Mensaje descriptivo para el stash (opcional): ")
        try:
            if message:
                result = subprocess.run(["git", "stash", "push", "-m", message], capture_output=True, text=True)
            else:
                result = subprocess.run(["git", "stash", "push"], capture_output=True, text=True)

            if result.returncode == 0:
                if "No local changes to save" in result.stdout:
                    print("No hay cambios locales para guardar en stash.")
                else:
                    print(f"{GREEN}Cambios guardados correctamente en stash.{ENDC}")
            else:
                print(f"{YELLOW}Error al guardar en stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error en la operación de stash: {e}")

    elif choice == 1:  # Listar stashes
        try:
            result = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
            if result.stdout.strip():
                print("\nStashes guardados:")
                print(result.stdout)
            else:
                print("No hay stashes guardados.")
        except Exception as e:
            print(f"Error al listar stashes: {e}")

    elif choice in [2, 3]:  # Aplicar stash
        # Primero listar los stashes disponibles
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No hay stashes guardados.")
                return

            print("\nStashes disponibles:")
            print(stash_list)

            stash_index = input("\nIngresa el índice del stash (0 para el más reciente, 1 para el siguiente, etc.): ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Índice inválido. Operación cancelada.")
                return

            if choice == 2:  # Aplicar conservando
                result = subprocess.run(["git", "stash", "apply", stash_ref], capture_output=True, text=True)
                success_message = "Stash aplicado correctamente y conservado en la lista."
            else:  # choice == 3, apply and drop
                result = subprocess.run(["git", "stash", "pop", stash_ref], capture_output=True, text=True)
                success_message = "Stash aplicado correctamente y eliminado de la lista."

            if result.returncode == 0:
                print(f"{GREEN}{success_message}{ENDC}")
            else:
                print(f"{YELLOW}Error al aplicar stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error en la operación de stash: {e}")

    elif choice == 4:  # Eliminar stash específico
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No hay stashes guardados.")
                return

            print("\nStashes disponibles:")
            print(stash_list)

            stash_index = input("\nIngresa el índice del stash a eliminar: ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Índice inválido. Operación cancelada.")
                return

            confirm = input(f"{YELLOW}¿Estás seguro de que quieres eliminar este stash? Esta acción no se puede deshacer. (s/n): {ENDC}").lower()
            if confirm != "s":
                print("Operación cancelada.")
                return

            result = subprocess.run(["git", "stash", "drop", stash_ref], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{GREEN}Stash eliminado correctamente.{ENDC}")
            else:
                print(f"{YELLOW}Error al eliminar stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error en la operación de stash: {e}")

    elif choice == 5:  # Eliminar todos los stashes
        confirm = input(f"{YELLOW}¿Estás seguro de que quieres eliminar TODOS los stashes? Esta acción no se puede deshacer. (s/n): {ENDC}").lower()
        if confirm != "s":
            print("Operación cancelada.")
            return

        try:
            result = subprocess.run(["git", "stash", "clear"], capture_output=True, text=True)
            print(f"{GREEN}Todos los stashes han sido eliminados.{ENDC}")
        except Exception as e:
            print(f"Error al eliminar stashes: {e}")

    elif choice == 6:  # Volver atrás
        return

def cherry_pick_commits():
    print(f"\n{GREEN}Cherry-pick (seleccionar commits específicos){ENDC}")

    # Mostrar últimos commits para seleccionar
    print("\nÚltimos commits disponibles:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "20"])
    except Exception as e:
        print(f"Error al mostrar commits: {e}")
        return

    commit_hash = input("\nIngresa el hash del commit que quieres aplicar: ")
    if not commit_hash:
        print("Operación cancelada.")
        return

    # Opciones para el cherry-pick
    menu_options = [
        "Cherry-pick normal (crear nuevo commit)",
        "Cherry-pick sin crear commit (--no-commit)",
        "Cherry-pick y editar mensaje de commit (--edit)",
        "Volver al menú anterior"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Selecciona una opción:")
    choice = terminal_menu.show()

    if choice == 3:  # Volver atrás
        return

    # Preparar el comando según la opción
    cherry_pick_cmd = ["git", "cherry-pick"]
    if choice == 1:
        cherry_pick_cmd.append("--no-commit")
    elif choice == 2:
        cherry_pick_cmd.append("--edit")

    cherry_pick_cmd.append(commit_hash)

    # Ejecutar cherry-pick
    try:
        result = subprocess.run(cherry_pick_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{GREEN}Cherry-pick completado correctamente.{ENDC}")
            if choice == 1:
                print("Los cambios se han aplicado pero no se ha creado un commit. Puedes modificarlos y luego hacer commit.")
        else:
            print(f"{YELLOW}Error al hacer cherry-pick: {result.stderr.strip()}{ENDC}")

            # Ofrecer opciones en caso de conflicto
            if "conflict" in result.stderr:
                print("\nSe detectaron conflictos. Opciones disponibles:")
                conflict_options = [
                    "Continuar manualmente (resolver conflictos en el editor)",
                    "Abortar cherry-pick y volver al estado anterior",
                    "Volver al menú"
                ]

                conflict_menu = TerminalMenu(conflict_options, title="¿Qué deseas hacer?")
                conflict_choice = conflict_menu.show()

                if conflict_choice == 0:
                    print("Continúa resolviendo los conflictos manualmente en tu editor.")
                    print("Después de resolverlos, usa 'git add' para los archivos modificados y 'git cherry-pick --continue'.")
                elif conflict_choice == 1:
                    abort_result = subprocess.run(["git", "cherry-pick", "--abort"], capture_output=True, text=True)
                    if abort_result.returncode == 0:
                        print(f"{GREEN}Cherry-pick abortado. Se ha restaurado el estado anterior.{ENDC}")
                    else:
                        print(f"{YELLOW}Error al abortar cherry-pick: {abort_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error durante el cherry-pick: {e}")

def interactive_rebase():
    print(f"\n{GREEN}Rebase interactivo{ENDC}")
    print(f"{YELLOW}ADVERTENCIA: Esta operación reescribe el historial de commits.{ENDC}")

    # Mostrar últimos commits para referencia
    print("\nÚltimos commits:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
    except Exception as e:
        print(f"Error al mostrar commits: {e}")
        return

    # Opciones para el rebase
    print("\nEspecifica cuántos commits quieres incluir en el rebase:")
    print("1. Últimos N commits")
    print("2. Desde un commit específico")
    print("3. Volver al menú anterior")

    rebase_option = input("Selecciona una opción (1-3): ")

    if rebase_option == "3" or not rebase_option:
        return

    rebase_target = ""
    if rebase_option == "1":
        num_commits = input("¿Cuántos commits atrás? ")
        try:
            rebase_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Número inválido. Operación cancelada.")
            return
    elif rebase_option == "2":
        rebase_target = input("Ingresa el hash del commit base: ")
    else:
        print("Opción inválida. Operación cancelada.")
        return

    # Confirmación extra debido a la naturaleza destructiva
    confirm = input(f"{YELLOW}El rebase interactivo modificará el historial de commits. Esta operación puede causar problemas si los commits ya han sido compartidos. ¿Estás seguro? (s/n): {ENDC}").lower()
    if confirm != "s":
        print("Operación cancelada.")
        return

    # Ejecutar el rebase interactivo
    print("\nSe abrirá el editor para el rebase interactivo. Instrucciones:")
    print("- pick: mantener el commit como está")
    print("- reword: mantener el commit pero cambiar su mensaje")
    print("- edit: mantener el commit pero pausar para modificarlo")
    print("- squash: combinar con el commit anterior (mantiene ambos mensajes)")
    print("- fixup: combinar con el commit anterior (descarta su mensaje)")
    print("- drop: eliminar el commit")
    print("\nGuarda y cierra el editor para continuar con el rebase.")

    input("\nPresiona Enter para continuar...")

    try:
        # El flag -i indica rebase interactivo
        result = subprocess.run(["git", "rebase", "-i", rebase_target])

        # El resultado dependerá de la interacción del usuario con el editor
        if result.returncode == 0:
            print(f"{GREEN}Rebase interactivo completado correctamente.{ENDC}")
        else:
            print(f"{YELLOW}El rebase interactivo no completó correctamente. Puede que haya conflictos por resolver.{ENDC}")
    except Exception as e:
        print(f"Error durante el rebase interactivo: {e}")

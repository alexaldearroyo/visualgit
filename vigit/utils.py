import sys
import subprocess
import shutil

from enum import Enum

# COLORS
YELLOW = '\033[93m'
ORANGE = "\033[33m"
GREEN = '\033[92m'
BLUE = '\033[95m'
DARK_BLUE = '\033[34m'
RED = '\033[91m'
WHITE = '\033[97m'
CYAN = '\033[96m'
MAGENTA = '\033[35m'
ENDC = '\033[0m'

# STYLES
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BG_GREEN = '\033[42m'
BG_BLUE = '\033[44m'
BG_PURPLE = '\033[45m'
BLACK_TEXT = '\033[30m'
WHITE_TEXT = '\033[97m'

# GLOBAL MENU
class global_menu(Enum):
    CHECK_REMOTE = 'See Remote Repos'
    BACK = 'Back to previous menu'
    QUIT = 'Quit program'

# REPEATING CHOICES
def quit():
    sys.exit("Exiting VisualGit...\n")
def invalid_opt():
    print("Invalid choice. Please select a valid option.")

def run_git_diff(diff_args=None):
    """
    Ejecuta git diff usando diff-so-fancy si está disponible.

    Args:
        diff_args: Lista de argumentos adicionales para git diff
    """
    if diff_args is None:
        diff_args = []

    # Verificar si diff-so-fancy está instalado
    has_diff_so_fancy = shutil.which('diff-so-fancy') is not None

    base_cmd = ["git", "--no-pager", "diff", "--color=always"]
    base_cmd.extend(diff_args)

    try:
        if has_diff_so_fancy:
            process = subprocess.Popen(
                base_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )

            subprocess.run(
                ["diff-so-fancy"],
                stdin=process.stdout,
                check=True
            )

            process.stdout.close()
            process.wait()
        else:
            # Usar git diff normal si diff-so-fancy no está disponible
            subprocess.run(base_cmd, check=True)
    except Exception as e:
        print(f"Error executing git diff: {e}")

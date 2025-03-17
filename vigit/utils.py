import sys

from enum import Enum

# COLORS
YELLOW = '\033[93m'
GREEN = '\033[92m'
ENDC = '\033[0m'

# STYLES
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
BG_GREEN = '\033[42m'
BG_BLUE = '\033[44m'
BG_PURPLE = '\033[45m'
BLACK_TEXT = '\033[30m'

# GLOBAL MENU
class global_menu(Enum):
    CHECK_REMOTE = 'See Remote Repos'
    BACK = 'Go Back'
    QUIT = 'Quit'

# REPEATING CHOICES
def quit():
    sys.exit("Exiting VisualGit...\n")
def invalid_opt():
    print("Invalid choice. Please select a valid option.")

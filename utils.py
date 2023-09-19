import sys

from enum import Enum

# COLORS
YELLOW = '\033[93m'
GREEN = '\033[92m'
ENDC = '\033[0m'

# GLOBAL MENU
class global_menu(Enum):
    CHECK_REMOTE = 'cr'
    BACK = 'x'
    QUIT = 'q'

# REPEATING CHOICES
def quit():
    sys.exit("Exiting VisualGit...\n")
def invalid_opt():
    print("Invalid choice. Please select a valid option.")
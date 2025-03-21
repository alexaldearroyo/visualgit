import subprocess
import sys
import os

from simple_term_menu import TerminalMenu

from .utils import YELLOW, GREEN, ENDC, BOLD, BG_PURPLE, BLACK_TEXT, WHITE_TEXT
from .constants import branch_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .menu import commit_to_local_repo
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main
from .branx_local import branch_local, check_local_branches, create_local_branch, go_to_branch, go_to_main
from .branx_remote import branch_remote
from .branx_manage import manage_branches
from .advanced import advanced_operations

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def work_in_branches():
    if not is_git_repo():
        print_not_git_repo()
        return

    while True:
        current = current_branch()
        branch_display = f"{BLACK_TEXT}{BG_PURPLE}{BOLD} Currently on: {current} {ENDC}"
        print(f"\n{GREEN}Work in branches{ENDC} {branch_display}")

        menu_options = [
            f"[l] {branch_menu.BRANCH_LOCAL.value}",
            f"[r] {branch_menu.BRANCH_REMOTE.value}",
            f"[m] {branch_menu.MANAGE_BRANCHES.value}",
            f"[a] Advanced operations",
            f"[x] Back to main menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Please select an option:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            branch_local()
        elif menu_entry_index == 1:
            branch_remote()
        elif menu_entry_index == 2:
            manage_branches()
        elif menu_entry_index == 3:
            advanced_operations()
        elif menu_entry_index == 4:
            clear_screen()
            break
        elif menu_entry_index == 5:
            sys.exit("Exiting VisualGit...\n")

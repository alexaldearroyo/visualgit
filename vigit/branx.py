import subprocess
import sys
import os

from simple_term_menu import TerminalMenu

from .utils import YELLOW, GREEN, ENDC
from .constants import branch_menu
from .mainm import commit_to_local_repo
from .checks import is_git_repo, print_not_git_repo, current_branch, is_local_branch_connected_to_remote, has_commits, print_not_commits, is_current_branch_main
from .branx_local import branch_local
from .branx_ltr import branch_local_to_remote
from .branx_rtl import branch_remote_to_local
from .branx_manage import manage_branches
from .advanced import advanced_operations

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def work_in_branches():
    current = current_branch()
    while True:
        print(f"\n{GREEN}Work in branches{ENDC} (Currently on: {current}):")

        menu_options = [
            f"[l] {branch_menu.BRANCH_LOCAL.value}",
            f"[t] {branch_menu.BRANCH_LOCAL_TO_REMOTE.value}",
            f"[r] {branch_menu.BRANCH_REMOTE_TO_LOCAL.value}",
            f"[m] {branch_menu.MANAGE_BRANCHES.value}",
            f"[a] Advanced operations",
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

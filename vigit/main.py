#!/usr/bin/env python3

import subprocess
import sys
import argparse
import os
import warnings

# Filtrar advertencias de urllib3 relacionadas con SSL
warnings.filterwarnings("ignore", category=Warning, module="urllib3")

from enum import Enum
from simple_term_menu import TerminalMenu

from .utils import BG_BLUE, YELLOW, GREEN, ENDC, BOLD, BG_PURPLE, BLACK_TEXT, WHITE_TEXT
from .constants import start_menu, main_menu, main_local_menu, main_remote_menu, branch_local_menu, branch_remote_menu, manage_branch_menu, updated_start_menu, MENU_CURSOR, MENU_CURSOR_STYLE, show_menu
from .checks import is_git_installed, is_git_repo, print_not_git_repo, current_branch, get_current_branch, is_current_branch_main
from .menu import work_in_main, create_local_repo, commit_to_local_repo, commit_and_push, main_local, main_remote, check_local_repos, create_remote_repo, show_menu_options, show_status_long
from .branx_local import go_to_branch, go_to_main, create_local_branch
from .branx_remote import commit_and_push_in_branch, push_changes_to_remote_branch, create_remote_branch
from .branx_manage import merge_branches, manage_branches, merge_with_main, merge_with_selected_branch
from .branx import work_in_branches
from .advanced import advanced_operations
from .config import configuration


def handle_args():
    parser = argparse.ArgumentParser(description="Visual Git Command Line Tool")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: vg a (add repo)
    add_parser = subparsers.add_parser('a', help='Quick action: Add a local repo')

    # Command: vg ar (add remote repo)
    ar_parser = subparsers.add_parser('ar', help='Quick action: Add repo to remote')

    # Command: vg b (add-branch)
    b_parser = subparsers.add_parser('b', help='Quick action: Add a local branch')

    # Command: vg br (branch to remote)
    br_parser = subparsers.add_parser('br', help='Quick action: Create a branch directly on remote')

    # Command: vg c (commit)
    c_parser = subparsers.add_parser('c', help='Quick action: Commit to local repo')
    c_parser.add_argument('message', nargs='?', help='Commit message')

    # Command: vg p (commit-push-main)
    p_parser = subparsers.add_parser('p', help='Quick action: Commit & Push in current branch')
    p_parser.add_argument('message', nargs='?', help='Commit message')

    # Command: vg f (merge/fusion)
    f_parser = subparsers.add_parser('f', help='Quick action: Merge branch with main')

    # Command: vg g (goto branch)
    g_parser = subparsers.add_parser('g', help='Quick action: Go to a different branch')

    # Command: vg m (merge with main)
    m_parser = subparsers.add_parser('m', help='Quick action: Merge current branch with main')

    # Command: vg mo (merge with main - alternative)
    mo_parser = subparsers.add_parser('mo', help='Quick action: Merge current branch with main')

    # Command: vg mb (merge with branch)
    mb_parser = subparsers.add_parser('mb', help='Quick action: Merge current branch with selected branch')

    # Command: vg n (new configuration)
    n_parser = subparsers.add_parser('n', help='Quick action: New Configuration')

    # Command: vg s (see log)
    s_parser = subparsers.add_parser('s', help='Quick action: See log')

    # Command: vg v (general view)
    v_parser = subparsers.add_parser('v', help='Quick action: General View')

    return parser.parse_args()


# TITLE
print("VISUAL GIT")
print("-" * 30)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def main():
    args = handle_args()

    # Handle subcommands
    if hasattr(args, 'command') and args.command:
        if args.command == 'a':
            create_local_repo()
            return
        elif args.command == 'ar':
            create_remote_repo()
            return
        elif args.command == 'b':
            create_local_branch()
            return
        elif args.command == 'br':
            create_remote_branch()
            return
        elif args.command == 'c':
            commit_to_local_repo(args.message if hasattr(args, 'message') and args.message else None)
            return
        elif args.command == 'p':
            commit_and_push(args.message if hasattr(args, 'message') and args.message else None)
            return
        elif args.command == 'f':
            merge_branches()
            return
        elif args.command == 'g':
            go_to_branch()
            return
        elif args.command == 'm':
            merge_with_main()
            return
        elif args.command == 'mo':
            merge_with_main()
            return
        elif args.command == 'mb':
            merge_with_selected_branch()
            return
        elif args.command == 'n':
            configuration()
            return
        elif args.command == 's':
            check_log()
            return
        elif args.command == 'v':
            check_local_repos()
            return

    if not is_git_installed():
        print("Git is not installed. You need to install git to use VisualGit.")
        return

    while True:
        current = current_branch()
        this_branch = get_current_branch()
        if is_git_repo() and this_branch:
            branch_display = f"{BLACK_TEXT}{BG_PURPLE}{BOLD} Currently on: {this_branch} {ENDC}"
            print(branch_display)
        elif is_git_repo():
            branch_display = f"{BLACK_TEXT}{BG_PURPLE}{BOLD} Currently on: {current} {ENDC}"
            print(branch_display)

        menu_options = [
            f"[v] {updated_start_menu.WATCH_STATUS.value}",
            f"[l] {updated_start_menu.LOCAL.value}",
            f"[r] {updated_start_menu.REMOTE.value}",
            f"[b] {updated_start_menu.MANAGE_BRANCHES.value}",
            f"[o] {updated_start_menu.ADVANCED_OPERATIONS.value}",
            f"[n] {updated_start_menu.CONFIGURATION.value}",
            f"[x] {updated_start_menu.QUICK_ACTIONS.value}",
            f"[s] {show_menu.SHOW.value}",
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
            # See Current Status
            if is_git_repo():
                check_local_repos()
            else:
                print_not_git_repo()

        elif menu_entry_index == 1:
            # Local

            main_local()
        elif menu_entry_index == 2:
            # Remote
            if is_git_repo():
                main_remote()
            else:
                print_not_git_repo()
        elif menu_entry_index == 3:
            # Manage Branches
            if is_git_repo():
                manage_branches()
            else:
                print_not_git_repo()
        elif menu_entry_index == 4:
            # Advanced Operations
            if is_git_repo():
                advanced_operations()
            else:
                print_not_git_repo()
        elif menu_entry_index == 5:
            # New Configuration
            configuration()
        elif menu_entry_index == 6:
            # Quick Actions
            quick_actions()
        elif menu_entry_index == 7:
            # Show
            show_menu_options()
        elif menu_entry_index == 8:
            quit()


def check_log():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        subprocess.run(["git", "log", "--oneline"])
    except Exception as e:
        print(f"Error checking log: {e}")


def quick_actions():
    while True:

        print(f"{GREEN}Quick Actions:{ENDC}")

        menu_options = [
            f"[a] {main_local_menu.ADD_LOCAL.value}",
            f"[c] {main_local_menu.COMMIT_LOCAL.value}",
            f"[p] {main_remote_menu.COMMIT_AND_PUSH.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {manage_branch_menu.MERGE.value}",
            "[x] Back to previous menu",
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
            create_local_repo()
        elif menu_entry_index == 1:
            commit_to_local_repo()
        elif menu_entry_index == 2:
            commit_and_push()
        elif menu_entry_index == 3:
            go_to_branch()
        elif menu_entry_index == 4:
            merge_branches()

        elif menu_entry_index == 5:
            clear_screen()
            break
        elif menu_entry_index == 6:
            quit()


def invalid_opt():
    print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

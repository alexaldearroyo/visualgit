#!/usr/bin/env python3

import subprocess
import sys
import argparse
import os

from enum import Enum
from simple_term_menu import TerminalMenu

from .utils import YELLOW, GREEN, ENDC, BOLD, BG_PURPLE, BLACK_TEXT
from .constants import start_menu, main_menu, main_local_menu, main_remote_menu, branch_local_menu, branch_remote_menu, manage_branch_menu, updated_start_menu
from .checks import is_git_installed, is_git_repo, print_not_git_repo, current_branch, get_current_branch, is_current_branch_main
from .mainm import work_in_main, create_local_repo, commit_to_local_repo, commit_and_push, main_local, main_remote, check_local_repos
from .branx_local import go_to_branch, go_to_main, create_local_branch
from .branx_remote import commit_and_push_in_branch
from .branx_manage import merge_branch_with_main, manage_branches
from .branx import work_in_branches
from .advanced import advanced_operations
from .config import configuration


def handle_args():
    parser = argparse.ArgumentParser(description="Visual Git Command Line Tool")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: vg a (add repo)
    add_parser = subparsers.add_parser('a', help='Quick action: Add a local repo')

    # Command: vg b (add-branch)
    b_parser = subparsers.add_parser('b', help='Quick action: Add a local branch')

    # Command: vg c (commit)
    c_parser = subparsers.add_parser('c', help='Quick action: Commit to local repo')

    # Command: vg p (commit-push-main)
    p_parser = subparsers.add_parser('p', help='Quick action: Commit & Push in main')

    # Command: vg f (merge/fusion)
    f_parser = subparsers.add_parser('f', help='Quick action: Merge branch with main')

    # Command: vg n (new configuration)
    n_parser = subparsers.add_parser('n', help='Quick action: New Configuration')

    # Command: vg s (see log)
    s_parser = subparsers.add_parser('s', help='Quick action: See log')

    # Maintain compatibility with previous options
    parser.add_argument("-a", "--add", action="store_true", help="Quick action: Add a local repo")
    parser.add_argument("-b", "--add-branch", action="store_true", help="Quick action: Add a local branch")
    parser.add_argument("-c", "--commit", action="store_true", help="Quick action: Commit to local repo")
    parser.add_argument("-p", "--commit-push-main", action="store_true", help="Quick action: Commit & Push in main")
    parser.add_argument("-f", "--merge", "--fusion", action="store_true", help="Quick action: Merge branch with main")
    parser.add_argument("-n", "--new", action="store_true", help="Quick action: New Configuration")
    parser.add_argument("-s", "--see", action="store_true", help="Quick action: See log")

    return parser.parse_args()


# TITLE
print("\nVISUAL GIT")
print("-" * 30)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

def main():
    args = handle_args()

    # Handle subcommands
    if hasattr(args, 'command') and args.command:
        if args.command == 'add':
            create_local_repo()
            return
        elif args.command == 'b':
            create_local_branch()
            return
        elif args.command == 'c':
            commit_to_local_repo()
            return
        elif args.command == 'p':
            commit_and_push()
            return
        elif args.command == 'f':
            merge_branch_with_main()
            return
        elif args.command == 'n':
            configuration()
            return
        elif args.command == 's':
            # check_log()
            return

    # Handle traditional options with dashes (for compatibility)
    if args.add:
        create_local_repo()
        return
    if args.add_branch:
        create_local_branch()
        return
    if args.commit:
        commit_to_local_repo()
        return
    if args.commit_push_main:
        commit_and_push()
        return
    if args.merge:
        merge_branch_with_main()
        return
    if args.new:
        configuration()
        return
    if args.see:
        # check_log()
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
            f"[s] {updated_start_menu.WATCH_STATUS.value}",
            f"[l] {updated_start_menu.LOCAL.value}",
            f"[r] {updated_start_menu.REMOTE.value}",
            f"[b] {updated_start_menu.MANAGE_BRANCHES.value}",
            f"[o] {updated_start_menu.ADVANCED_OPERATIONS.value}",
            f"[n] {updated_start_menu.CONFIGURATION.value}",
            f"[x] {updated_start_menu.QUICK_ACTIONS.value}",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
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
        print(f"\n{GREEN}Quick Actions:{ENDC}")

        menu_options = [
            f"[a] {main_local_menu.ADD_LOCAL.value}",
            f"[c] {main_local_menu.COMMIT_LOCAL.value}",
            f"[p] {main_remote_menu.COMMIT_AND_PUSH.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {manage_branch_menu.MERGE.value}",
            "[x] Back to previous menu",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
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
            merge_branch_with_main()

        elif menu_entry_index == 5:
            clear_screen()
            break
        elif menu_entry_index == 6:
            quit()


def invalid_opt():
    print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

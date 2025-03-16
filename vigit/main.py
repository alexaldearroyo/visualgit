#!/usr/bin/env python3

import subprocess
import sys
import argparse
import os

from enum import Enum
from simple_term_menu import TerminalMenu

from .utils import YELLOW, GREEN, ENDC
from .constants import start_menu, main_menu, main_local_menu, main_lr_menu, branch_local_menu, branch_lr_menu, manage_branch_menu
from .checks import is_git_installed, is_git_repo, print_not_git_repo, current_branch, get_current_branch, is_current_branch_main
from .mainm import work_in_main, create_local_repo, commit_to_local_repo, commit_and_push
from .branx_local import go_to_branch, go_to_main, create_local_branch
from .branx_ltr import commit_and_push_in_branch
from .branx_manage import merge_branch_with_main
from .branx import work_in_branches
from .config import configuration


def handle_args():
    parser = argparse.ArgumentParser(description="Visual Git Command Line Tool")

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Command: vg a (add repo)
    add_parser = subparsers.add_parser('a', help='Quick action: Add a local repo')

    # Command: vg ab (add-branch)
    ab_parser = subparsers.add_parser('ab', help='Quick action: Add a local branch')

    # Command: vg c (commit)
    c_parser = subparsers.add_parser('c', help='Quick action: Commit to local repo')

    # Command: vg cp (commit-push-main)
    cp_parser = subparsers.add_parser('cp', help='Quick action: Commit & Push in main')

    # Command: vg cb (commit-push-branch)
    cb_parser = subparsers.add_parser('cb', help='Quick action: Commit & Push in branch')

    # Command: vg o (merge/one)
    o_parser = subparsers.add_parser('o', help='Quick action: Merge branch with main')

    # Command: vg n (new configuration)
    n_parser = subparsers.add_parser('n', help='Quick action: New Configuration')

    # Command: vg s (see log)
    s_parser = subparsers.add_parser('s', help='Quick action: See log')

    # Maintain compatibility with previous options
    parser.add_argument("-a", "--add", action="store_true", help="Quick action: Add a local repo")
    parser.add_argument("-ab", "--add-branch", action="store_true", help="Quick action: Add a local branch")
    parser.add_argument("-c", "--commit", action="store_true", help="Quick action: Commit to local repo")
    parser.add_argument("-cp", "--commit-push-main", action="store_true", help="Quick action: Commit & Push in main")
    parser.add_argument("-cb", "--commit-push-branch", action="store_true", help="Quick action: Commit & Push in branch")
    parser.add_argument("-o", "--merge", "--one", action="store_true", help="Quick action: Merge branch with main")
    parser.add_argument("-n", "--new", action="store_true", help="Quick action: New Configuration")
    parser.add_argument("-s", "--see", action="store_true", help="Quick action: See log")

    return parser.parse_args()


# TITLE
this_branch = get_current_branch()
print("\nVISUAL GIT")
print("-" * 30)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\nVISUAL GIT")
    print("-" * 30)

class start_menu(Enum):
    WORK_IN_MAIN = "Work in Main"
    WORK_IN_BRANCHES = "Work in Branches"
    CHECK_LOG = "See Log"
    CONFIGURATION = "New Configuration"
    QUICK_ACTIONS = "Quick Actions"


def main():
    args = handle_args()

    # Manejar los subcomandos
    if hasattr(args, 'command') and args.command:
        if args.command == 'add':
            create_local_repo()
            return
        elif args.command == 'ab':
            create_local_branch()
            return
        elif args.command == 'c':
            commit_to_local_repo()
            return
        elif args.command == 'cp':
            commit_and_push()
            return
        elif args.command == 'cb':
            commit_and_push_in_branch()
            return
        elif args.command == 'o':
            merge_branch_with_main()
            return
        elif args.command == 'n':
            configuration()
            return
        elif args.command == 's':
            check_log()
            return

    # Manejar las opciones tradicionales con guiones (para compatibilidad)
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
    if args.commit_push_branch:
        commit_and_push_in_branch()
        return
    if args.merge:
        merge_branch_with_main()
        return
    if args.new:
        configuration()
        return
    if args.see:
        check_log()
        return

    if not is_git_installed():
        print("Git is not installed. You need to install git to use VisualGit.")
        return

    current = current_branch()

    while True:
        if is_git_repo() and this_branch:
            print(f"{GREEN}Currently on: {this_branch}{ENDC}")
        elif is_git_repo():
            print((f"{GREEN}Currently on: {current}{ENDC}"))

        menu_options = [
            f"[m] {start_menu.WORK_IN_MAIN.value}",
            f"[b] {start_menu.WORK_IN_BRANCHES.value}",
            f"[s] {start_menu.CHECK_LOG.value}",
            f"[n] {start_menu.CONFIGURATION.value}",
            f"[x] {start_menu.QUICK_ACTIONS.value}",
            "[q] Quit program"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Please select an option:")
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            if not is_git_repo():
                work_in_main()
            elif is_git_repo and not is_current_branch_main():
                print(
                    f"\n{YELLOW}You are not in main. Go to main to proceed.{ENDC}\nTo go to main: Quick actions -> Go to main"
                )
            else:
                work_in_main()
        elif menu_entry_index == 1:
            if is_git_repo():
                work_in_branches()
            else:
                print_not_git_repo()
        elif menu_entry_index == 2:
            check_log()
        elif menu_entry_index == 3:
            configuration()
        elif menu_entry_index == 4:
            quick_actions()
        elif menu_entry_index == 5:
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
            f"[p] {main_lr_menu.COMMIT_AND_PUSH.value}",
            f"[b] {branch_lr_menu.COMMIT_PUSH_BRANCH.value}",
            f"[o] {manage_branch_menu.MERGE.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {branch_local_menu.GOTO_MAIN.value}",
            f"[x] Back to previous menu",
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
            commit_and_push_in_branch()
        elif menu_entry_index == 4:
            merge_branch_with_main()
        elif menu_entry_index == 5:
            go_to_branch()
        elif menu_entry_index == 6:
            go_to_main()
        elif menu_entry_index == 7:
            clear_screen()
            break
        elif menu_entry_index == 8:
            quit()

if __name__ == "__main__":
    main()

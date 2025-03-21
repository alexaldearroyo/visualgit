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
from .constants import start_menu, main_menu, main_local_menu, main_remote_menu, branch_local_menu, branch_remote_menu, manage_branch_menu, updated_start_menu, MENU_CURSOR, MENU_CURSOR_STYLE, show_menu, add_menu
from .checks import is_git_installed, is_git_repo, print_not_git_repo, current_branch, get_current_branch, is_current_branch_main
from .menu import work_in_main, create_local_repo, commit_to_local_repo, commit_and_push, main_local, main_remote, create_remote_repo
from .show_menu import show_menu_options, show_status_long, general_view, show_detailed_history, show_expanded_history, show_tracking_history, show_differences_history, show_local_repo, show_remote_repo, show_branches, show_differences_non_staged, show_differences_staged, show_differences_between_commits, show_differences_between_branches
from .branx_local import go_to_branch, go_to_main, create_local_branch
from .branx_remote import commit_and_push_in_branch, push_changes_to_remote_branch, create_remote_branch
from .branx_manage import merge_branches, manage_branches, merge_with_main, merge_with_selected_branch
from .branx import work_in_branches
from .advanced import advanced_operations
from .config import configuration
from .add_menu import add_menu_options, add_tracked_files


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
    s_parser = subparsers.add_parser('s', help='Quick action: See detailed status')

    # Command: vg ss (same as s)
    ss_parser = subparsers.add_parser('ss', help='Quick action: See detailed status (alias of s)')

    # Command: vg v (general view)
    v_parser = subparsers.add_parser('v', help='Quick action: General View')

    # Command: vg sv (same as v)
    sv_parser = subparsers.add_parser('sv', help='Quick action: General View (alias of v)')

    # Command: vg sd (diff non-staged)
    sd_parser = subparsers.add_parser('sd', help='Quick action: Show differences of non staged files')

    # Command: vg sdd (same as sd)
    sdd_parser = subparsers.add_parser('sdd', help='Quick action: Show differences of non staged files (alias of sd)')

    # Command: vg sda (diff staged/added)
    sda_parser = subparsers.add_parser('sda', help='Quick action: Show differences of added files')

    # Command: vg sdc (diff between commits)
    sdc_parser = subparsers.add_parser('sdc', help='Quick action: Show differences between commits')

    # Command: vg sdb (diff between branches)
    sdb_parser = subparsers.add_parser('sdb', help='Quick action: Show differences between branches')

    # Command: vg h (history)
    h_parser = subparsers.add_parser('h', help='Quick action: Show commit history')

    # Command: vg sh (same as h)
    sh_parser = subparsers.add_parser('sh', help='Quick action: Show commit history (alias of h)')

    # Command: vg shh (same as h)
    shh_parser = subparsers.add_parser('shh', help='Quick action: Show commit history (alias of h)')

    # Command: vg sc (same as h)
    sc_parser = subparsers.add_parser('sc', help='Quick action: Show commit history (alias of h)')

    # Command: vg shx (expanded history)
    shx_parser = subparsers.add_parser('shx', help='Quick action: Show expanded history')

    # Command: vg sx (same as shx)
    sx_parser = subparsers.add_parser('sx', help='Quick action: Show expanded history (alias of shx)')

    # Command: vg hx (same as shx)
    hx_parser = subparsers.add_parser('hx', help='Quick action: Show expanded history (alias of shx)')

    # Command: vg sht (tracking history)
    sht_parser = subparsers.add_parser('sht', help='Quick action: Show tracking history')

    # Command: vg st (same as sht)
    st_parser = subparsers.add_parser('st', help='Quick action: Show tracking history (alias of sht)')

    # Command: vg ht (same as sht)
    ht_parser = subparsers.add_parser('ht', help='Quick action: Show tracking history (alias of sht)')

    # Command: vg shd (differences history)
    shd_parser = subparsers.add_parser('shd', help='Quick action: Show differences history')

    # Command: vg hd (same as shd)
    hd_parser = subparsers.add_parser('hd', help='Quick action: Show differences history (alias of shd)')

    # Command: vg sl (local repo)
    sl_parser = subparsers.add_parser('sl', help='Quick action: Show local repo')

    # Command: vg l (same as sl)
    l_parser = subparsers.add_parser('l', help='Quick action: Show local repo (alias of sl)')

    # Command: vg sr (remote repo)
    sr_parser = subparsers.add_parser('sr', help='Quick action: Show remote repo')

    # Command: vg r (same as sr)
    r_parser = subparsers.add_parser('r', help='Quick action: Show remote repo (alias of sr)')

    # Command: vg sb (branches)
    sb_parser = subparsers.add_parser('sb', help='Quick action: Show branches')

    # Command: vg at (add tracked files)
    at_parser = subparsers.add_parser('at', help='Quick action: Add tracked files')

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
        elif args.command == 's' or args.command == 'ss':
            show_status_long()
            return
        elif args.command == 'v' or args.command == 'sv':
            general_view()
            return
        elif args.command == 'sd' or args.command == 'sdd':
            show_differences_non_staged(ask_for_enter=False)
            return
        elif args.command == 'sda':
            show_differences_staged(ask_for_enter=False)
            return
        elif args.command == 'sdc':
            show_differences_between_commits(ask_for_enter=False)
            return
        elif args.command == 'sdb':
            show_differences_between_branches(ask_for_enter=False)
            return
        elif args.command == 'h' or args.command == 'sh' or args.command == 'shh' or args.command == 'sc':
            show_detailed_history(ask_for_enter=False)
            return
        elif args.command == 'shx' or args.command == 'sx' or args.command == 'hx':
            show_expanded_history(ask_for_enter=False)
            return
        elif args.command == 'sht' or args.command == 'st' or args.command == 'ht':
            show_tracking_history(ask_for_enter=False)
            return
        elif args.command == 'shd' or args.command == 'hd':
            show_differences_history(ask_for_enter=False)
            return
        elif args.command == 'sl' or args.command == 'l':
            show_local_repo(ask_for_enter=False)
            return
        elif args.command == 'sr' or args.command == 'r':
            show_remote_repo(ask_for_enter=False)
            return
        elif args.command == 'sb':
            show_branches(ask_for_enter=False)
            return
        elif args.command == 'at':
            add_tracked_files(ask_for_enter=False)
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
            f"[l] {updated_start_menu.LOCAL.value}",
            f"[r] {updated_start_menu.REMOTE.value}",
            f"[b] {updated_start_menu.MANAGE_BRANCHES.value}",
            f"[o] {updated_start_menu.ADVANCED_OPERATIONS.value}",
            f"[n] {updated_start_menu.CONFIGURATION.value}",
            f"[x] {updated_start_menu.QUICK_ACTIONS.value}",
            f"[s] {show_menu.SHOW.value}",
            f"[a] {add_menu.ADD.value}",
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
            # Local
            main_local()
        elif menu_entry_index == 1:
            # Remote
            if is_git_repo():
                main_remote()
            else:
                print_not_git_repo()
        elif menu_entry_index == 2:
            # Manage Branches
            if is_git_repo():
                manage_branches()
            else:
                print_not_git_repo()
        elif menu_entry_index == 3:
            # Advanced Operations
            if is_git_repo():
                advanced_operations()
            else:
                print_not_git_repo()
        elif menu_entry_index == 4:
            # New Configuration
            configuration()
        elif menu_entry_index == 5:
            # Quick Actions
            quick_actions()
        elif menu_entry_index == 6:
            # Show
            show_menu_options()
        elif menu_entry_index == 7:
            # Add
            if is_git_repo():
                add_menu_options()
            else:
                print_not_git_repo()
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

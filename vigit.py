#!/usr/bin/env python3

import subprocess
import sys
import argparse


from enum import Enum

from utils import *
from checks import *
from mainm import *
from branx import *
from config import *


def handle_args():
    parser = argparse.ArgumentParser(description='Visual Git Command Line Tool')

    parser.add_argument('-a', '--create-local-repo', action='store_true', help='Quick action: Add a local repo')
    parser.add_argument('-cp', '--commit-push-main', action='store_true', help='Quick action: Commit & Push in main')
    parser.add_argument('-cb', '--commit-push-branch', action='store_true', help='Quick action: Commit & Push in branch')
    parser.add_argument('-m', '--merge-branch-with-main', action='store_true', help='Quick action: Merge branch with main')
    
    return parser.parse_args()


# TITLE
this_branch = get_current_branch()
print("\nVISUAL GIT")
print("-"*30)


class start_menu(Enum):
    WORK_IN_MAIN = 'm'
    WORK_IN_BRANCHES = 'b'
    CHECK_LOG = 'l'
    CONFIGURATION = 'c'
    QUICK_ACTIONS = 'a'

def main():
    args = handle_args()

    if getattr(args, 'a', False):
        create_local_repo()
    if getattr(args, 'cp', False):
        commit_and_push()
        sys.exit()
    if getattr(args, 'cb', False):
        commit_and_push_in_branch()
        sys.exit()
    if getattr(args, 'm', False):
        merge_branch_with_main()


    if not is_git_installed():
        print("Git is not installed. You need to install git to use VisualGit.")
        return
    
    current = current_branch()

    while True:
        if is_git_repo() and this_branch:
            print(f"\n{GREEN}Currently on: {this_branch}{ENDC}")
        elif is_git_repo():
            print((f"\n{GREEN}Currently on: {current}{ENDC}"))
        print("\n[m] Work in main")
        print("[b] Work in branches")
        print("[l] Check log")
        print("[c] Configuration")
        print("[a] Quick actions")
        print("[q] Quit program\n")

        choice = input("Please select an option: ")

        if choice == start_menu.WORK_IN_MAIN.value:
            
            if not is_git_repo():
                work_in_main()
            elif is_git_repo and not is_current_branch_main():
                print(f"\n{YELLOW}You are not in main. Go to main to proceed.{ENDC}\nTo go to main: Quick actions -> Go to main")
            else:
                work_in_main()
        elif choice == start_menu.WORK_IN_BRANCHES.value:
            if is_git_repo():
                work_in_branches()
            else:
                print_not_git_repo()
        elif choice == start_menu.CHECK_LOG.value:
            check_log()
        elif choice == start_menu.CONFIGURATION.value:
            configuration()
        elif choice == start_menu.QUICK_ACTIONS.value:
            quick_actions()
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()
            


def check_log():
    subprocess.run(["git", "log"])


def quick_actions():
    while True:
        print(f"\n{GREEN}Quick Actions:{ENDC}")
        print("[a] Add a local repo")
        print("[c] Commit to local repo")
        print("[cp] Commit & Push in main")
        print("[cb] Commit & Push in branch")
        print("[m] Merge branch with main")
        print("[g] Go to branch")
        print("[gm] Go to main")
        print("[x] Back to main menu")
        print("[q] Quit program")

        choice = input("\nPlease select an option: ")

        if choice == main_local_menu.ADD_LOCAL.value:
            create_local_repo()
        elif choice == main_local_menu.COMMIT_LOCAL.value:
            commit_to_local_repo()
        elif choice == main_lr_menu.COMMIT_AND_PUSH.value:
            commit_and_push()
        elif choice == branch_lr_menu.COMMIT_PUSH_BRANCH.value:
            commit_and_push_in_branch()
        elif choice == branch_lr_menu.COMMIT_PUSH_BRANCH.value:
            commit_and_push_in_branch()
        elif choice == manage_branch_menu.MERGE.value:
            merge_branch_with_main()
        elif choice == branch_local_menu.GOTO_BRANCH.value:
            go_to_branch()
        elif choice == branch_local_menu.GOTO_MAIN.value:
            go_to_main()
        elif choice == global_menu.BACK.value:
            break
        elif choice == global_menu.QUIT.value:
            quit()
        else:
            invalid_opt()


if __name__ == "__main__":
    main()
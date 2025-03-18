from enum import Enum

import os
import subprocess
import json
import time
from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC, BOLD, BG_PURPLE, BLACK_TEXT, WHITE_TEXT, BG_BLUE
from .constants import manage_branch_menu, branch_remote_menu, branch_local_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo, current_branch, get_current_branch, has_commits, print_not_commits, is_current_branch_main, is_connected_to_remote, print_not_connected_to_remote
from .branx_local import go_to_branch, go_to_main, create_local_branch
from .branx_remote import check_remote_branches, connect_local_branch_with_remote
from .menu import clear_screen

def handle_uncommitted_changes(target_branch):
    """
    Handle uncommitted changes when switching branches fails.
    Returns True if the switch was successful after handling changes, False otherwise.
    """
    commit_choice = input(f"\nDo you want to commit your changes before switching branches? (y/n): ").lower()

    if commit_choice == 'y' or commit_choice == 's':
        # Commit the changes
        commit_msg = input(f"\nCommit message: ")

        # Add all changes
        add_result = subprocess.run(
            ["git", "add", "."],
            capture_output=True,
            text=True
        )

        if add_result.returncode != 0:
            print(f"{YELLOW}Error adding changes: {add_result.stderr.strip()}{ENDC}")
            return False

        # Commit
        commit_result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True,
            text=True
        )

        if commit_result.returncode != 0:
            print(f"{YELLOW}Error committing changes: {commit_result.stderr.strip()}{ENDC}")
            return False

        print(f"{GREEN}Commit successful.{ENDC}")

        # Try to switch to the branch again
        checkout_result = subprocess.run(
            ["git", "checkout", target_branch],
            capture_output=True,
            text=True
        )

        if checkout_result.returncode != 0:
            print(f"{YELLOW}Still unable to switch to branch {target_branch}: {checkout_result.stderr.strip()}{ENDC}")
            return False

        print(f"{GREEN}Successfully switched to branch {target_branch}.{ENDC}")
        return True
    else:
        print(f"{YELLOW}Operation canceled. You must commit or stash your changes before switching branches.{ENDC}")
        return False

def merge_with_main():
    """Merge the current branch with main automatically"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Get current branch
        source_branch = current_branch()

        # Define the target branch (main)
        target_branch = "main"

        # Make sure source and target are different
        if source_branch == target_branch:
            print(f"{YELLOW}You are already on {target_branch}. No merge needed.{ENDC}")
            return

        print(f"\n{GREEN}Merging current branch '{source_branch}' into '{target_branch}'...{ENDC}")

        # Save the current branch name to return later
        original_branch = source_branch

        # Switch to target branch (main)
        checkout_result = subprocess.run(
            ["git", "checkout", target_branch],
            capture_output=True,
            text=True
        )

        if checkout_result.returncode != 0:
            print(f"{YELLOW}Could not switch to branch {target_branch}: {checkout_result.stderr.strip()}{ENDC}")

            # Check for uncommitted changes
            if "local changes" in checkout_result.stderr or "cambios locales" in checkout_result.stderr:
                if not handle_uncommitted_changes(target_branch):
                    return
            else:
                return

        # Perform the merge
        merge_result = subprocess.run(
            ["git", "merge", source_branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # Check merge result
        if merge_result.returncode == 0:
            print(f"{GREEN}Branch '{source_branch}' successfully merged into '{target_branch}'.{ENDC}")

            # Ask if user wants to go back to original branch
            go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
            if go_back == 'y':
                subprocess.run(["git", "checkout", original_branch])
                print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
        else:
            # Handle merge conflicts
            print(f"{YELLOW}Could not merge branch '{source_branch}' into '{target_branch}'.{ENDC}")
            print(f"Reason: {merge_result.stderr.strip()}")

            # Offer conflict resolution options
            print("\nAvailable options:")
            print(f"1. Force merge ('ours' strategy - prioritizes {target_branch} changes)")
            print(f"2. Force merge ('theirs' strategy - prioritizes {source_branch} changes)")
            print("3. Cancel operation")

            choice = input("\nSelect an option (1-3): ")

            if choice == "1":
                # Use "ours" strategy (keep target/main changes)
                ours_result = subprocess.run(
                    ["git", "merge", "-X", "ours", source_branch],
                    capture_output=True,
                    text=True
                )

                if ours_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Changes from '{target_branch}' have been prioritized.{ENDC}")

                    # Ask about returning to original branch
                    go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
                    if go_back == 'y':
                        subprocess.run(["git", "checkout", original_branch])
                        print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {ours_result.stderr.strip()}{ENDC}")
                    # Return to original branch
                    subprocess.run(["git", "checkout", original_branch])
                    print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

            elif choice == "2":
                # Use "theirs" strategy (keep source branch changes)
                theirs_result = subprocess.run(
                    ["git", "merge", "-X", "theirs", source_branch],
                    capture_output=True,
                    text=True
                )

                if theirs_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Changes from '{source_branch}' have been prioritized.{ENDC}")

                    # Ask about returning to original branch
                    go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
                    if go_back == 'y':
                        subprocess.run(["git", "checkout", original_branch])
                        print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {theirs_result.stderr.strip()}{ENDC}")
                    # Return to original branch
                    subprocess.run(["git", "checkout", original_branch])
                    print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

            else:
                print("Merge operation canceled.")
                # Return to original branch
                subprocess.run(["git", "checkout", original_branch])
                print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

    except Exception as e:
        print(f"Error merging branches: {e}")
        # Try to return to the original branch in case of error
        try:
            original_branch = source_branch
            subprocess.run(["git", "checkout", original_branch])
            print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
        except:
            pass

def merge_with_selected_branch():
    """Merge the current branch with a selected branch"""
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Get current branch
        source_branch = current_branch()

        # Get all available branches
        result = subprocess.run(["git", "branch"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        branches = result.stdout.strip().split('\n')

        # Format branch names (remove asterisk from current branch)
        formatted_branches = []
        for branch in branches:
            branch = branch.strip()
            if branch.startswith('*'):
                branch = branch[1:].strip()  # Remove asterisk and spaces
            formatted_branches.append(branch)

        # Remove current branch from the list
        if source_branch in formatted_branches:
            formatted_branches.remove(source_branch)

        if not formatted_branches:
            print(f"{YELLOW}No other branches available to merge with.{ENDC}")
            return

        # Let user select target branch
        print("\nAvailable branches to merge with:")
        for idx, branch in enumerate(formatted_branches, 1):
            print(f"{idx}. {branch}")

        branch_choice = input("\nSelect a branch to merge with (by number), or 'c' to cancel: ")

        if branch_choice.lower() == 'c':
            print("Merge operation canceled.")
            return

        try:
            branch_idx = int(branch_choice) - 1
            if 0 <= branch_idx < len(formatted_branches):
                target_branch = formatted_branches[branch_idx]
            else:
                print(f"{YELLOW}Invalid branch number.{ENDC}")
                return
        except ValueError:
            print(f"{YELLOW}Invalid input. Please enter a number.{ENDC}")
            return

        # Save the current branch name to return later
        original_branch = source_branch

        print(f"\n{GREEN}Merging current branch '{source_branch}' into '{target_branch}'...{ENDC}")

        # Switch to target branch
        checkout_result = subprocess.run(
            ["git", "checkout", target_branch],
            capture_output=True,
            text=True
        )

        if checkout_result.returncode != 0:
            print(f"{YELLOW}Could not switch to branch {target_branch}: {checkout_result.stderr.strip()}{ENDC}")

            # Check for uncommitted changes
            if "local changes" in checkout_result.stderr or "cambios locales" in checkout_result.stderr:
                if not handle_uncommitted_changes(target_branch):
                    return
            else:
                return

        # Perform the merge
        merge_result = subprocess.run(
            ["git", "merge", source_branch, "--allow-unrelated-histories"],
            capture_output=True,
            text=True
        )

        # Check merge result
        if merge_result.returncode == 0:
            print(f"{GREEN}Branch '{source_branch}' successfully merged into '{target_branch}'.{ENDC}")

            # Ask if user wants to go back to original branch
            go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
            if go_back == 'y':
                subprocess.run(["git", "checkout", original_branch])
                print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
        else:
            # Handle merge conflicts
            print(f"{YELLOW}Could not merge branch '{source_branch}' into '{target_branch}'.{ENDC}")
            print(f"Reason: {merge_result.stderr.strip()}")

            # Offer conflict resolution options
            print("\nAvailable options:")
            print(f"1. Force merge ('ours' strategy - prioritizes {target_branch} changes)")
            print(f"2. Force merge ('theirs' strategy - prioritizes {source_branch} changes)")
            print("3. Cancel operation")

            choice = input("\nSelect an option (1-3): ")

            if choice == "1":
                # Use "ours" strategy (keep target branch changes)
                ours_result = subprocess.run(
                    ["git", "merge", "-X", "ours", source_branch],
                    capture_output=True,
                    text=True
                )

                if ours_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Changes from '{target_branch}' have been prioritized.{ENDC}")

                    # Ask about returning to original branch
                    go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
                    if go_back == 'y':
                        subprocess.run(["git", "checkout", original_branch])
                        print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {ours_result.stderr.strip()}{ENDC}")
                    # Return to original branch
                    subprocess.run(["git", "checkout", original_branch])
                    print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

            elif choice == "2":
                # Use "theirs" strategy (keep source branch changes)
                theirs_result = subprocess.run(
                    ["git", "merge", "-X", "theirs", source_branch],
                    capture_output=True,
                    text=True
                )

                if theirs_result.returncode == 0:
                    print(f"{GREEN}Forced merge completed. Changes from '{source_branch}' have been prioritized.{ENDC}")

                    # Ask about returning to original branch
                    go_back = input(f"Do you want to go back to branch '{source_branch}'? (y/n): ").lower()
                    if go_back == 'y':
                        subprocess.run(["git", "checkout", original_branch])
                        print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
                else:
                    print(f"{YELLOW}Forced merge failed: {theirs_result.stderr.strip()}{ENDC}")
                    # Return to original branch
                    subprocess.run(["git", "checkout", original_branch])
                    print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

            else:
                print("Merge operation canceled.")
                # Return to original branch
                subprocess.run(["git", "checkout", original_branch])
                print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")

    except Exception as e:
        print(f"Error merging branches: {e}")
        # Try to return to the original branch in case of error
        try:
            original_branch = source_branch
            subprocess.run(["git", "checkout", original_branch])
            print(f"{GREEN}Returned to branch '{original_branch}'.{ENDC}")
        except:
            pass

def show_all_branches():
    """Muestra tanto las ramas locales como remotas"""
    from .branx_local import check_local_branches  # Import here to avoid circular import

    print(f"\n{GREEN}Local Branches:{ENDC}")
    check_local_branches()
    print(f"\n{GREEN}Remote Branches:{ENDC}")
    check_remote_branches()
    print()

def add_branch_menu():
    """Submenú para añadir una rama"""
    while True:
        print(f"\n{GREEN}Add Branch:{ENDC}")

        menu_options = [
            "[l] Local Branch",
            "[r] Remote Branch",
            "[x] Back to Branches menu"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Select where to add the branch:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            create_local_branch()
            break
        elif menu_entry_index == 1:
            create_remote_branch()
            break
        elif menu_entry_index == 2:
            break

def create_remote_branch():
    """Create a branch directly on the remote repository."""
    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    try:
        # Get the current branch as base reference
        base_branch = input("Enter the name of the base branch (default: main): ") or "main"

        # Get the name for the new remote branch
        new_branch_name = input("Enter the name for the new remote branch: ")
        if not new_branch_name:
            print("Branch name cannot be empty. Operation cancelled.")
            return

        # First, fetch to make sure we have the latest reference of the base branch
        fetch_result = subprocess.run(
            ["git", "fetch", "origin", base_branch],
            capture_output=True,
            text=True
        )

        if fetch_result.returncode != 0:
            print(f"{YELLOW}Error fetching the base branch: {fetch_result.stderr.strip()}{ENDC}")
            return

        # Create a remote branch based on the specified base branch
        create_result = subprocess.run(
            ["git", "push", "origin", f"origin/{base_branch}:refs/heads/{new_branch_name}"],
            capture_output=True,
            text=True
        )

        if create_result.returncode == 0:
            print(f"{GREEN}Remote branch '{new_branch_name}' created successfully!{ENDC}")

            # Ask if user wants to check out the new branch locally
            checkout_local = input(f"Do you want to check out this branch locally? (y/n): ").lower()
            if checkout_local == 'y':
                checkout_result = subprocess.run(
                    ["git", "checkout", "-b", new_branch_name, f"origin/{new_branch_name}"],
                    capture_output=True,
                    text=True
                )

                if checkout_result.returncode == 0:
                    print(f"{GREEN}Switched to a new branch '{new_branch_name}' tracking the remote branch.{ENDC}")
                else:
                    print(f"{YELLOW}Error checking out the branch locally: {checkout_result.stderr.strip()}{ENDC}")
        else:
            print(f"{YELLOW}Error creating remote branch: {create_result.stderr.strip()}{ENDC}")

    except Exception as e:
        print(f"Error creating remote branch: {e}")

def delete_branch_menu():
    """Submenú para eliminar una rama"""
    while True:
        print(f"\n{GREEN}Delete Branch:{ENDC}")

        menu_options = [
            "[l] Local Branch",
            "[r] Remote Branch",
            "[x] Back to Branches menu"
        ]

        terminal_menu = TerminalMenu(
            menu_options,
            title="Select where to delete the branch:",
            menu_cursor=MENU_CURSOR,
            menu_cursor_style=MENU_CURSOR_STYLE
        )
        menu_entry_index = terminal_menu.show()

        if menu_entry_index == 0:
            delete_local_branch()
            break
        elif menu_entry_index == 1:
            delete_remote_branch()
            break
        elif menu_entry_index == 2:
            break

def import_remote_branch():
    """Importa una rama remota al repositorio local"""
    if not is_git_repo():
        print_not_git_repo()
        return

    if not is_connected_to_remote():
        print_not_connected_to_remote()
        return

    try:
        # Obtenemos la lista de ramas remotas
        subprocess.run(["git", "fetch"])
        result = subprocess.run(
            ["git", "--no-pager", "branch", "-r"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"{YELLOW}Error listing remote branches: {result.stderr.strip()}{ENDC}")
            return

        remote_branches = result.stdout.strip().split('\n')
        remote_branches = [branch.strip() for branch in remote_branches if branch.strip()]

        if not remote_branches:
            print(f"{YELLOW}No remote branches found.{ENDC}")
            return

        print("\nAvailable remote branches:")
        for idx, branch in enumerate(remote_branches, 1):
            print(f"{idx}. {branch}")

        choice = input("\nSelect a branch to import (by number, or 0 to cancel): ")
        try:
            choice_idx = int(choice)
            if choice_idx == 0:
                print("Import operation cancelled.")
                return

            if 1 <= choice_idx <= len(remote_branches):
                selected_branch = remote_branches[choice_idx - 1]
                # Extraemos solo el nombre de la rama sin el "origin/"
                branch_name = selected_branch.split('/', 1)[1] if '/' in selected_branch else selected_branch

                # Creamos una rama local que hace tracking de la remota
                checkout_result = subprocess.run(
                    ["git", "checkout", "--track", selected_branch],
                    capture_output=True,
                    text=True
                )

                if checkout_result.returncode == 0:
                    print(f"{GREEN}Remote branch '{branch_name}' successfully imported to local repository.{ENDC}")
                else:
                    print(f"{YELLOW}Could not import remote branch: {checkout_result.stderr.strip()}{ENDC}")
            else:
                print(f"{YELLOW}Invalid choice. Please select a number between 1 and {len(remote_branches)}.{ENDC}")
        except ValueError:
            print(f"{YELLOW}Please enter a valid number.{ENDC}")
    except Exception as e:
        print(f"Error importing remote branch: {e}")

def manage_branches():
    while True:
        current = current_branch()
        branch_display = f"{WHITE_TEXT}{BG_BLUE}{BOLD} {current} {ENDC}"
        print(f"{GREEN}Branches:{ENDC} {branch_display}")

        menu_options = [
            f"[s] Show All Branches",
            f"[a] {manage_branch_menu.ADD_BRANCH.value}",
            f"[g] {branch_local_menu.GOTO_BRANCH.value}",
            f"[m] {manage_branch_menu.MERGE.value}",
            f"[j] {manage_branch_menu.LINK_BRANCH.value}",
            f"[y] {manage_branch_menu.PULL_BRANCH.value}",
            f"[d] Delete Branch",
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
            show_all_branches()
        elif menu_entry_index == 1:
            add_branch_menu()
        elif menu_entry_index == 2:
            go_to_branch()
        elif menu_entry_index == 3:
            merge_branches()
        elif menu_entry_index == 4:
            connect_local_branch_with_remote()
        elif menu_entry_index == 5:
            import_remote_branch()
        elif menu_entry_index == 6:
            delete_branch_menu()
        elif menu_entry_index == 7:
            clear_screen()
            break
        elif menu_entry_index == 8:
            quit()

def merge_branches():
    if not is_git_repo():
        print_not_git_repo()
        return

    try:
        # Get all local branches
        result = subprocess.run(
            ["git", "branch"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"{YELLOW}Error listing branches: {result.stderr.strip()}{ENDC}")
            return

        # Process the branch list
        all_branches = []
        current_branch_name = current_branch()

        for branch in result.stdout.strip().split('\n'):
            branch = branch.strip()
            if branch.startswith('*'):
                branch = branch[2:]  # Remove the * and space

            if branch:
                all_branches.append(branch)

        if len(all_branches) < 2:
            print(f"{YELLOW}At least two branches are needed to perform a merge.{ENDC}")
            return

        # STEP 1: Select the source branch (the one that will be merged into the destination)
        print(f"\n{GREEN}Current branch:{ENDC} {current_branch_name}")
        print(f"\n{GREEN}Select the source branch (the one that will be merged into the destination):{ENDC}")

        for idx, branch in enumerate(all_branches, 1):
            if branch == current_branch_name:
                print(f"{idx}. {branch} (current branch)")
            else:
                print(f"{idx}. {branch}")

        # Ask the user to choose the source branch
        origin_choice = input("\nSelect the source branch (number, or 0 to cancel): ")

        try:
            origin_idx = int(origin_choice)
            if origin_idx == 0:
                print("Merge operation canceled.")
                return

            if 1 <= origin_idx <= len(all_branches):
                origin_branch = all_branches[origin_idx - 1]

                # STEP 2: Select the destination branch (where changes will be merged)
                print(f"\n{GREEN}Select the destination branch (where changes will be merged):{ENDC}")

                # Filter out the source branch from options
                destination_branches = [b for b in all_branches if b != origin_branch]

                for idx, branch in enumerate(destination_branches, 1):
                    if branch == current_branch_name:
                        print(f"{idx}. {branch} (current branch)")
                    else:
                        print(f"{idx}. {branch}")

                # Ask the user to choose the destination branch
                dest_choice = input("\nSelect the destination branch (number, or 0 to cancel): ")

                try:
                    dest_idx = int(dest_choice)
                    if dest_idx == 0:
                        print("Merge operation canceled.")
                        return

                    if 1 <= dest_idx <= len(destination_branches):
                        target_branch = destination_branches[dest_idx - 1]

                        # Save the original branch to return to it later if needed
                        original_branch = current_branch_name

                        # Switch to destination branch
                        checkout_result = subprocess.run(
                            ["git", "checkout", target_branch],
                            capture_output=True,
                            text=True
                        )

                        if checkout_result.returncode != 0:
                            print(f"{YELLOW}Could not switch to branch {target_branch}: {checkout_result.stderr.strip()}{ENDC}")

                            # Check if the error is due to uncommitted local changes
                            if "local changes" in checkout_result.stderr or "cambios locales" in checkout_result.stderr:
                                if handle_uncommitted_changes(target_branch):
                                    # Try to do a normal merge
                                    print(f"\n{YELLOW}Attempting to merge {origin_branch} into {target_branch}...{ENDC}")
                                    result = subprocess.run(
                                        ["git", "merge", origin_branch, "--allow-unrelated-histories"],
                                        capture_output=True,
                                        text=True
                                    )

                                    # If merge is successful
                                    if result.returncode == 0:
                                        print(f"{GREEN}Branch {origin_branch} successfully merged into {target_branch}.{ENDC}")

                                        # Ask if they want to stay on destination branch
                                        if target_branch != original_branch:
                                            # We're already on the target_branch at this point
                                            stay_on_target = input(f"\nGo to destination branch '{target_branch}'? (y/n): ").lower()
                                            if stay_on_target != 'y' and stay_on_target != 's':
                                                subprocess.run(["git", "checkout", original_branch])
                                                print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")
                                    else:
                                        # If merge fails, show error and offer options
                                        print(f"{YELLOW}Could not merge branch {origin_branch} into {target_branch}.{ENDC}")
                                        print(f"Reason: {result.stderr.strip()}")

                                        # Offer options to resolve
                                        print("\nAvailable options:")
                                        print(f"1. Force merge ('ours' strategy - prioritizes {target_branch} changes)")
                                        print(f"2. Force merge ('theirs' strategy - prioritizes {origin_branch} changes)")
                                        print("3. Cancel operation")

                                        choice = input("\nSelect an option (1-3): ")

                                        if choice == "1":
                                            print(f"{YELLOW}Executing forced merge (ours)...{ENDC}")
                                            ours_result = subprocess.run(
                                                ["git", "merge", "-X", "ours", origin_branch],
                                                capture_output=True,
                                                text=True
                                            )

                                            if ours_result.returncode == 0:
                                                print(f"{GREEN}Forced merge completed. Changes from {target_branch} have been prioritized.{ENDC}")

                                                # Ask if they want to stay on destination branch
                                                if target_branch != original_branch:
                                                    # We're already on the target_branch at this point
                                                    stay_on_target = input(f"\nGo to destination branch '{target_branch}'? (y/n): ").lower()
                                                    if stay_on_target != 'y' and stay_on_target != 's':
                                                        subprocess.run(["git", "checkout", original_branch])
                                                        print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")
                                            else:
                                                print(f"{YELLOW}Forced merge failed: {ours_result.stderr.strip()}{ENDC}")
                                                # Return to original branch
                                                if target_branch != original_branch:
                                                    subprocess.run(["git", "checkout", original_branch])
                                                    print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")

                                        elif choice == "2":
                                            print(f"{YELLOW}Executing forced merge (theirs)...{ENDC}")
                                            theirs_result = subprocess.run(
                                                ["git", "merge", "-X", "theirs", origin_branch],
                                                capture_output=True,
                                                text=True
                                            )

                                            if theirs_result.returncode == 0:
                                                print(f"{GREEN}Forced merge completed. Changes from {origin_branch} have been prioritized.{ENDC}")

                                                # Ask if they want to stay on destination branch
                                                if target_branch != original_branch:
                                                    # We're already on the target_branch at this point
                                                    stay_on_target = input(f"\nGo to destination branch '{target_branch}'? (y/n): ").lower()
                                                    if stay_on_target != 'y' and stay_on_target != 's':
                                                        subprocess.run(["git", "checkout", original_branch])
                                                        print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")
                                            else:
                                                print(f"{YELLOW}Forced merge failed: {theirs_result.stderr.strip()}{ENDC}")
                                                # Return to original branch
                                                if target_branch != original_branch:
                                                    subprocess.run(["git", "checkout", original_branch])
                                                    print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")

                                        else:
                                            print("Merge operation canceled.")
                                            # Return to original branch
                                            if target_branch != original_branch:
                                                subprocess.run(["git", "checkout", original_branch])
                                                print(f"{GREEN}You have returned to branch {original_branch}.{ENDC}")
                    else:
                        print(f"{YELLOW}Invalid option. Please select a number between 1 and {len(destination_branches)}.{ENDC}")
                except ValueError:
                    print(f"{YELLOW}Please enter a valid number.{ENDC}")
            else:
                print(f"{YELLOW}Invalid option. Please select a number between 1 and {len(all_branches)}.{ENDC}")
        except ValueError:
            print(f"{YELLOW}Please enter a valid number.{ENDC}")
    except Exception as e:
        print(f"Error merging branches: {e}")
        # Try to return to the original branch in case of error
        try:
            subprocess.run(["git", "checkout", current_branch_name])
        except:
            pass

def delete_local_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    from .branx_local import check_local_branches  # Import here to avoid circular import

    # Show existing branches
    print("\nAvailable local branches:")
    check_local_branches()

    branch = input("\nEnter the name of the branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch.{ENDC}\nIf you want to delete the repository: Work in local -> Local -> Manage repos -> Delete local repo")
        return

    # Check if the branch exists
    try:
        branch_exists = subprocess.run(
            ["git", "show-ref", "--verify", f"refs/heads/{branch}"],
            capture_output=True,
            text=True
        ).returncode == 0

        if not branch_exists:
            print(f"{YELLOW}The branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying branch existence: {e}")
        return

    # Check if it's the current branch
    current = current_branch()
    if current == branch:
        print(f"{YELLOW}You cannot delete the branch you are currently on.{ENDC}\nSwitch to another branch first using 'Go to Branch' or 'Go to Main'.")
        return

    # Try to delete the branch normally
    try:
        result = subprocess.run(
            ["git", "branch", "-d", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            # If it fails, probably has unmerged changes
            print(f"{YELLOW}Could not delete branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")

            # Ask if they want to force delete
            force_delete = input("\nDo you want to force deletion? This action is irreversible and you will lose all unmerged changes. (y/n): ").lower()

            if force_delete == 'y':
                force_result = subprocess.run(["git", "branch", "-D", branch])
                if force_result.returncode == 0:
                    print(f"{GREEN}The branch '{branch}' has been forcibly deleted.{ENDC}")
                else:
                    print(f"{YELLOW}Could not forcibly delete the branch: {force_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error deleting local branch: {e}")

def delete_remote_branch():
    if not is_git_repo():
        print_not_git_repo()
        return

    # Show available remote branches
    print("\nAvailable remote branches:")
    check_remote_branches()

    branch = input("\nEnter the name of the remote branch you want to delete: ")

    # Check if the branch is main
    if branch == "main":
        print(f"{YELLOW}You cannot delete the main branch of the remote repository.{ENDC}")
        return

    # Verify if the remote branch exists
    try:
        remote_branches = subprocess.run(
            ["git", "ls-remote", "--heads", "origin"],
            capture_output=True,
            text=True
        ).stdout

        if f"refs/heads/{branch}" not in remote_branches:
            print(f"{YELLOW}The remote branch '{branch}' does not exist.{ENDC}")
            return
    except Exception as e:
        print(f"Error verifying remote branch existence: {e}")
        return

    # Ask for confirmation
    confirm = input(f"\nAre you sure you want to delete the remote branch '{branch}'? This action is irreversible. (y/n): ").lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return

    # Delete the remote branch
    try:
        result = subprocess.run(
            ["git", "push", "origin", "--delete", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}The remote branch '{branch}' has been successfully deleted.{ENDC}")
        else:
            print(f"{YELLOW}Could not delete remote branch '{branch}'.{ENDC}")
            print(f"Reason: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error deleting remote branch: {e}")

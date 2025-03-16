# ADVANCED OPERATIONS
import subprocess
from simple_term_menu import TerminalMenu
from .utils import YELLOW, GREEN, ENDC
from .checks import is_git_repo, print_not_git_repo, current_branch

def advanced_operations():
    while True:
        print(f"\n{GREEN}Advanced Operations{ENDC}")
        print(f"{YELLOW}WARNING: Some of these operations can be destructive.{ENDC}")

        menu_options = [
            "Reset (undo changes at specific levels)",
            "Clean (remove untracked files)",
            "Force push (forcefully send changes)",
            "Stash (temporarily save changes)",
            "Cherry-pick (select specific commits)",
            "Interactive rebase (reorganize/edit commits)",
            "Return to main menu"
        ]

        terminal_menu = TerminalMenu(menu_options, title="Select an operation:")
        choice = terminal_menu.show()

        if choice == 0:
            reset_operations()
        elif choice == 1:
            clean_untracked_files()
        elif choice == 2:
            force_push()
        elif choice == 3:
            stash_operations()
        elif choice == 4:
            cherry_pick_commits()
        elif choice == 5:
            interactive_rebase()
        elif choice == 6:
            clear_screen()
            break

def reset_operations():
    print(f"\n{GREEN}Reset Operations{ENDC}")
    print(f"{YELLOW}WARNING: These operations can be destructive.{ENDC}")

    menu_options = [
        "Soft reset (preserves changes in staging area)",
        "Mixed reset (preserves changes in files but removes them from staging area)",
        "Hard reset (discards all local changes)",
        "Return to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select reset type:")
    choice = terminal_menu.show()

    if choice == 3:  # Return to previous menu
        return

    # Get the commit to reset to
    print("\nReset options:")
    print("1. Reset to the last commit")
    print("2. Reset to a specific number of commits back")
    print("3. Reset to a specific commit hash")

    reset_option = input("Select an option (1-3): ")

    reset_target = ""

    if reset_option == "1":
        reset_target = "HEAD~1"
    elif reset_option == "2":
        num_commits = input("How many commits back? ")
        try:
            reset_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Invalid number. Operation cancelled.")
            return
    elif reset_option == "3":
        # Show recent commits for reference
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
        reset_target = input("\nEnter the commit hash: ")
    else:
        print("Invalid option. Operation cancelled.")
        return

    # Confirm the operation
    confirm = input(f"{YELLOW}This operation can be destructive. Are you sure? (y/n): {ENDC}").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return


    # Execute the corresponding reset
    reset_type = ["--soft", "--mixed", "--hard"][choice]
    try:
        result = subprocess.run(
            ["git", "reset", reset_type, reset_target],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Reset {reset_type} completed successfully.{ENDC}")
            if reset_type == "--hard":
                print("All local changes have been discarded.")
            elif reset_type == "--soft":
                print("Changes have been preserved in the staging area.")
            else:  # mixed
                print("Changes have been preserved in files but removed from the staging area.")
        else:
            print(f"{YELLOW}Error executing reset: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during reset: {e}")

def clean_untracked_files():
    print(f"\n{GREEN}Clean untracked files{ENDC}")

    # Show untracked files
    print("\nUntracked files:")
    subprocess.run(["git", "ls-files", "--others", "--exclude-standard"])

    menu_options = [
        "Interactive mode (select files to delete)",
        "Delete all untracked files",
        "Delete untracked files and directories",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an option:")
    choice = terminal_menu.show()

    if choice == 3:  # Go back
        return

    # Confirm the operation
    if choice == 0:
        print("Starting interactive mode...")
        subprocess.run(["git", "clean", "-i"])
    else:
        # For options 1 and 2, ask for explicit confirmation
        clean_message = "all untracked files"
        clean_command = ["git", "clean", "-f"]

        if choice == 1:
            clean_message = "all untracked files"
        elif choice == 2:
            clean_message = "all untracked files and directories"
            clean_command = ["git", "clean", "-fd"]

        confirm = input(f"{YELLOW}Are you sure you want to delete {clean_message}? This action cannot be undone. (y/n): {ENDC}").lower()
        if confirm == "y":
            try:
                result = subprocess.run(clean_command, capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"{GREEN}Cleaning completed successfully.{ENDC}")
                else:
                    print(f"{YELLOW}Error during cleaning: {result.stderr.strip()}{ENDC}")
            except Exception as e:
                print(f"Error during cleaning: {e}")
        else:
            print("Operation cancelled.")

def force_push():
    branch = current_branch()
    if not branch:
        print_not_git_repo()
        return

    print(f"\n{GREEN}Force Push{ENDC}")
    print(f"{YELLOW}WARNING: This operation may overwrite changes in the remote repository.{ENDC}")

    # Offer options for different types of force push
    menu_options = [
        "Normal force push (--force)",
        "Safe force push (--force-with-lease)",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select the type of force push:")
    choice = terminal_menu.show()

    if choice == 2:  # Go back
        return

    # Confirm the operation
    warning_message = "This action may permanently overwrite remote changes."
    if choice == 0:
        confirm = input(f"{YELLOW}Normal force push: {warning_message} Are you sure? (y/n): {ENDC}").lower()
        push_option = "--force"
    else:  # choice == 1
        confirm = input(f"{YELLOW}Safe force push: Will only overwrite if there are no new changes in remote. Continue? (y/n): {ENDC}").lower()
        push_option = "--force-with-lease"

    if confirm != "y":
        print("Operation cancelled.")
        return

    # Execute the force push
    try:
        result = subprocess.run(
            ["git", "push", push_option, "origin", branch],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print(f"{GREEN}Force push completed. Changes have been forcibly sent to remote branch {branch}.{ENDC}")
        else:
            print(f"{YELLOW}Force push failed: {result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during force push: {e}")

def stash_operations():
    print(f"\n{GREEN}Stash Operations{ENDC}")

    menu_options = [
        "Save changes to stash",
        "List saved stashes",
        "Apply stash (keeping in list)",
        "Apply and remove stash",
        "Delete specific stash",
        "Delete all stashes",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an operation:")
    choice = terminal_menu.show()

    if choice == 0:  # Save to stash
        message = input("Descriptive message for the stash (optional): ")
        try:
            if message:
                result = subprocess.run(["git", "stash", "push", "-m", message], capture_output=True, text=True)
            else:
                result = subprocess.run(["git", "stash", "push"], capture_output=True, text=True)

            if result.returncode == 0:
                if "No local changes to save" in result.stdout:
                    print("No local changes to save in stash.")
                else:
                    print(f"{GREEN}Changes successfully saved to stash.{ENDC}")
            else:
                print(f"{YELLOW}Error saving to stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 1:  # List stashes
        try:
            result = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
            if result.stdout.strip():
                print("\nSaved stashes:")
                print(result.stdout)
            else:
                print("No saved stashes.")
        except Exception as e:
            print(f"Error listing stashes: {e}")

    elif choice in [2, 3]:  # Apply stash
        # First list available stashes
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No saved stashes.")
                return

            print("\nAvailable stashes:")
            print(stash_list)

            stash_index = input("\nEnter the stash index (0 for most recent, 1 for next, etc.): ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Invalid index. Operation cancelled.")
                return

            if choice == 2:  # Apply keeping
                result = subprocess.run(["git", "stash", "apply", stash_ref], capture_output=True, text=True)
                success_message = "Stash applied successfully and kept in the list."
            else:  # choice == 3, apply and drop
                result = subprocess.run(["git", "stash", "pop", stash_ref], capture_output=True, text=True)
                success_message = "Stash applied successfully and removed from the list."

            if result.returncode == 0:
                print(f"{GREEN}{success_message}{ENDC}")
            else:
                print(f"{YELLOW}Error applying stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 4:  # Delete specific stash
        try:
            stash_list = subprocess.run(["git", "stash", "list"], capture_output=True, text=True).stdout.strip()

            if not stash_list:
                print("No saved stashes.")
                return

            print("\nAvailable stashes:")
            print(stash_list)

            stash_index = input("\nEnter the index of the stash to delete: ")
            try:
                stash_ref = f"stash@{{{stash_index}}}"
            except ValueError:
                print("Invalid index. Operation cancelled.")
                return

            confirm = input(f"{YELLOW}Are you sure you want to delete this stash? This action cannot be undone. (y/n): {ENDC}").lower()
            if confirm != "y":
                print("Operation cancelled.")
                return

            result = subprocess.run(["git", "stash", "drop", stash_ref], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"{GREEN}Stash deleted successfully.{ENDC}")
            else:
                print(f"{YELLOW}Error deleting stash: {result.stderr.strip()}{ENDC}")
        except Exception as e:
            print(f"Error in stash operation: {e}")

    elif choice == 5:  # Delete all stashes
        confirm = input(f"{YELLOW}Are you sure you want to delete ALL stashes? This action cannot be undone. (y/n): {ENDC}").lower()
        if confirm != "y":
            print("Operation cancelled.")
            return

        try:
            result = subprocess.run(["git", "stash", "clear"], capture_output=True, text=True)
            print(f"{GREEN}All stashes have been deleted.{ENDC}")
        except Exception as e:
            print(f"Error deleting stashes: {e}")

    elif choice == 6:  # Go back
        return

def cherry_pick_commits():
    print(f"\n{GREEN}Cherry-pick (select specific commits){ENDC}")

    # Show latest commits to select from
    print("\nLatest available commits:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "20"])
    except Exception as e:
        print(f"Error showing commits: {e}")
        return

    commit_hash = input("\nEnter the hash of the commit you want to apply: ")
    if not commit_hash:
        print("Operation cancelled.")
        return

    # Options for cherry-pick
    menu_options = [
        "Normal cherry-pick (create new commit)",
        "Cherry-pick without creating commit (--no-commit)",
        "Cherry-pick and edit commit message (--edit)",
        "Back to previous menu"
    ]

    terminal_menu = TerminalMenu(menu_options, title="Select an option:")
    choice = terminal_menu.show()

    if choice == 3:  # Go back
        return

    # Prepare command according to option
    cherry_pick_cmd = ["git", "cherry-pick"]
    if choice == 1:
        cherry_pick_cmd.append("--no-commit")
    elif choice == 2:
        cherry_pick_cmd.append("--edit")

    cherry_pick_cmd.append(commit_hash)

    # Execute cherry-pick
    try:
        result = subprocess.run(cherry_pick_cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"{GREEN}Cherry-pick completed successfully.{ENDC}")
            if choice == 1:
                print("Changes have been applied but no commit has been created. You can modify them and then commit.")
        else:
            print(f"{YELLOW}Error during cherry-pick: {result.stderr.strip()}{ENDC}")

            # Offer options in case of conflict
            if "conflict" in result.stderr:
                print("\nConflicts detected. Available options:")
                conflict_options = [
                    "Continue manually (resolve conflicts in editor)",
                    "Abort cherry-pick and return to previous state",
                    "Back to menu"
                ]

                conflict_menu = TerminalMenu(conflict_options, title="What do you want to do?")
                conflict_choice = conflict_menu.show()

                if conflict_choice == 0:
                    print("Continue resolving conflicts manually in your editor.")
                    print("After resolving them, use 'git add' for the modified files and 'git cherry-pick --continue'.")
                elif conflict_choice == 1:
                    abort_result = subprocess.run(["git", "cherry-pick", "--abort"], capture_output=True, text=True)
                    if abort_result.returncode == 0:
                        print(f"{GREEN}Cherry-pick aborted. Previous state has been restored.{ENDC}")
                    else:
                        print(f"{YELLOW}Error aborting cherry-pick: {abort_result.stderr.strip()}{ENDC}")
    except Exception as e:
        print(f"Error during cherry-pick: {e}")

def interactive_rebase():
    print(f"\n{GREEN}Interactive Rebase{ENDC}")
    print(f"{YELLOW}WARNING: This operation rewrites commit history.{ENDC}")

    # Show recent commits for reference
    print("\nRecent commits:")
    try:
        subprocess.run(["git", "--no-pager", "log", "--oneline", "-n", "10"])
    except Exception as e:
        print(f"Error displaying commits: {e}")
        return

    # Rebase options
    print("\nSpecify how many commits you want to include in the rebase:")
    print("1. Last N commits")
    print("2. From a specific commit")
    print("3. Return to previous menu")

    rebase_option = input("Select an option (1-3): ")

    if rebase_option == "3" or not rebase_option:
        return

    rebase_target = ""
    if rebase_option == "1":
        num_commits = input("How many commits back? ")
        try:
            rebase_target = f"HEAD~{int(num_commits)}"
        except ValueError:
            print("Invalid number. Operation cancelled.")
            return
    elif rebase_option == "2":
        rebase_target = input("Enter the base commit hash: ")
    else:
        print("Invalid option. Operation cancelled.")
        return

    # Extra confirmation due to destructive nature
    confirm = input(f"{YELLOW}Interactive rebase will modify commit history. This operation can cause problems if commits have already been shared. Are you sure? (y/n): {ENDC}").lower()
    if confirm != "y":
        print("Operation cancelled.")
        return

    # Execute interactive rebase
    print("\nThe editor will open for interactive rebase. Instructions:")
    print("- pick: keep the commit as is")
    print("- reword: keep the commit but change its message")
    print("- edit: keep the commit but pause to modify it")
    print("- squash: combine with previous commit (keeps both messages)")
    print("- fixup: combine with previous commit (discards its message)")
    print("- drop: remove the commit")
    print("\nSave and close the editor to continue with the rebase.")

    input("\nPress Enter to continue...")

    try:
        # The -i flag indicates interactive rebase
        result = subprocess.run(["git", "rebase", "-i", rebase_target])

        # The result will depend on user interaction with the editor
        if result.returncode == 0:
            print(f"{GREEN}Interactive rebase completed successfully.{ENDC}")
        else:
            print(f"{YELLOW}Interactive rebase did not complete successfully. There may be conflicts to resolve.{ENDC}")
    except Exception as e:
        print(f"Error during interactive rebase: {e}")

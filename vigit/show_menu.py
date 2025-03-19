import subprocess
import os
from simple_term_menu import TerminalMenu
from rich.console import Console
from rich.theme import Theme

from .constants import show_menu, MENU_CURSOR, MENU_CURSOR_STYLE
from .checks import is_git_repo, print_not_git_repo
from .menu import show_status_short, draw_box_blessed
from .utils import YELLOW, GREEN, ENDC

# Initialize Rich console with custom theme
custom_theme = Theme({
    "info": "green",
    "warning": "yellow",
    "error": "bold red",
    "clean": "green italic"
})
console = Console(theme=custom_theme)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("\nVISUAL GIT", style="bold green")
    console.print("-" * 30)

def show_git_status_legend():
    """Display legend for Git status codes"""
    print("\nStatus codes:")
    print(f"{GREEN}M{ENDC} = Modified   {GREEN}A{ENDC} = Added     {GREEN}D{ENDC} = Deleted")
    print(f"{GREEN}R{ENDC} = Renamed    {GREEN}C{ENDC} = Copied    {GREEN}U{ENDC} = Updated but unmerged")
    print(f"{GREEN}??{ENDC} = Untracked files")

def show_menu_options():
    while True:
        console.print(f"\nSHOW", style="green")

        # Automatically show status before displaying menu options
        if is_git_repo():
            try:
                # Capture output to check for changes
                result = subprocess.run(
                    ["git", "status", "-s"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                status = result.stdout.strip()

                print()  # Space before panel
                if status:
                    # Get colored output
                    colored_result = subprocess.run(
                        ["git", "-c", "color.status=always", "status", "-s"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    colored_status = colored_result.stdout.strip()

                    # Get status output
                    status_lines = colored_status.split('\n')
                    draw_box_blessed(status_lines, "Status", use_colors=True, include_status_legend=True)
                else:
                    draw_box_blessed(["Working tree clean"], "Status")
                print()
            except Exception as e:
                console.print(f"Error getting status: {e}", style="error")
        else:
            print_not_git_repo()

        menu_options = [
            f"[s] {show_menu.SHOW_STATUS.value}",
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
            show_status_short()
        elif menu_entry_index == 1:
            clear_screen()
            break
        elif menu_entry_index == 2:
            quit()
        else:
            console.print("Invalid option. Please try again.", style="warning")

from enum import Enum

class branch_menu(Enum):
    BRANCH_LOCAL = 'Local'
    BRANCH_REMOTE = 'Remote'
    MANAGE_BRANCHES = 'Branches'

class branch_local_menu(Enum):
    CHECK_LOCAL_BRANCH = 'See Local Branches'
    ADD_LOCAL_BRANCH = 'Add a Local Branch'
    GOTO_BRANCH = 'Go to Branch'
    GOTO_MAIN = 'Go to Main'

class branch_lr_menu(Enum):
    CHECK_REMOTE_BRANCH = 'See Remote Branches'
    LINK_REMOTE_BRANCH = 'Join Local Branch to Remote'
    COMMIT_LOCAL_BRANCH = 'Commit to Local Branch'
    PUSH_BRANCH = 'Push Changes to Remote Branch'
    COMMIT_PUSH_BRANCH = 'Commit & Push in Branch'

class branch_rl_menu(Enum):
    CLONE_BRANCH = 'Fork Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'

class branch_remote_menu(Enum):
    CHECK_REMOTE_BRANCH = 'See Remote Branches'
    LINK_REMOTE_BRANCH = 'Join Local Branch to Remote'
    COMMIT_LOCAL_BRANCH = 'Commit to Local Branch'
    PUSH_BRANCH = 'Push Changes to Remote Branch'
    COMMIT_PUSH_BRANCH = 'Commit & Push in Branch'
    CLONE_BRANCH = 'Fork Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'

class manage_branch_menu(Enum):
    ADD_BRANCH = 'Add a Branch'
    LINK_BRANCH = 'Join Local Branch with Remote'
    MERGE = 'Merge Branches'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'
    DELETE_LOCAL_BRANCH = 'Delete Local Branch'
    DELETE_REMOTE_BRANCH = 'Delete Remote Branch'

class main_menu(Enum):
    LOCAL = 'Local'
    REMOTE = 'Remote'

class main_local_menu(Enum):
    ADD_LOCAL = 'Add a Local Repo'
    COMMIT_LOCAL = 'Commit to Local Repo'

class main_remote_menu(Enum):
    ADD_REMOTE = 'Add Remote Repo'
    LINK = 'Join Local to Remote'
    COMMIT_AND_PUSH = 'Commit & Push'
    CLONE = 'Fork Remote to Local'
    PULL = 'Yank Changes from Remote'
    DELETE_REMOTE = 'Delete Remote Repo'

class start_menu(Enum):
    WORK_IN_MAIN = "Work in Main"
    WORK_IN_BRANCHES = "Work in Branches"
    CHECK_LOG = "See Log"
    CONFIGURATION = "New Configuration"
    QUICK_ACTIONS = "Quick Actions"

class updated_start_menu(Enum):
    LOCAL = "Local"
    REMOTE = "Remote"
    MANAGE_BRANCHES = "Branches"
    ADVANCED_OPERATIONS = "Operations"
    CONFIGURATION = "New Configuration"
    QUICK_ACTIONS = "Quick Actions"
    WATCH_STATUS = "General View"

class show_menu(Enum):
    SHOW = 'Show'
    GENERAL_VIEW = 'Show General View'
    SHOW_STATUS = 'Show Detailed Status'
    SHOW_DIFFERENCES = 'Show Differences ►'
    SHOW_HISTORY = 'Show History ►'
    SHOW_LOCAL_REPO = 'Show Local Repo'
    SHOW_REMOTE_REPO = 'Show Remote Repo'
    SHOW_BRANCHES = 'Show Branches'

class add_menu(Enum):
    ADD = 'Add'
    ADD_ALL_FILES = 'Add All Files'
    ADD_TRACKED_FILES = 'Add Tracked Files'
    ADD_EXPANDED_FILES = 'Add Expanded Files'
    ADD_LOCAL_BRANCH = 'Add Local Branch'

class history_menu(Enum):
    DETAILED_HISTORY = 'Show Commit History'
    EXPANDED_HISTORY = 'Show Expanded History'
    TRACKING_HISTORY = 'Show Tracking History'
    DIFFERENCES_HISTORY = 'Show Differences History'

class differences_menu(Enum):
    NON_STAGED_DIFFERENCES = 'Show Differences of non staged files'
    STAGED_DIFFERENCES = 'Show Differences of Added files'
    COMMIT_TO_COMMIT_DIFFERENCES = 'Show Differences Between Commits'
    BRANCH_TO_BRANCH_DIFFERENCES = 'Show Differences Between Branches'

# Menu cursor definition
MENU_CURSOR = "▶ "
MENU_CURSOR_STYLE = ("fg_yellow", "bold")

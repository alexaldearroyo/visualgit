from enum import Enum

class branch_menu(Enum):
    BRANCH_LOCAL = 'Local'
    BRANCH_LOCAL_TO_REMOTE = 'Local to Remote'
    BRANCH_REMOTE_TO_LOCAL = 'Remote to Local'
    MANAGE_BRANCHES = 'Manage Branches'

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
    CLONE_BRANCH = 'Join Remote Branch to Local'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'

class manage_branch_menu(Enum):
    MERGE = 'Merge One Branch with Main'
    PULL_BRANCH = 'Yank Remote Branch Changes to Local'
    DELETE_LOCAL_BRANCH = 'Delete Local Branch'
    DELETE_REMOTE_BRANCH = 'Delete Remote Branch'

class main_menu(Enum):
    LOCAL = 'Local'
    LOCAL_TO_REMOTE = 'Local to Remote'
    REMOTE_TO_LOCAL = 'Remote to Local'
    MANAGE_REPOS = 'Manage Repos'

class main_local_menu(Enum):
    CHECK_LOCAL = 'See Local Repos'
    ADD_LOCAL = 'Add a Local Repo'
    COMMIT_LOCAL = 'Commit to Local Repo'

class main_lr_menu(Enum):
    CHECK_REMOTE = 'See Remote Repos'
    LINK = 'Join Local to Remote'
    PUSH = 'Push Changes to Remote'
    COMMIT_AND_PUSH = 'Commit & Push'

class start_menu(Enum):
    WORK_IN_MAIN = "Work in Main"
    WORK_IN_BRANCHES = "Work in Branches"
    CHECK_LOG = "See Log"
    CONFIGURATION = "New Configuration"
    QUICK_ACTIONS = "Quick Actions"

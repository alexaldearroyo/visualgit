import subprocess
import os

from .utils import YELLOW, GREEN, ENDC


def is_git_installed():
    try:
        result = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except Exception as e:
        pass
    return False

def is_git_repo():
    try:
        # Usar git rev-parse para verificar si estamos en un repositorio Git
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
    except Exception:
        return False

def print_git_repo():
    print(f"{YELLOW}The present working directory is already a git repository. No need to create one.{ENDC}")

def print_not_git_repo():
    print(f"{YELLOW}The present working directory is not a git repository, please create one to proceed.{ENDC}\nTo create one: Quick actions -> Add a local repo")

def is_connected_to_remote():
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def print_connected_to_remote():
    print(f"{YELLOW}The local repository is already connected to a remote repository.{ENDC}")

def print_not_connected_to_remote():
    print(f"{YELLOW}The local repository is not connected to a remote repository. Please connect it to proceed.{ENDC}\nTo connect: Work in main -> Link local repo with remote")

def current_branch():
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except Exception:
        return None

def is_local_branch_connected_to_remote(branch_name):
    try:
        result = subprocess.run(["git", "for-each-ref", "--format", '%(upstream:short)', f"refs/heads/{branch_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip() != ""
    except Exception:
        return False


def get_current_branch():
    try:
        result = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None

def is_current_branch_main():
    branch = current_branch()
    return branch == "main"

def has_commits():
    try:
        result = subprocess.run(["git", "rev-parse", "--verify", "HEAD"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking commits: {e}")
        return False

def print_not_commits():
    print(f"{YELLOW}To work with branches, you need to commit first. Please commit to proceed.{ENDC}\nTo commit locally: Quick actions -> Commit to local repo")

def list_local_branches():
    try:
        result = subprocess.run(["git", "branch"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        branches = result.stdout.decode('utf-8')
        print("Available branches:")
        print(branches)
    except subprocess.CalledProcessError as e:
        print(f"Error listing branches: {e}")

import subprocess
import os

from .utils import YELLOW, GREEN, ENDC, RED


def is_git_installed():
    try:
        result = subprocess.run(["git", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return True
    except Exception as e:
        pass
    return False

def is_git_repo():
    """Comprueba si el directorio actual es un repositorio Git"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip() == "true"
    except:
        # El directorio actual no es un repositorio Git
        return False

def print_git_repo():
    print(f"{YELLOW}The present working directory is already a git repository. No need to create one.{ENDC}")

def print_not_git_repo():
    """Imprime un mensaje de error indicando que el directorio actual no es un repositorio Git"""
    print(f"{RED}The present working directory is not a git repository, please create one to proceed.{ENDC}")
    print(f"{YELLOW}To create one: Local -> Add a local repo{ENDC}")

def is_connected_to_remote():
    try:
        result = subprocess.run(["git", "remote", "get-url", "origin"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False

def print_connected_to_remote():
    print(f"{YELLOW}The local repository is already connected to a remote repository.{ENDC}")

def print_not_connected_to_remote():
    print(f"{YELLOW}The local repository is not connected to a remote repository. Please connect it to proceed.{ENDC}\nTo connect: Remote -> Join Local to Remote")

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

def has_unstaged_changes():
    """Checks if there are unstaged changes in the repository."""
    try:
        result = subprocess.run(
            ["git", "diff", "--quiet"],
            capture_output=True
        )
        return result.returncode != 0
    except Exception:
        return False

def has_staged_changes():
    """Checks if there are changes staged for commit."""
    try:
        result = subprocess.run(
            ["git", "diff", "--quiet", "--staged"],
            capture_output=True
        )
        return result.returncode != 0
    except Exception:
        return False

def has_stash():
    """Checks if there are saved stashes."""
    try:
        result = subprocess.run(
            ["git", "stash", "list"],
            capture_output=True,
            text=True
        )
        return bool(result.stdout.strip())
    except Exception:
        return False

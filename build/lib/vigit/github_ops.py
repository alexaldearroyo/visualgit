import subprocess
import requests
from .utils import YELLOW, GREEN, ENDC

def get_github_token():
    try:
        result = subprocess.run(
            ["git", "config", "--global", "github.token"],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception:
        return None

def create_github_repository(name, description="", private=False):
    token = get_github_token()
    if not token:
        print(f"{YELLOW}GitHub token not found. Please configure one in the configuration menu.{ENDC}")
        print("Go to: Configuration > GitHub API Configuration")
        return False

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    data = {
        'name': name,
        'description': description,
        'private': private
    }

    try:
        response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            json=data
        )

        if response.status_code == 201:
            repo_url = response.json()['html_url']
            print(f"{GREEN}Repository successfully created: {repo_url}{ENDC}")
            return repo_url
        else:
            error_message = response.json().get('message', 'Unknown error')
            print(f"{YELLOW}Error creating repository: {error_message}{ENDC}")

            # Detect duplicate name error
            if "name already exists" in error_message or "Repository creation failed" in error_message:
                print("\nThe repository name already exists in your GitHub account.")
                print("Solution: Try a different name for your repository.")
            # Detect authentication problems
            elif "Resource not accessible by integration" in error_message or "Bad credentials" in error_message:
                print("\nPossible solutions:")
                print("1. Verify that your token has the correct permissions:")
                print("   - Go to https://github.com/settings/tokens")
                print("   - Create a new token (classic)")
                print("   - Check the full 'repo' checkbox")
                print("2. Configure the new token in:")
                print("   Configuration > GitHub API Configuration")

            return False
    except Exception as e:
        print(f"{YELLOW}Error connecting to GitHub: {e}{ENDC}")
        return False

def delete_github_repository(owner, repo):
    """
    Delete a GitHub repository using the GitHub API.

    Args:
        owner (str): The GitHub username/owner
        repo (str): The repository name

    Returns:
        bool: True if successful, False otherwise
    """
    token = get_github_token()
    if not token:
        print(f"{YELLOW}GitHub token not found. Please configure one in the configuration menu.{ENDC}")
        print("Go to: Configuration > GitHub API Configuration")
        return False

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.delete(
            f'https://api.github.com/repos/{owner}/{repo}',
            headers=headers
        )

        if response.status_code == 204:  # Success, no content
            print(f"{GREEN}Repository {owner}/{repo} has been successfully deleted.{ENDC}")
            return True
        else:
            error_message = "Unknown error"
            try:
                error_data = response.json()
                if 'message' in error_data:
                    error_message = error_data['message']
            except:
                pass

            print(f"{YELLOW}Error deleting repository: {error_message}{ENDC}")

            # Provide helpful troubleshooting information
            if "Not Found" in error_message:
                print("\nThe repository could not be found. Please check:")
                print("1. That you have the correct owner/repository name")
                print("2. That you have permission to delete this repository")
            elif "Bad credentials" in error_message:
                print("\nAuthentication failed. Please check your GitHub token:")
                print("1. Go to: Configuration > GitHub API Configuration")
                print("2. Update your token with the correct permissions")
            elif "Must have admin rights" in error_message:
                print("\nYou don't have permission to delete this repository.")
                print("You must be an owner or have admin permissions.")

            return False

    except Exception as e:
        print(f"{YELLOW}Error connecting to GitHub: {e}{ENDC}")
        return False

def get_github_username():
    """
    Get the GitHub username of the current user.

    Returns:
        str: The GitHub username or None if not found
    """
    token = get_github_token()
    if not token:
        return None

    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        response = requests.get(
            'https://api.github.com/user',
            headers=headers
        )

        if response.status_code == 200:
            return response.json().get('login')
        else:
            return None
    except:
        return None

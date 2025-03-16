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

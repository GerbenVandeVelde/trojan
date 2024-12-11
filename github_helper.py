from github import Github  # PyGithub library
import os

GITHUB_TOKEN = "your_personal_access_token"
REPO_NAME = "your_username/TrojanFramework"

def fetch_config():
    """Fetch configuration from GitHub."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    content = repo.get_contents("config/config.json")
    return json.loads(content.decoded_content)

def upload_results(file_path):
    """Upload results to the GitHub repository."""
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)
    with open(file_path, 'r') as file:
        content = file.read()
    try:
        repo.create_file(f"data/results/{os.path.basename(file_path)}", "Add results", content)
    except:
        # File already exists, update it instead.
        file = repo.get_contents(f"data/results/{os.path.basename(file_path)}")
        repo.update_file(file.path, "Update results", content, file.sha)

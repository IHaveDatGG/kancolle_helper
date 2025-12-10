from pathlib import Path
from dulwich import porcelain
from dulwich.repo import Repo

def update(repo_path=Path.cwd(), remote_url="https://github.com/IHaveDatGG/kancolle_helper.git", branch="main"):
    """Auto-update this project from GitHub."""
    repo = Repo(repo_path)

    print("Fetching remote updates...")
    porcelain.fetch(repo, remote_url)

    print("Trying to pull...")
    porcelain.pull(repo, remote_url, branch)

    print("Already up to date.")

if __name__ == "__main__":
    update()

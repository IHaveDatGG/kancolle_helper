from pathlib import Path
from dulwich import porcelain
from dulwich.errors import NotGitRepository
from dulwich.repo import Repo


def get_or_init_repo(repo_path):
    try:
        return Repo(repo_path)
    except NotGitRepository:
        return Repo.init(repo_path)


def update(repo_path=Path.cwd(), remote_url="https://github.com/IHaveDatGG/kancolle_helper.git"):
    """Auto-update this project from GitHub."""
    print("Trying to update...")
    repo = get_or_init_repo(repo_path)
    porcelain.pull(repo=repo, remote_location=remote_url, force=True)
    print("Already up to date.")


if __name__ == "__main__":
    update()

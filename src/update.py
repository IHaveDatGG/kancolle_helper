from pathlib import Path
from dulwich import porcelain

def update(repo_path=Path.cwd(), remote_url="https://github.com/IHaveDatGG/kancolle_helper.git"):
    """Auto-update this project from GitHub."""
    print("Trying to update...")
    porcelain.pull(repo=repo_path, remote_location=remote_url, force=True)
    print("Already up to date.")


if __name__ == "__main__":
    update()

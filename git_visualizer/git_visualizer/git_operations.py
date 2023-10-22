## git_operations.py
from git import Repo
from models import Version
from typing import Optional

class GitOperations:
    def __init__(self, repo_path: str = '.'):
        self.repo = Repo(repo_path)

    def save_version(self, version: Version):
        # Create a new file with the version content
        with open(f'{version.id}.txt', 'w') as f:
            f.write(version.content)

        # Add the file to the staging area
        self.repo.git.add(f'{version.id}.txt')

        # Commit the changes
        self.repo.git.commit('-m', f'Add version {version.id}')

    def get_version(self, version_id: int) -> Optional[str]:
        try:
            # Get the commit that added the version
            commit = self.repo.git.log('--', f'{version_id}.txt', n=1, format="%H")

            # Get the version content from the commit
            version_content = self.repo.git.show(f'{commit}:{version_id}.txt')

            return version_content
        except Exception:
            return None

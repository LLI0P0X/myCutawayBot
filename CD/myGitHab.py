import subprocess
import os
import sys

project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_directory)
import config


def pull(branch: str = 'master'):
    subprocess.run(f'sudo git pull {config.gitHabUrl}.git {branch}', shell=True)


if __name__ == "__main__":
    pull()

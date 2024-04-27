import subprocess
import config


def pull(branch: str = 'master'):
    subprocess.run(f'git pull {config.gitHabUrl}.git {branch}')

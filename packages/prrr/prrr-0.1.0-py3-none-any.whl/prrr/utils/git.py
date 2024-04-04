import os


def read_last_commit_message():
    # read the last commit message
    return os.popen("git log -1 --pretty=%B").read().strip()


def read_last_commits():
    # read the last commit message
    return os.popen("git log --pretty=%B").read().strip()


def get_git_remote_url():
    git_uri = os.popen("git config --get remote.origin.url").read().strip()
    # strip : at the end
    if git_uri.endswith(".git"):
        git_uri = git_uri[:-4]
    # replace : with /
    git_uri = git_uri.replace(":", "/")
    # replace git@github.com with https://github.com
    git_uri = git_uri.replace("git@github.com", "https://github.com")
    return git_uri


def get_current_branch():
    return os.popen("git rev-parse --abbrev-ref HEAD").read().strip()

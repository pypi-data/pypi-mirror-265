import os
from git_ai.cmd.ai_repo import AIRepo
import pygit2
from pygit2 import discover_repository

from git_ai.errors.errors import GitAIException, InitError


def init():
    try:
        if not discover_repository(os.getcwd()):
            print(
                f"Creating Git Repository and initializing Git AI Repository in ${os.getcwd()}")
            pygit2.init_repository(os.getcwd(), bare=False)
        repo = AIRepo(os.getcwd())
        print('Initialized Git AI repository in %s' % repo.workdir)
        repo.init_ai_repo()
    except GitAIException as e:
        raise e
    except Exception as e:
        raise InitError.failed_to_init_repo() from e

# Common test fixtures
#
# -----------------------------------

import pytest


@pytest.fixture(scope='session')
def default_shell(target, strategy):
    """
    Bring the default target in the 'shell' state and provide a ShellDriver instance.
    """
    strategy.transition("shell")
    shell = target.get_driver("ShellDriver")
    return shell


@pytest.fixture(scope='session')
def default_ssh(target, strategy):
    """
    Bring the default target in the 'shell' state and provide a SSHDriver instance.
    """
    strategy.transition("shell")
    ssh = target.get_driver("SSHDriver")
    return ssh

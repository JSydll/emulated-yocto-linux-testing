# Common test fixtures
#
# -----------------------------------

import pytest

from typing import Any

from labgrid import Target
from labgrid.driver import ShellDriver, SSHDriver

@pytest.fixture(scope='session')
def default_shell(target: Target, strategy: Any) -> ShellDriver:
    """
    Bring the default target in the 'shell' state and provide a ShellDriver instance.
    """
    strategy.transition("shell")
    shell = target.get_driver("ShellDriver")
    return shell


@pytest.fixture(scope='session')
def default_ssh(target: Target, strategy: Any) -> ShellDriver:
    """
    Bring the default target in the 'shell' state and provide a SSHDriver instance.
    """
    strategy.transition("shell")
    ssh = target.get_driver("SSHDriver")
    return ssh

# Tests for reaching the target from the outside
#
# -----------------------------------

import pytest

from labgrid.driver import ShellDriver, SSHDriver

@pytest.mark.smoketest
@pytest.mark.on_latest
def test_shell_command(default_shell: ShellDriver) -> None:
    default_shell.run("true")

@pytest.mark.smoketest
@pytest.mark.on_latest
def test_ssh_command(default_ssh: SSHDriver) -> None:
    default_ssh.run("true")

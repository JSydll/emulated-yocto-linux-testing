# Tests for reaching the target from the outside
#
# -----------------------------------

import pytest


@pytest.mark.smoketest
@pytest.mark.on_latest
def test_shell_command(default_shell):
    default_shell.run("true")

@pytest.mark.smoketest
@pytest.mark.on_latest
def test_ssh_command(default_ssh):
    default_ssh.run("true")

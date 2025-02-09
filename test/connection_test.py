# Tests for reaching the target from the outside
#
# -----------------------------------

import pytest


@pytest.mark.smoketest
def test_shell_command(shell_instance):
    shell_instance.run("true")

@pytest.mark.smoketest
def test_ssh_command(ssh_instance):
    ssh_instance.run("true")

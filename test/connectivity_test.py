# Tests for reaching the target from the outside
#
# -----------------------------------

import pytest

from labgrid.driver import ShellDriver, SSHDriver

@pytest.mark.smoketest
def test_shell_command(default_shell: ShellDriver) -> None:
    """Ensures the target can be reached via serial."""
    default_shell.run("true")

@pytest.mark.nightly
@pytest.mark.emulation_only
def test_ssh_command(default_ssh: SSHDriver) -> None:
    """Ensures the target can be reached via SSH.
    
    Note: It probably makes sense to also test this in a smoketest and on hardware too,
    but let's assume the network is stable and this feature only depends on proper configuration
    of the ssh server in the image. Then it could be argued that execution on emulation is enough.
    """
    default_ssh.run("true")

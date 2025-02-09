# Update related test fixtures
#
# -----------------------------------

import pytest

import environment.update as update

@pytest.fixture(scope='function')
def update_flow(target, shell_instance, ssh_instance):
    """
    Initializes and returns an UpdateFlow instance.
    Args:
        target: The target device or system to be updated.
        shell_instance: An instance of the Shell class for executing shell commands.
        ssh_instance: An instance of the SSH class for managing SSH connections.
    Returns:
        UpdateFlow: An instance of the UpdateFlow class initialized with the provided arguments.
    """
    return update.UpdateFlow(target, shell_instance, ssh_instance)
# Update related test fixtures
#
# 
#
# -----------------------------------

import pytest

from typing import Callable
from labgrid import Environment

import environment.update as update
import environment.software_version as versions

def get_update_flow(env: Environment, preset_software_version: versions.SoftwareVersion) -> update.UpdateFlow:
    """
    Initializes and returns an update flow for a given environment and software version.

    This function determines the appropriate target based on the provided software version.
    If the current software version on the target does not match the preset software version,
    it forces the installation of the desired version and verifies the update.
    
    Args:
        env: The environment object that provides access to targets and their configurations.
        preset_software_version: The desired software version to be installed on the target.
    
    Returns:
        update.UpdateFlow: An object representing the update flow for the target.
    """
    target = None

    if preset_software_version != versions.SoftwareVersion.latest:
        # We expect preset targets to be named according to the software version they are in.
        target = env.get_target(preset_software_version.name)
    
    if target is None:
        # Fallback to default target (latest) also if the environment has no preset targets.
        target = env.get_target()
    
    strategy = target.get_strategy()
    strategy.transition("shell")

    shell = target.get_driver("ShellDriver")
    target.activate(shell)

    ssh = target.get_driver("SSHDriver")
    target.activate(ssh)

    update_flow = update.UpdateFlow(target, shell, ssh)

    current_version = versions.get_current_software_version(ssh)
    if current_version != preset_software_version:
        # If the target is not running the desired software version, force install it.
        update_flow.enable_force_install()
        update_flow.execute_all_steps(preset_software_version)

    # Now, the target should be in the desired state
    return update_flow
    


def create_update_fixture(software_version: versions.SoftwareVersion) -> Callable[[Environment], update.UpdateFlow]:
    @pytest.fixture(scope='function')
    def _update_fixture(env: Environment) -> update.UpdateFlow:
        """
        Initializes and returns an UpdateFlow instance for running updates
        started from the specified software version.
        """
        return get_update_flow(env, software_version)
    return _update_fixture

update_manufacturing: Callable[[Environment], update.UpdateFlow] = create_update_fixture(versions.SoftwareVersion.manufacturing)
update_lts: Callable[[Environment], update.UpdateFlow] = create_update_fixture(versions.SoftwareVersion.lts)
update_latest: Callable[[Environment], update.UpdateFlow] = create_update_fixture(versions.SoftwareVersion.latest)

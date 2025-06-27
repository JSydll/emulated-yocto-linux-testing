# Tests for the (hypothetical) Alive Service
#
# The service would send cyclic alive messages and respond to synchronization requests
# over several connections, e.g. CAN. CAN is taken to illustrate the considerations when
# attempting to emulate peripherals.
# -----------------------------------

import pytest

from labgrid.driver import SSHDriver

_SERVICE_SYSTEMD_UNIT: str = "alive.service"


@pytest.mark.smoketest
@pytest.mark.emulation_only
@pytest.mark.lg_feature("os-canbus")
def test_alive_service_bootstrapping(default_ssh: SSHDriver) -> None:
    """
    Ensure that the Alive Service is automatically started on boot and comes up healthy.

    Note: The Alive Service expects can0 and can1 to be available.
    """
    default_ssh.run(f"systemctl status {_SERVICE_SYSTEMD_UNIT}")
    # Extend with more checks...


@pytest.mark.nightly
@pytest.mark.lg_feature("peripherals-canbus")
def test_alive_service_acks_request_for_syn() -> None:
    """
    Sends a SYN request to the target via CAN and expects to receive an ACK from the Alive Service.

    Note: Can only be executed on targets with physical CAN connections.
    """
    # Implement test logic...

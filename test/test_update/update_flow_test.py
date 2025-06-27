# Tests for installing the current software
#
# -----------------------------------

import pytest

import environment.update as update

from environment.software_version import SoftwareVersion

# All tests in this module are related to the update feature.
pytestmark = [pytest.mark.lg_feature("os-base"), pytest.mark.update]

@pytest.mark.release
@pytest.mark.hardware_only
@pytest.mark.parametrize('version_to_install',
        [SoftwareVersion.lts, SoftwareVersion.latest]
    )
def test_update_from_manufacturing_succeeds(update_manufacturing: update.UpdateFlow, version_to_install: SoftwareVersion) -> None:
    """
    Test that the happy path update from manufacturing to the specified version succeeds.
    """
    update_manufacturing.execute_all_steps(version_to_install)


@pytest.mark.nightly
@pytest.mark.parametrize('version_to_install',
        [SoftwareVersion.lts, SoftwareVersion.latest]
    )
def test_update_from_lts_succeeds(update_lts: update.UpdateFlow, version_to_install: SoftwareVersion) -> None:
    """
    Test that the happy path update from LTS to the specified version succeeds.
    """
    update_lts.execute_all_steps(version_to_install)


@pytest.mark.smoketest
@pytest.mark.parametrize('version_to_install',
        [SoftwareVersion.latest]
    )
def test_update_from_latest_succeeds(update_latest: update.UpdateFlow, version_to_install: SoftwareVersion) -> None:
    """
    Test that the happy path update from latest to the specified version succeeds.
    """
    update_latest.execute_all_steps(version_to_install)
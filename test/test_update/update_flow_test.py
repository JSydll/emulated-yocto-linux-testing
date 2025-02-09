# Tests for installing the current software
#
# -----------------------------------

import pytest

import environment.update as update

pytestmark = [pytest.mark.update, pytest.mark.lg_feature('update')]


@pytest.mark.smoketest
def test_successful_update_installation(update_flow):
    """
    Test the successful, undisturbed update flow from current to current
    software version.
    """
    update_flow.deploy_bundle(update.BundleVersion.current)
    update_flow.install_bundle()
    update_flow.activate_update()
    update_flow.verify_update()

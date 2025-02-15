# ...
#
# -----------------------------------

import attr
import json

from dataclasses import dataclass
from labgrid import Target
from labgrid.driver import ShellDriver, SSHDriver
from labgrid.factory import target_factory
from labgrid.resource import Resource

import environment.software_version as versions


_UPDATE_INSTALLATION_TIMEOUT = 300

@target_factory.reg_resource
@attr.s(eq=False)
class UpdateBundles(Resource):
    latest: str = attr.ib()
    lts: str = attr.ib()
    manufacturing: str = attr.ib()


@dataclass
class SlotState:
    """
    Represents the state of a slot in the system.

    Attributes:
        good (bool): Indicates whether the slot is in a good state.
        booted (bool): Indicates whether the slot has been booted.
    """
    good: bool
    booted: bool


class UpdateFlow:
    """
    Implements the control flow and verification of the update process.
    """
    
    def __init__(self, target: Target, shell: ShellDriver, ssh: SSHDriver) -> None:
        self.target = target
        self.shell = shell
        self.ssh = ssh

        self._slot_states = {}
        self._update_slot_states()

    def _update_slot_states(self) -> None:
        self.target.activate(self.shell)

        captured_output, _, _ = self.shell.run('rauc status --output-format=json')
        status = json.loads(captured_output[0])
        slots = status['slots']
        
        for slot in slots:
            # Note that the slot dict will always contain only a single item.
            for _, slot_info in slot.items():
                good = slot_info['boot_status'] == 'good'
                booted = slot_info['state'] == 'booted'
                self._slot_states[slot_info['bootname']] = SlotState(good=good, booted=booted)
        
    def deploy_bundle(self, version: versions.SoftwareVersion) -> None:
        """
        Deploys the specified update bundle version to the target device.

        Args:
            version: The version of the bundle to deploy.

        Raises:
            NotImplementedError: If the specified version is not supported.

        """
        bundles = self.target.get_resource(UpdateBundles)

        if version == versions.SoftwareVersion.lts:
            src_path = bundles.lts
        elif version == versions.SoftwareVersion.latest:
            src_path = bundles.latest
        elif version == versions.SoftwareVersion.manufacturing:
            # Note: This is usually only used to reset targets to the manufacturing state.
            src_path = bundles.manufacturing
        else:
            raise NotImplementedError(f"Version {version} not supported yet.")

        self.target.activate(self.ssh)
        self.ssh.put(src_path, '/tmp/update-bundle.raucb')

    def enable_force_install(self) -> None:
        """Enable the force-install flag for the ongoing update (once).

        This is only meant for testing purposes, given downgrades are usually forbidden.
        """
        # The current implementation does not prevent downgrades - so nothing to do here.
        # A common approach would be to create a temporary flag file on the device to allow
        # the downgrade and remove it immediately when it's "read" by the update flow.
        pass

    def install_bundle(self) -> None:
        """
        Installs the update bundle on the target device.

        Raises:
            Any exceptions raised by the shell instance.
        """
        self.target.activate(self.shell)
        self.shell.run('rauc install /tmp/update-bundle.raucb', timeout=_UPDATE_INSTALLATION_TIMEOUT)

    def activate_update(self) -> None:
        """
        Activates the update process on the target device.

        Raises:
            Any exceptions raised by the shell instance.
        """
        self.target.activate(self.shell)
        self.shell.run('reboot')
        # Make sure the drivers do not assume a false target state.
        self.target.deactivate(self.shell)
        self.target.deactivate(self.ssh)

    def verify_update(self) -> None:
        """
        Verifies the update process by checking the state of the slots before and after the update.

        Raises:
            AssertionError: If the expected slot is not in a good state or is not booted.
        """
        slot_states_before = self._slot_states.copy()
        self._update_slot_states()
        
        for slot, state_before in slot_states_before.items():
            if state_before.booted:
                expected_slot = 'B' if slot == 'A' else 'A'
                state = self._slot_states.get(expected_slot)
                assert state and state.good and state.booted, (
                    f"After update from slot {slot} [{self._slot_states.get(slot)}]: "
                    f"Slot {expected_slot} is not in the expected state after the update [{state}]."
                )

    def execute_all_steps(self, version: versions.SoftwareVersion) -> None:
        """
        Executes all steps of the update process for the specified version.

        Args:
            version: The version of the bundle to deploy.

        Raises:
            Any exceptions raised by the shell instance.
        """
        self.deploy_bundle(version)
        self.install_bundle()
        self.activate_update()
        self.verify_update()


# ...
#
# -----------------------------------

import attr
import enum
import json

from dataclasses import dataclass
from labgrid.factory import target_factory
from labgrid.resource import Resource


_UPDATE_INSTALLATION_TIMEOUT = 300

@target_factory.reg_resource
@attr.s(eq=False)
class UpdateBundles(Resource):
    current = attr.ib()


class BundleVersion(enum.Enum):
    current = 0


@dataclass
class SlotState:
    good: bool
    booted: bool


class UpdateFlow:
    """
    Implements the control flow and verification of the update process.
    """
    
    def __init__(self, target, shell, ssh):
        self.target = target
        self.shell = shell
        self.ssh = ssh

        self._slot_states = {}
        self._update_slot_states()

    def _update_slot_states(self):
        self.target.activate(self.shell)

        captured_output, _, _ = self.shell.run("rauc status --output-format=json")
        status = json.loads(captured_output[0])
        slots = status['slots']
        
        for slot in slots:
            # Note that the slot dict will always contain only a single item.
            for _, slot_info in slot.items():
                good = slot_info['boot_status'] == 'good'
                booted = slot_info['state'] == 'booted'
                self._slot_states[slot_info['bootname']] = SlotState(good=good, booted=booted)
        
    def deploy_bundle(self, version: BundleVersion):
        """
        Deploys the specified update bundle version to the target device.

        Args:
            version: The version of the bundle to deploy. Currently, only BundleVersion.current is supported.

        Raises:
            NotImplementedError: If the specified version is not supported.

        """
        bundles = self.target.get_resource(UpdateBundles)

        if version == BundleVersion.current:
            src_path = bundles.current
        else:
            raise NotImplementedError(f"Version {version} not supported yet.")

        self.ssh.put(src_path, '/tmp/update-bundle.raucb')

    def install_bundle(self):
        """
        Installs the update bundle on the target device.

        Raises:
            Any exceptions raised by the shell instance.
        """
        self.target.activate(self.shell)
        self.shell.run("rauc install /tmp/update-bundle.raucb", timeout=_UPDATE_INSTALLATION_TIMEOUT)

    def activate_update(self):
        """
        Activates the update process on the target device.

        Raises:
            Any exceptions raised by the shell instance.
        """
        self.target.activate(self.shell)
        self.shell.run("reboot")
        self.target.deactivate(self.shell)

    def verify_update(self):
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
        

# ...
#
# -----------------------------------

import enum
import re

_EXPECTED_LATEST_VERSION: str = '3.1'
_EXPECTED_LTS_VERSION: str = '3.0'
_EXPECTED_MANUFACTURING_VERSION: str = '1.0'

_SOFTWARE_VERSION_FILE: str = '/etc/buildinfo'


class SoftwareVersion(enum.Enum):
    latest = _EXPECTED_LATEST_VERSION
    lts = _EXPECTED_LTS_VERSION
    manufacturing = _EXPECTED_MANUFACTURING_VERSION


def get_current_software_version(ssh):
    """Read the currently running software version from the target.

    Args:
        ssh: Connection to the target

    Returns:
        SoftwareVersion: Running software version.
    """
    out, _, _ = ssh.run(f"cat {_SOFTWARE_VERSION_FILE}")
    version = re.search(r'SOFTWARE_VERSION\s*=\s*(\d\.\d)', ''.join(out))
    
    if version is None:
        raise ValueError(f"Failed to read software version from '{_SOFTWARE_VERSION_FILE}'")
    
    return SoftwareVersion(version.group(1))
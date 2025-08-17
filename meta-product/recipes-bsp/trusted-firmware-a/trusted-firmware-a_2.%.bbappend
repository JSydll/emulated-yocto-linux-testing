# Configuration of the TF-A extended firmware package
#
# Heavily inspired from Linaro's Trusted Substrate implementation
# (https://gitlab.com/Linaro/trustedsubstrate/meta-ts) and the meta-arm layer.

# --- START of build hacks ---
S = "${UNPACKDIR}/git"
# In addition, trusted-firmware-a.inc:53 needed to be patched out or adjusted for immediate expansion.
# --- END of build hacks ---

COMPATIBLE_MACHINE:virt-aarch64 = "virt-aarch64"

# Note:
# Several configurations are already provided for aarch64:qemuall in meta-arm/**/trusted-firmware-a_%.bbappend

TFA_PLATFORM:virt-aarch64 = "qemu"
#TFA_SPD = "opteed"
TFA_UBOOT:virt-aarch64 = "1"
TFA_INSTALL_TARGET:virt-aarch64 = "flash.bin"

# Clean before building
TFA_BUILD_TARGET:prepend:aarch64:qemuall = " clean "

do_compile:append:virt-aarch64() {
    # meta-arm provides an almost identical implementation, but per machine. Documented by
    # https://git.trustedfirmware.org/TF-A/trusted-firmware-a.git/tree/docs/plat/qemu.rst
    dd if=/dev/zero of=${BUILD_DIR}/flash.bin bs=1M count=64
    dd if=${BUILD_DIR}/bl1.bin of=${BUILD_DIR}/flash.bin bs=4096 conv=notrunc
    dd if=${BUILD_DIR}/fip.bin of=${BUILD_DIR}/flash.bin seek=64 bs=4096 conv=notrunc
}
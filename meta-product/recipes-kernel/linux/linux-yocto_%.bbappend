FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append:virt-aarch64 = " \
    file://canbus.cfg \
"

# UEFI / secure boot related configuration already pulled in by meta-arm.
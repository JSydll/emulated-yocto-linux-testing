# Overwrite the DTS for the qemuarm64 machine, which is the base for our custom machine definition
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append:virt-aarch64 = " \
    file://canbus.cfg \
"
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " \
    file://bootflow.cfg \
"

# Fix proposed in https://github.com/agherzan/meta-raspberrypi/issues/1306 to resolve
# failing boot when uncompressing the kernel on raspberrypi 4 (and scarthgap).
SRC_URI:append:raspberrypi4 = " \
    file://memorysize.cfg \
"

# UEFI-based secure boot
# Note that for QEMU does not support authenticated EFI variables, due to missing RPMB emulation.
# For this reason, the secrets must be baked into the binary, which is implemented in meta-arm/recipes-bsp/u-boot/u-boot_%.bbappend.
# We don't use a boot menu based boot though, so uefi-secureboot.cfg ais overwritten here.
SRC_URI:append:virt-aarch64 = " \
    file://uefi-secureboot.cfg \
    file://uefi-insecure-vars.cfg \
"

# Remove boot path via bootloader script
UBOOT_ENV:virt-aarch64 = ""
UBOOT_ENV_SUFFIX:virt-aarch64 = ""

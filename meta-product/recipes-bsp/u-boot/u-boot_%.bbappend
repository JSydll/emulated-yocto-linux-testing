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
SRC_URI:append:virt-aarch64 = " \
    file://uefi-secure-boot.cfg \
"

# Remove boot path via bootloader script
UBOOT_ENV:virt-aarch64 = ""
UBOOT_ENV_SUFFIX:virt-aarch64 = ""

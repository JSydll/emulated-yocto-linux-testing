SUMMARY = "..."
IMAGE_LINGUAS = " "

LICENSE = "MIT"

inherit core-image uki-with-profiles

require conf/product.conf

# Testing support
DEPENDS:append = "labgrid-env-config"

# Image contents
IMAGE_INSTALL:append = " \
    packagegroup-core-boot \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    rauc \
    e2fsprogs-mke2fs \
    mtd-utils \
    devicetree-qemuarm \
"

IMAGE_INSTALL:append:virt-aarch64 = " \
    alive-service \
"

IMAGE_FSTYPES = "tar.bz2 wic.qcow2"
WKS_FILE = "secure-system-image.wks.in"

# UKI specification
INITRAMFS_IMAGE = "core-image-minimal-initramfs"
KERNEL_DEVICETREE = "devicetree/qemuarm64.dtb"
# No default commandline - profiles are used instead
UKI_CMDLINE = ""
#UKI_SB_KEY = "${SBSIGN_KEY}"
#UKI_SB_CERT = "${SBSIGN_CERT}"

# Definition of two profiles to be embedded in the UKI, allowing a common UKI to be used for both update slots
UKI_PROFILES = "boot_a boot_b"
UKI_PROFILE_boot_a[name] = "${BOOT_A_PROFILE}"
UKI_PROFILE_boot_a[meta] = "TITLE=Profile for booting with rootFS A ID=${BOOT_A_PROFILE}"
UKI_PROFILE_boot_a[cmdline] = "root=PARTUUID=${ROOTFS_A_PARTUUID} rootfstype=ext4 rauc.slot=${ROOTFS_A_NAME}"
UKI_PROFILE_boot_b[name] = "${BOOT_B_PROFILE}"
UKI_PROFILE_boot_b[meta] = "TITLE=Profile for booting with rootFS B ID=${BOOT_B_PROFILE}"
UKI_PROFILE_boot_b[cmdline] = "root=PARTUUID=${ROOTFS_B_PARTUUID} rootfstype=ext4 rauc.slot=${ROOTFS_B_NAME}"

IMAGE_BOOT_FILES = "${UKI_FILENAME}"

# Dependencies for image creation and deployment of all relevant artifacts
do_image_wic[depends] += " \
    u-boot:do_deploy \
"

# While not directly depending on it, running the emulation requires the ESP
do_image_complete[depends] += " \
    trusted-firmware-a:do_deploy \
    efi-system-partition-image:do_image_complete \
"
SUMMARY = "..."
IMAGE_LINGUAS = " "

LICENSE = "MIT"

inherit core-image uki-with-profiles sbsign

# Testing support
DEPENDS:append = "labgrid-env-config"

# Image features
OVERLAYFS_ETC_MOUNT_POINT = "/data"
OVERLAYFS_ETC_FSTYPE = "ext4"
OVERLAYFS_ETC_DEVICE:virt-aarch64 = "/dev/vdb5"

IMAGE_FEATURES:append:virt-aarch64 = " \
    read-only-rootfs \
    overlayfs-etc \
"

# Image contents
IMAGE_INSTALL:append = " \
    packagegroup-core-boot \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    rauc \
    e2fsprogs-mke2fs \
"

IMAGE_INSTALL:append:raspberrypi4-64 = " \
    devicetree-qemuarm \
"

# The u-boot-efivars-sync is a development-only workaround!
IMAGE_INSTALL:append:virt-aarch64 = " \
    efivar \
    efibootmgr \
    u-boot-efivars-sync \
    alive-service \
"

IMAGE_FSTYPES = "squashfs wic.qcow2"
WKS_FILE = "secure-system-image.wks.in"

# dm-verity setup
INITRAMFS_IMAGE = "dm-verity-image-initramfs"

# UKI specification
KERNEL_DEVICETREE = "devicetree/qemuarm64.dtb"
do_uki[depends] += " devicetree-qemuarm:do_deploy "
# No default commandline - profiles are used instead
UKI_CMDLINE = ""
UKI_SB_KEY = "${SBSIGN_KEY}"
UKI_SB_CERT = "${SBSIGN_CERT}"

# Definition of two profiles to be embedded in the UKI, allowing a common UKI to be used for both update slots
CMDLINE_BASE = "rootfstype=squashfs verity=1"
UKI_PROFILES = "boot_a boot_b"
UKI_PROFILE_boot_a[name] = "boot-profile-a"
UKI_PROFILE_boot_a[meta] = "TITLE=Profile for booting with rootFS A ID=boot-profile-a"
UKI_PROFILE_boot_a[cmdline] = "${CMDLINE_BASE} root=PARTUUID=020977a6-f364-4499-a61c-bc4708908265 rauc.slot=system0"
UKI_PROFILE_boot_b[name] = "boot-profile-b"
UKI_PROFILE_boot_b[meta] = "TITLE=Profile for booting with rootFS B ID=boot-profile-b"
UKI_PROFILE_boot_b[cmdline] = "${CMDLINE_BASE} root=PARTUUID=99979fdc-3a79-452d-a62a-cf09030f241b rauc.slot=system1"

IMAGE_BOOT_FILES = "${UKI_FILENAME}"

# Allow reuse of the partition images already created by wic
do_copy_wic_partitions() {
    wic_workdir="${WORKDIR}/build-wic"
    cp -v "${wic_workdir}"/*.direct.p1 "${IMGDEPLOYDIR}"/${IMAGE_BASENAME}${IMAGE_MACHINE_SUFFIX}${IMAGE_NAME_SUFFIX}.uki.squashfs
    cp -v "${wic_workdir}"/*.direct.p3 "${IMGDEPLOYDIR}"/${IMAGE_BASENAME}${IMAGE_MACHINE_SUFFIX}${IMAGE_NAME_SUFFIX}.rootfs.squashfs.verity
}
addtask copy_wic_partitions after do_image_wic before do_image_complete

# Dependencies for image creation and deployment of all relevant artifacts
do_image_wic[depends] += " \
    u-boot:do_deploy \
"

# While not directly depending on it, running the emulation requires the ESP
do_image_complete[depends] += " \
    trusted-firmware-a:do_deploy \
    efi-system-partition-image:do_image_complete \
"
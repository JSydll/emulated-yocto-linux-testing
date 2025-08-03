SUMMARY = "..."
IMAGE_LINGUAS = " "

LICENSE = "MIT"

inherit core-image deploy

# Testing support
DEPENDS:append = "labgrid-env-config"

IMAGE_INSTALL:append = " \
    packagegroup-core-boot \
    ${CORE_IMAGE_EXTRA_INSTALL} \
    rauc \
    e2fsprogs-mke2fs \
    mtd-utils \
"

IMAGE_INSTALL:append:virt-aarch64 = " \
    alive-service \
"

IMAGE_FSTYPES = "tar.bz2 wic.qcow2"
WKS_FILE = "secure-system-image.wks"

# Note: startup.nsh will be deployed by bootimg-efi.bbclass
IMAGE_EFI_BOOT_FILES:append = " \
    EFI/BOOT/*;EFI/BOOT/ \
    loader/loader.conf;loader/ \
    loader/entries/*;loader/entries/ \
"

# Dependencies for image creation and deployment of all relevant artifacts
do_image_wic[depends] += " \
    systemd-boot:do_deploy \
"

# TODO: Update this as soon as a real FIP is built
do_deploy[mcdepends] = " \
    mc::firmware:u-boot:do_deploy \
    mc::uefi-shell:edk2-firmware:do_deploy \
"

FIRMWARE_BINARY_PATH = "${TMPDIR}-firmware/deploy/images/${MACHINE}/${FIRMWARE_BINARY}"
FIRMWARE_BINARY_PATH[vardepsexclude] += "TMPDIR"

UEFI_SHELL_EFI = "${TMPDIR}-uefi-shell/deploy/images/${MACHINE}/shell.efi"
UEFI_SHELL_EFI[vardepsexclude] += "TMPDIR"

do_deploy() {
    install -m 0644 ${FIRMWARE_BINARY_PATH} ${DEPLOYDIR}/${FIRMWARE_BINARY}
    install -m 0644 ${UEFI_SHELL_EFI} ${DEPLOYDIR}/shell.efi
}
addtask do_deploy before do_image_wic


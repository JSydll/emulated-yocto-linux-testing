UBOOT_BOOTENV_FILE:virt-aarch64 = "bootenv-${RELEASE_TYPE}.img"

do_deploy:append:virt-aarch64() {
    cp ${DEPLOYDIR}/boot.scr ${DEPLOYDIR}/boot-${MACHINE}-${RELEASE_TYPE}.scr
    cp ${DEPLOYDIR}/${UBOOT_BINARY} ${DEPLOYDIR}/u-boot-${MACHINE}-${RELEASE_TYPE}.bin
}
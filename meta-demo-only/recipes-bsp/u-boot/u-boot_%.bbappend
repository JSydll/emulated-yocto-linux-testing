do_deploy:append:virt-aarch64() {
    cp ${DEPLOYDIR}/${UBOOT_BINARY} ${DEPLOYDIR}/u-boot-${MACHINE}-${RELEASE_TYPE}.bin
}
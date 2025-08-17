do_deploy:append:virt-aarch64() {
    cp ${DEPLOYDIR}/flash.bin ${DEPLOYDIR}/flash-${MACHINE}-${RELEASE_TYPE}.bin
}
FILESEXTRAPATHS:prepend := "${THISDIR}/systemd-boot:"

SRC_URI:append = " \
    file://loader.conf \
    file://shell.conf \
    file://startup.nsh \
"

# Depend on edk2-firmware mc

do_deploy:append() {
    install -d ${DEPLOYDIR}/loader/entries

    install ${UNPACKDIR}/loader.conf ${DEPLOYDIR}/loader/
    install ${UNPACKDIR}/shell.conf ${DEPLOYDIR}/loader/entries

    install ${UNPACKDIR}/startup.nsh ${DEPLOYDIR}
}
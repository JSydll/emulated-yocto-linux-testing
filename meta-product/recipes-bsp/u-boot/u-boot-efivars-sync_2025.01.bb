# -------------------
# NOT MEANT FOR PRODUCTIVE USE!
# -------------------

SUMMARY = "Provides a service to persist EFI variables on shutdown - given u-boot does not yet support SetVariableRT."

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

inherit systemd

SRC_URI = " \
    file://efivar.py \
    file://efivars-sync.py \
    file://run-efivars-sync.bash \
    file://efivars-sync.service \
"

RDEPENDS:${PN} = " \
    bash \
    efibootmgr \
    python3-core \
    python3-pyopenssl \    
"

S = "${UNPACKDIR}"

do_install(){
    install -d ${D}${bindir}
    install -m 0755 ${UNPACKDIR}/efivar.py ${D}${bindir}/u-boot-efivar-tool
    install -m 0755 ${UNPACKDIR}/efivars-sync.py ${D}${bindir}/efivars-sync
    install -m 0755 ${UNPACKDIR}/run-efivars-sync.bash ${D}${bindir}/run-efivars-sync

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${UNPACKDIR}/efivars-sync.service ${D}${systemd_system_unitdir}/efivars-sync.service
}

SYSTEMD_SERVICE:${PN} = "efivars-sync.service"

FILES:${PN} += " \
    ${bindir}/u-boot-efivar-tool \
    ${bindir}/efivars-sync \
    ${bindir}/run-efivars-sync \
    ${systemd_system_unitdir}/efivars-sync.service \
"
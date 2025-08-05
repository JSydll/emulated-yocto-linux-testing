SUMMARY = "Service broadcasting alive messages in the network."
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COMMON_LICENSE_DIR}/MIT;md5=0835ade698e0bcf8506ecda2f7b4f302"

SRC_URI = " \
    file://srv/alive-service \
    file://systemd/alive.service \
"

S = "${UNPACKDIR}"

RDEPENDS:${PN} = " bash systemd systemd-conf"

inherit systemd

SYSTEMD_SERVICE:${PN} = "alive.service"

do_install() {
    install -d ${D}${servicedir}
    install -m 0755 ${UNPACKDIR}/srv/alive-service ${D}${servicedir}/alive-service
    
    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${UNPACKDIR}/systemd/alive.service ${D}${systemd_system_unitdir}/alive.service
}

FILES:${PN} = " \
    ${servicedir}/alive-service \
    ${systemd_system_unitdir}/alive.service \
"
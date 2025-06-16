FILESEXTRAPATHS:prepend := "${THISDIR}/systemd-conf:"

SRC_URI:append:virt-aarch64 = " \
    file://10-can.network \
"

do_install:append:virt-aarch64() {
    install -d ${D}${systemd_unitdir}/network
    install -m 0644 ${S}/10-can.network ${D}${systemd_unitdir}/network
}

FILES:${PN}:append:virt-aarch64 = " \
    ${systemd_unitdir}/network/10-can.network \
"
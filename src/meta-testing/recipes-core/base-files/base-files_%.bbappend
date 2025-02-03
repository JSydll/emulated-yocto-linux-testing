# In this demo, do not display the warning that poky is not a productive distribution.
do_install:append() {
    rm ${D}${sysconfdir}/motd
}
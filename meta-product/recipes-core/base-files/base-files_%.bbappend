# Let wic create the fstab according to secure-image-minimal.wks
do_install:append:virt-aarch64() {
   rm ${D}/${sysconfdir}/fstab
}
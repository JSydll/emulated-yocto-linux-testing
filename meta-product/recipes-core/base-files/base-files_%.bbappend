# Let wic create the fstab according to secure-image-minimal.wks
do_install:append:virt-aarch64() {
   sed -i '/\/data/d' ${D}/${sysconfdir}/fstab
}
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

SRC_URI:append = " \
    file://bootflow.cfg \
"

# Fix proposed in https://github.com/agherzan/meta-raspberrypi/issues/1306 to resolve
# failing boot when uncompressing the kernel on raspberrypi 4 (and scarthgap).
SRC_URI:append:raspberrypi4 = " \
    file://memorysize.cfg \
"
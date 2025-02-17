FROM docker.io/labgrid/client

# Due to an issue in the default QEMU version distributed with Debian 12
# (see https://gitlab.com/qemu-project/qemu/-/issues/2343), we need to 
# upgrade to the lastest version to be able to use the pflash for persisting
# the u-boot environment.
RUN echo 'deb http://deb.debian.org/debian bookworm-backports main' > /etc/apt/sources.list.d/bookworm-backports.list && \
    apt update && \
    apt -t bookworm-backports install -y qemu-system-arm qemu-system-aarch64

# Plugins for parallelization
RUN pip install --break-system-packages pytest-xdist[psutil]
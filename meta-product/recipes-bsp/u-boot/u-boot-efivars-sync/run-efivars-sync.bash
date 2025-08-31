#!/bin/bash
set -e

readonly VARS_PARTITION="/dev/vda1"
readonly VARS_MOUNTPOINT="/mnt"
readonly VAR_ORIG="${VARS_MOUNTPOINT}/ubootefi.var"
readonly VAR_TMP="${VARS_MOUNTPOINT}/ubootefi.var.tmp"

mount "${VARS_PARTITION}" "${VARS_MOUNTPOINT}"
trap 'umount "${VARS_MOUNTPOINT}"' EXIT

cp "${VAR_ORIG}" "$VAR_TMP"
if /usr/bin/efivars-sync "${VAR_TMP}"; then
    mv "${VAR_TMP}" "${VAR_ORIG}"
else
    echo "efivars-sync failed, not updating ubootefi.var!" >&2
    rm "${VAR_TMP}"
    exit 1
fi

exit 0
